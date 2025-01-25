here=`pwd`
parent="$(dirname "$here")"
ref_data_dir=$parent/data
data_dir=$parent/data
data_dir_selected=$parent/data/water_selected_5kcalmol
scr_dir=$parent/graphdescriptors
res=$here/results
ref=$here/reference
mkdir -p $res

#
# this tests the code as used in the original paper:
#
python $scr_dir/get_descriptors.py --data_path $data_dir/test_predictions.xyz --output $res/test_df.csv --min_dir $ref_data_dir
python verify.py $res/test_df.csv $ref/test_df.csv

#
# this tests the modified code: compare the selected W6 structures from the wdbase against W6 of the lowest energy:
#
python $scr_dir/get_descriptors.py --reference_path $data_dir/W6_geoms_all_lowestE.xyz --data_path $data_dir_selected/W6_geoms_5.0_KCal-1hgztfv.xyz --output $res/test_W6_wdbase.csv --min_dir $ref_data_dir
python verify.py $res/test_W6_wdbase.csv $ref/test_W6_wdbase.csv
