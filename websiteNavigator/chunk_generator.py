#%%
import pandas as pd

df = pd.read_csv('valid_ids.csv',sep=': ',index_col=0,names=['id','value'], engine='python')
df = df.loc[df['value'] == True]
codes = df.index.tolist()
chunks = 20
chunk_size = (len(codes)//chunks) + 1

for i in range(chunks):
    code_block = codes[i*chunk_size : (i+1)*chunk_size]    
    with open(f'./codeblocks/codeblock{i+1}.csv','w') as out:
        for code in code_block:
            print(code,file=out)


# %%
