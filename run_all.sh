here=`pwd`
ref_data_dir=$here/data
data_dir=$here/data/water_selected_5kcalmol
scr_dir=$here/graphdescriptors
res=$here/results
mkdir -p $res

for c in $data_dir/W*xyz
do
  tmp=$(basename -- "$c")
  out="${tmp%-*}"
  python $scr_dir/get_descriptors.py --data_path $c --output $res/$out"_df.csv" --min_dir $ref_data_dir --single
  #mv $out"_df.csv" $res/
done
