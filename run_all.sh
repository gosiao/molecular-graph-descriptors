here=`pwd`
ref_data_dir=$here/data
data_dir=$here/data
scr_dir=$here/graphdescriptors
res=$here/results
mkdir -p $res

python $scr_dir/get_descriptors.py --data_path $data_dir/test_predictions.xyz --output $res/test_df.csv --min_dir $ref_data_dir

