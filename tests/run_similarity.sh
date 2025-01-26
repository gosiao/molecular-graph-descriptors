here=`pwd`
parent="$(dirname "$here")"
ref_data_dir=$parent/data
data_dir_selected=$parent/data/water_selected_5kcalmol/W6_water_prep
scr_dir=$parent/graphdescriptors
res=$here/results
ref=$here/reference
mkdir -p $res

#
# this tests the calculation of similarity graphs between two structures
# here: calculations for f1 against the reference f2:
#
f1="W6_struc_1"
f2="W6_struc_68"
python $scr_dir/get_descriptors.py --data_path $data_dir_selected/$f1.xyz --reference_path $data_dir_selected/$f2.xyz --output $res/$f1"_"$f2"_df.csv"
python verify.py $res/$f1"_"$f2"_df.csv" $ref/$f1"_"$f2"_df.csv"
