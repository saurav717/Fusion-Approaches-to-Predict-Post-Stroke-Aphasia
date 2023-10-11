#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_2__RS-trans_pearson_1_EF_level1_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_2__RS-trans_pearson_1_EF_level1_EXP-final-RF-normal_train-data.prof /projectnb/skiran/saurav/Fall-2022/src2/scripts/main.py -CV kTkV -model RF -metric all-metrics -f 2 -stratified  -data RS-trans -features_R pearson -frstep 1 -approach EF -level level1 -experiment EXP-final-RF-normal -feature_base train-data
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_2__RS-trans_pearson_1_EF_level1_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_2__RS-trans_pearson_1_EF_level1_EXP-final-RF-normal_train-data.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_2__RS-trans_pearson_1_EF_level1_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_2__RS-trans_pearson_1_EF_level1_EXP-final-RF-normal_train-data.svg
