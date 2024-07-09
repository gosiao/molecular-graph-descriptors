here=`pwd`
parent="$(dirname "$here")"
ref_data_dir=$parent/data
data_dir=$parent/data/water_selected_5kcalmol_reoptimized
scr_dir=$parent/graphdescriptors
res=$parent/results/optimized_structures
mkdir -p $res


for mol in $data_dir/*
do
  molname=`basename "$mol"`
  cd $mol
  for model in $mol/*
  do
    modelname=`basename "$model"`
    echo $model
    cd $model
    finp=${molname}"_"${modelname}".xyz"
    fout=${molname}"_"${modelname}".csv"
    python $scr_dir/get_descriptors.py --data_path $finp --output $fout --min_dir $ref_data_dir --single
    cd ../
  done
  cd ../
done
