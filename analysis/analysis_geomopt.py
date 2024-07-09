import os
import pandas as pd
import numpy as np
from pathlib import Path
import shutil
from pprint import pprint

parent=Path.cwd().parents[0]

dir_df=Path(parent, "results").resolve()
dir_xyz=Path(parent, "data/water_selected_5kcalmol_reoptimized/").resolve()

outdir=Path(dir_df, "optimized_structures").resolve()
if outdir.exists():
    shutil.rmtree(outdir)

def select_structures(df,typ):
    '''
    here, we first count the number of structures of type "typ", and
    from these structures, we select the one of the lowest energy
    '''
    counter = df[typ].value_counts()
    s = pd.DataFrame(index=None,columns=['motif', 'Nmotif', 'Nstruc_motif', 'IDstruc_minE'])
    for k, v in counter.items():
        s2={}
        s2["motif"] = typ
        s2["Nmotif"] = k
        s2["Nstruc_motif"] = v
        sub_df = df[df[typ] == k]
        id_e = sub_df[sub_df["Actual Energy"] == min(sub_df["Actual Energy"])]["Id"].iloc[0]
        e = sub_df[sub_df["Actual Energy"] == min(sub_df["Actual Energy"])]["Actual Energy"].iloc[0]
        s2["IDstruc_minE"] = id_e
        s2["fxyz"] = id_e+1
        s2["Actual Energy"] = e
        s = s._append(s2, ignore_index = True)
    return s

def run_single_analysis(df,f_out,dir_out,dir_xyz):
    frames = []
    motifs=["Trimers", "Tetramers", "Pentamers", "Hexamers"]
    for m in motifs:
        data = select_structures(df,m)
        # now, select only the ones with the maximum number of a "motif"
        max_m = data['Nmotif'].max()
        data_f = data[data["Nmotif"] == max_m]
        # if the lowest-energy structure is not in selected, then add it here:
        data_f = pd.concat([data[data["IDstruc_minE"] == 0], data_f.loc[:]]).reset_index(drop=True)
        frames.append(data_f)
    selected = pd.concat(frames)
    mol = Path(f_out).stem.split('_')[0]
    selected["mol"] = mol
    # WARNING: assuming that xyz files with separated structures are in "$dir_xyz/*_water_prep/*_struc_$x.xyz" files
    selected['fxyz']=selected['fxyz'].apply(lambda x: str(Path(dir_xyz,mol+"_water_prep",mol+"_struc_"+str(int(x))+".xyz")))
    unique_fxyz= selected['fxyz'].drop_duplicates().to_list()
    return selected, unique_fxyz


# print explanation of keys on the dataframe:

def helpmsg():
    print("There are 'Nstruc_motif' structures that have 'Nmotif' [Trimers/Tetramers/Pentamers/Hexamers].")
    print("Among them, the ID of the lowest-energy structure is 'IDstruc_minE' and the corresponding energy is 'Actual Energy'.")
    print("Then, 'fxyz' is the file with the selected molecular structure.")


for x in dir_xyz.iterdir():
    if x.is_dir():
        molname=x.name
        for y in x.iterdir():
            if y.is_dir:
                modelname=y.name
                # first, concatenate all xyz files into one:
                xyzcomments = {f.stem:f.stem+"_"+modelname for f in Path(y).glob("*.xyz")}
                fxyzall = Path(y, molname+"_"+modelname+".xyz").resolve()
                with open(fxyzall, 'w') as fout:
                    for fxyzinp in Path(y).glob("*_optimized.xyz"):
                        with open(fxyzinp, 'r') as finp:
                            lines = finp.readlines()
                            for line in lines:
                                if len(line.strip()) > 0:
                                    #print(line.strip())
                                    fout.write(line)
                                else:
                                    #print(xyzcomments[fxyzinp.stem])
                                    fout.write(xyzcomments[fxyzinp.stem]+"\n")
#
#for file in Path(dir_df).glob("*.csv"):
#    if file.stem.startswith("W"):
#        df=pd.read_csv(file)
#        selected, xyz_list=run_single_analysis(df,Path(file),dir_df,dir_xyz)
#
#        for xyz in xyz_list:
#            f = file.stem.replace('_5.0_KCal_df', '_selected')
#            p = Path(outdir, f).resolve()
#            p.mkdir(parents=True, exist_ok=True)
#            shutil.copy(xyz, p)
#
#        summary=Path(outdir, Path(file).stem+"_selected.csv").resolve()
#        selected.to_csv(summary, index=False)



