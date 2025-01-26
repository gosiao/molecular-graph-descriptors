here=`pwd`
parent="$(dirname "$here")"
ref_data_dir=$parent/data
data_dir_selected=$parent/data/water_selected_5kcalmol/W6_water_prep
scr_dir=$parent/graphdescriptors
res=$here/results
ref=$here/reference
mkdir -p $res

#
# this tests the possibility to export the structural information for a single structure;
#
python $scr_dir/get_descriptors.py --data_path $data_dir_selected/"W6_struc_62.xyz" --output $res/"W6_struc_62_df.csv"  --single
python verify.py $res/W6_struc_62_df.csv $ref/W6_struc_62_df.csv

#
# the same, but loops over many files:
#
#for c in $data_dir_selected/W*xyz
#do
#  tmp=$(basename -- "$c")
#  out="${tmp%.*}"
#  #echo $c $tmp $out
#  python $scr_dir/get_descriptors.py --data_path $c --output $res/$out"_df.csv" --single
#done
