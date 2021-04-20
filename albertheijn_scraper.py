# %%
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from concurrent.futures import ThreadPoolExecutor, as_completed

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

threads = []
valid_ids = []
with ThreadPoolExecutor(max_workers=45) as executor:

    for x in range(9999999):
        threads.append(executor.submit(return_ah_page_source, x))

    for task in as_completed(threads):
        result, id = task.result()
        if result:
            valid_ids.append(id)
        print('\r' + str(id), end ='') 

#%%

# %%
