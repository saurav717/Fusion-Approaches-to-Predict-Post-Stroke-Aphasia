from libraries import *
from params import * 

class getData:
    def __init__(self, settings):
        self.path = PATH_DATA
        self.augment = settings["Augment"]
        # self.path = PATH
        self.repeat_features = settings["repeat features"]
        # self.init()
        self.all_features = []
        
        dta = settings["data"]
        if dta == "RS": # Done
            print("loading resting state data")
            self.init()
        elif dta == "stan_optimal": 
            print("loading stan's data")
            self.stan_optimal()
        # elif dta == "LS": # Done
        #     print("loading WM GM lesion remaining data")
            # self.init2()
        elif dta == "MM": # Done
            self.multi_modal()
        else:
            self.dta = dta
            self.init3()
        
    
    def read_data(self):
        
        df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        outputs = df[("behavioral", "wab_aq_bd")].values
        outputs = outputs.reshape(len(outputs),1)

        data = {}

        # AQ - Aphasia Quotient
        data["AQ"] = pd.DataFrame(df[('behavioral', "wab_aq_bd")].values, columns = ["wab_aq_bd"]) 

        # DM - Demographics
        data["DM"] = df["demographic_info"]

        # FA - Fractional Anisotropy
        featuresFAL = ["fa_avg_ccmaj", "fa_avg_ccmin", "fa_avg_lifof", "fa_avg_lilf", "fa_avg_lslf", "fa_avg_lunc", "fa_avg_larc"]
        featuresFAR = ["fa_avg_rifof", "fa_avg_rilf", "fa_avg_rslf", "fa_avg_runc", "fa_avg_rarc"]
        FA_L = df["average_FA_values"][featuresFAL].fillna(0).values
        FA_R = df["average_FA_values"][featuresFAR].fillna(df["average_FA_values"][featuresFAR].mean()).values
        data["FA"] = pd.DataFrame(np.hstack((FA_L, FA_R)), columns = featuresFAL+featuresFAR)

        # PS_G - percent grey matter per region  
        data["PSG"] = df["percent_spared_in_gray_matter"]

        # PS_W - percent white matter per region  
        data["PSW"] = df["percent_spared_in_white_matter"]

        # RS - Resting state data
        data["RS"] = df["restingstate_bivariate_correlations"]

        # LS - Lesion size (Total)   ; Need to add lesion size per region
        data["LS"] = pd.DataFrame(df[("lesion_size", "lesion_size_ls")].values, columns = ["lesion_size_ls"])

        self.datadict = data 
        self.outputs = outputs
    
    
    def init3():
        self.read_data()
    
        features = self.dta.split("-")
    
        correlations = []
        for i,dataset in enumerate(features):
            if i==0:
                correlations = self.datadict[dataset].values
                featureList = list(self.datadict[dataset].columns)
                
            else:
                correlations = np.hstack((correlations, self.datadict[dataset].values))
                featureList += list(self.datadict[dataset].columns)
        
        self.correlation_data = correlations
        self.all_features = featureList
        
        
    
    def multi_modal(self):
        data = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/src2/data/" + "allModalityOutputs.xlsx" )
        self.outputs = data["ground truth score"].values
        self.all_features = data.columns
        self.correlation_data = data.drop(["ground truth score", "Unnamed: 0"], axis = 1)


    def reduce_features(self, data,outputs, num_features, columns):
        

        data = np.hstack((data, outputs))
        data = pd.DataFrame(data)
    
        corrs = data.corr().abs()
        importances = corrs.values[-1][:-1]
        
        top_columns = np.argpartition(importances, -num_features)[-num_features:]
    
        data = data.iloc[:,top_columns]
        self.all_features += list(data.columns)
        
        outputs = outputs.ravel()
        data = data.values
        return data


    def stan_optimal(self):
        print("using stan's data")
        df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        outputs = df[("behavioral", "wab_aq_bd")].values
        outputs = outputs.reshape(len(outputs),1)
    
        data = {}
        data["AQ"] = df[('behavioral', "wab_aq_bd")].values[:, np.newaxis]
        data["DM"] = df["demographic_info"].values
    
        featuresFAL = ["fa_avg_ccmaj", "fa_avg_ccmin", "fa_avg_lifof", "fa_avg_lilf", "fa_avg_lslf", "fa_avg_lunc", "fa_avg_larc"]
        featuresFAR = ["fa_avg_rifof", "fa_avg_rilf", "fa_avg_rslf", "fa_avg_runc", "fa_avg_rarc"]

        FA_L = df["average_FA_values"][featuresFAL].fillna(0).values
        FA_R = df["average_FA_values"][featuresFAR].fillna(df["average_FA_values"][featuresFAR].mean()).values
        data["FA"] = np.hstack((FA_L, FA_R))
        data["FA"] = self.reduce_features(data["FA"], outputs, 2, pd.Index(featuresFAL + featuresFAR))

        data["PS_G"] = df["percent_spared_in_gray_matter"].values
        data["PS_G"] = self.reduce_features(data["PS_G"], outputs, 4, df["percent_spared_in_gray_matter"].columns)

        data["RS"] = df["restingstate_bivariate_correlations"].values
        data["RS"] = self.reduce_features(data["RS"], outputs, 11, df["restingstate_bivariate_correlations"].columns)
        
        self.all_features += list(df["demographic_info"].columns)
        total_data = np.hstack((data["FA"], data["PS_G"]))
        total_data = np.hstack((total_data, data["RS"]))
        # total_data = np.hstack((total_data, data["AQ"]))
        total_data = np.hstack((total_data, data["DM"]))
        
        total_data = pd.DataFrame(total_data)
        
        self.correlation_data = total_data.values 
        self.outputs = outputs

            
    def init2(self): # this needs to be removed later in early fusion.
        data = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        self.outputs = data[("behavioral", "wab_aq_bd")].values

        d1 = data["percent_spared_in_white_matter"]
        d2 = data["percent_spared_in_gray_matter"]
        d3 = data["lesion_size"]
        
        df = pd.concat([d1,d2], axis = 1)
        df = pd.concat([df,d3], axis = 1)
        self.all_features = df.columns
        self.correlation_data = df.values
            
        

    # def sortFiles(self) -> None:
    #     # READING THE DATA,
    #     self.column_names = pd.read_csv(self.path + "/" + "ROIs.csv", header = None)
    #     # self.all_features = self.column_names
    #     self.files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
    #     self.files.remove("ROIs.csv")
    #     self.files = np.sort(self.files) # file names for the data"

    #     # READING THE FILE TO GET PATIENT SCORES",
    #     real_df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/RS_bivariate_AQ_continuous.xlsx")
    #     rdf = real_df[["participant", "AQ"]]

    #     # EXTRACTING THE WAB SCORES OF THE PATIENTS
    #     parts = list(rdf["participant"])
    #     self.participants= parts[:30] + parts[31:32] + parts[35:51] + parts[53:60] + parts[61:63] + parts[30:31] # participant IDs"
    #     self.wabaq = list(rdf["AQ"])  # Participant scores"
    
    def sortFiles(self) -> None:
        mypath = "/projectnb/skiran/Isaac/data_for_saurav/"
        self.path =  mypath
        subjectIDs = pd.read_csv(mypath+"Subject_IDs.csv", header = None)
        
        filenames = listdir(mypath)
        csvfiles = [ filename for filename in filenames if filename.endswith( ".csv" ) ]
        csvfiles.remove('Subject_IDs.csv')
        csvfiles = sorted(csvfiles)
        
        pdf = {"patientIDs" : list(subjectIDs.values.flatten().astype(str)),
               "alias" : list(csvfiles)
              }
        pdf_alias = pd.DataFrame(pdf)
        
        
        df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        outputs = df[("behavioral", "wab_aq_bd")]
        
        pdf = { "patientIDs": list(df[("participant", "participant")]),
                "scores" : list(outputs) 
              }
        pdf_scores = pd.DataFrame(pdf)
        
        
        
        corr_data = []
        scores = []
        for patient, score in pdf_scores.values:
            if patient != "BU29c07":
                fname = mypath  + list(pdf_alias[pdf_alias["patientIDs"] == patient]["alias"])[0]
                scores.append(score)
                df = pd.read_csv(fname)
                columns = df.columns
                df.index = columns
                corr_data.append(df)
            else:
                fname = mypath  + list(pdf_alias[pdf_alias["patientIDs"] == patient+"NU"]["alias"])[0]
                df = pd.read_csv(fname)
                columns = df.columns
                df.index = columns
                scores.append(score)
                corr_data.append(df)

        self.correlation_data = corr_data
        self.outputs = scores
        
        print("correlation data shape first new data = ", np.array(self.correlation_data).shape)
        print("output shape first new datz = ", np.array(self.outputs).shape)
        
        


    def noAugment(self) -> None:

        # self.correlation_data = []
        # self.outputs = []

        def modify_data():
            for index,data in enumerate(self.correlation_data):
                df = data
                df = df.where(np.triu(np.ones(df.shape),k=1).astype(np.bool))
                df = df.stack().reset_index()
                df.columns = ['Row','Column','Value']
                df["index"] = df["Row"] + "-vs-" + df["Column"]
                self.correlation_data[index] = df["Value"].values #data.values[np.triu_indices(48, k = 1)]
                self.all_features = df["index"]

            self.correlation_data = np.array(self.correlation_data)
            self.outputs =  np.array(self.outputs)

        # for patient_index, patient_file in enumerate(self.files):

            # READING THE PATIENT TIME SERIES FMRI DATA
            # file = pd.read_csv(self.path + "/" + self.files[patient_index], header = None)
            # file.columns = list(self.column_names[0])
            # file = file.reindex(sorted(file.columns), axis = 1)

            
            # CALCULATE THE CORRELATION MATRIX\n",
            # self.correlation_data.append(file.corr())
            # self.outputs.append(self.wabaq[patient_index])

        modify_data()

    # def reduce(self):


    def data(self, reduce = False):
        if reduce == True:
            self.reduce()
        return self.all_features, self.correlation_data, self.outputs

    def params(self, model):
        if model == "SVR":
            return


    def init(self):
        # GETTING THINGS READY TO GET THE DATA
        self.sortFiles()

        # GETTING THE DATA
        if self.augment:
            raise NotImplementedError
            self.augment() 
        else:
            self.noAugment()

    def describe(self):
        print('data shape = ', self.correlation_data.shape)
        print("output shape = ", self.outputs.shape)