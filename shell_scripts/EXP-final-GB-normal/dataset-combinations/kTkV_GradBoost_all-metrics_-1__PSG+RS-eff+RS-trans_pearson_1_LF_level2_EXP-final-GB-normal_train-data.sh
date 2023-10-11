#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_GradBoost_all-metrics_-1__PSG+RS-eff+RS-trans_pearson_1_LF_level2_EXP-final-GB-normal_train-data/kTkV_GradBoost_all-metrics_-1__PSG+RS-eff+RS-trans_pearson_1_LF_level2_EXP-final-GB-normal_train-data.prof /projectnb/skiran/saurav/Fall-2022/src2/scripts/main.py -CV kTkV -model GradBoost -metric all-metrics -f -1 -stratified  -data PSG+RS-eff+RS-trans -features_R pearson -frstep 1 -approach LF -level level2 -experiment EXP-final-GB-normal -feature_base train-data
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_GradBoost_all-metrics_-1__PSG+RS-eff+RS-trans_pearson_1_LF_level2_EXP-final-GB-normal_train-data/kTkV_GradBoost_all-metrics_-1__PSG+RS-eff+RS-trans_pearson_1_LF_level2_EXP-final-GB-normal_train-data.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_GradBoost_all-metrics_-1__PSG+RS-eff+RS-trans_pearson_1_LF_level2_EXP-final-GB-normal_train-data/kTkV_GradBoost_all-metrics_-1__PSG+RS-eff+RS-trans_pearson_1_LF_level2_EXP-final-GB-normal_train-data.svg
