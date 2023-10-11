#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_GradBoost_all-metrics_36__PSG_shap_1_LF_level1_EXP-final-GB-normal_train-data/kTkV_GradBoost_all-metrics_36__PSG_shap_1_LF_level1_EXP-final-GB-normal_train-data.prof /projectnb/skiran/saurav/Fall-2022/src2/scripts/main.py -CV kTkV -model GradBoost -metric all-metrics -f 36 -stratified  -data PSG -features_R shap -frstep 1 -approach LF -level level1 -experiment EXP-final-GB-normal -feature_base train-data
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_GradBoost_all-metrics_36__PSG_shap_1_LF_level1_EXP-final-GB-normal_train-data/kTkV_GradBoost_all-metrics_36__PSG_shap_1_LF_level1_EXP-final-GB-normal_train-data.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_GradBoost_all-metrics_36__PSG_shap_1_LF_level1_EXP-final-GB-normal_train-data/kTkV_GradBoost_all-metrics_36__PSG_shap_1_LF_level1_EXP-final-GB-normal_train-data.svg
