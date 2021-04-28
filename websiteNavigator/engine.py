
#%%
from random import shuffle
from numpy import product
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from pprint import pprint
df = pd.read_csv('valid_ids.csv',sep=': ',index_col=0,names=['id','value'], engine='python')
df = df.loc[df['value'] == True]
codes = df.index.tolist()
shuffle(codes)

#%%
succes ={}
database = {}
chrome_options = Options()
chrome_options.add_argument("--headless")

for code in tqdm(codes):
    succes[code] = False
    driver = webdriver.Chrome(ChromeDriverManager(print_first_line=False, log_level=0).install(),options=chrome_options)
    url = 'https://www.ah.nl/producten/product/wi' + str(code)
    driver.get(url)

    # click accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'accept-cookies'))).click()

    # get product name
    product_name = driver.find_element_by_tag_name('h1').text

    # get product price
    try:
        price = float(driver.find_element_by_xpath("//div[@data-testhook='price-amount']").text)
    except NoSuchElementException:
        driver.quit()
        continue
    try:
        weightperkilo =  driver.find_element_by_xpath("//div[@class='product-card-header_unitInfo__2ncbP']").text
    except NoSuchElementException:
        driver.quit()
        continue
    try:
        priceperkilo = driver.find_element_by_xpath("//span[@class='product-card-header_unitPriceWithPadding__MonzR']").text
    except NoSuchElementException:
        driver.quit()
        continue
    # get product weight
    weight = weightperkilo.replace(priceperkilo,'')

    # get nutritional info table
    try:
        table = driver.find_element_by_class_name("product-info-nutrition_table__1PDio")
    except NoSuchElementException:
        driver.quit()
        continue
    nutritional_info = table.text.split('\n')

    succes[code] = True
    database[code] ={
        'name':product_name,
        'price':price,
        'sold_per':weight,
        'price_per':priceperkilo,
    }
    split_info = [re.sub(r'(\d+)', '\n\\1', nut,count=1) for nut in nutritional_info]
    true_split = [s.split('\n',1) for s in split_info]
    for label, amount in true_split:
        database[code][label] = amount
    '''
    pprint(product_name)
    pprint(price)
    pprint(weight)
    pprint(priceperkilo)
    pprint(nutritional_info)
    '''
    driver.quit()

# %%
''' TODO 
    - Wrapper for try excep
    - Keep record of which id's succeed all checks
    - Keep record of all info
'''

# %%
