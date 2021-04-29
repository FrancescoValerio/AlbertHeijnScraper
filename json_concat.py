#%%
import json
import os
import pandas as pd

collection = []
for file in sorted(os.listdir('./database')):
    with open('./database/'+file,'r') as f:
        tmp_d = json.load(f)
    ids = list(tmp_d)
    for id in ids:
        collection.append({**tmp_d[id],**{'id':id}})
df = pd.DataFrame.from_records(collection,index='name')
df.to_excel('ah_product_database.xlsx')
# %%
