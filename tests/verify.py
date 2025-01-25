import sys
import pandas as pd
from pandas.testing import assert_frame_equal

f1=sys.argv[1]
f2=sys.argv[2]

df1=pd.read_csv(f1)
df2=pd.read_csv(f2)

try:
    assert_frame_equal(df1, df2, check_like=True)
except:
    print("ERROR: Different dataframes on {} and {}!".format(f1,f2))
    df_diff = pd.concat([df1,df2]).drop_duplicates(keep=False)
    print(df_diff)

