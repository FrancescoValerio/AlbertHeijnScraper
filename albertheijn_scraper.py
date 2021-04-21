# %%
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
archive = pd.read_csv('valid_ids.csv',sep=': ',index_col=0,names=['id','value'])
# %%
def return_ah_page_source(id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    valid_page = False



    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    url = 'https://www.ah.nl/producten/product/' + str(id)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'accept-cookies'))).click()
    page_source = driver.page_source
    try:
        driver.find_element_by_xpath("//h2[contains(text(), 'Voedingswaarden')]").text
        valid_page = True
    except NoSuchElementException:
        pass
    driver.quit()
    return valid_page, id
def get_code(number):
    try:
        response = requests.get(f'https://www.ah.nl/producten/product/wi{number}/')
    except requests.Timeout:
        return 0, 0
    if response.status_code == 404:
        valid_page = False
    if response.status_code == 200:
        valid_page = True
    return number, valid_page
#%%
with open('valid_ids.csv','a') as f:
    threads = []
    id_result = {}
    with ThreadPoolExecutor(max_workers=50) as executor:

        for number in reversed(range(100000,900000)):
            if number in archive.index:
                continue
            threads.append(executor.submit(get_code, number))
        for task in as_completed(threads):
            id, result = task.result()
            if id == 0 and task == 0:
                print('connection problem occured')
                break
            id_result[id] = result
            print(str(id) + ': '+str(result),file=f)
#%%

# %%
