here=`pwd`
parent="$(dirname "$here")"
ref_data_dir=$parent/data
data_dir=$parent/data
scr_dir=$parent/graphdescriptors
res=$here/results
mkdir -p $res

python $scr_dir/get_descriptors.py --data_path $data_dir/test_predictions.xyz --output $res/test_df.csv --min_dir $ref_data_dir

