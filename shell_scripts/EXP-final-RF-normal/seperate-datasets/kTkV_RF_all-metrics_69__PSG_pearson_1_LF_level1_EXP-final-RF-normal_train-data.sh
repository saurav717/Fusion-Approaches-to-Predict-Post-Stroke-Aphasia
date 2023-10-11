#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_69__PSG_pearson_1_LF_level1_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_69__PSG_pearson_1_LF_level1_EXP-final-RF-normal_train-data.prof /projectnb/skiran/saurav/Fall-2022/src2/scripts/main.py -CV kTkV -model RF -metric all-metrics -f 69 -stratified  -data PSG -features_R pearson -frstep 1 -approach LF -level level1 -experiment EXP-final-RF-normal -feature_base train-data
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_69__PSG_pearson_1_LF_level1_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_69__PSG_pearson_1_LF_level1_EXP-final-RF-normal_train-data.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_69__PSG_pearson_1_LF_level1_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_69__PSG_pearson_1_LF_level1_EXP-final-RF-normal_train-data.svg
