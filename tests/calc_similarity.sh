here=`pwd`
parent="$(dirname "$here")"
ref_data_dir=$parent/data
data_dir=$parent/data/water_selected_5kcalmol
scr_dir=$parent/graphdescriptors
res=$here/results
mkdir -p $res

for c in $data_dir/W*xyz
do
  tmp=$(basename -- "$c")
  out="${tmp%-*}"
  python $scr_dir/get_descriptors.py --data_path $c --output $res/$out"_df.csv" --min_dir $ref_data_dir --single
done
