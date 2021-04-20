# %%
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# %%
def check_if_id_exists(id):
    found = True
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://www.ah.nl/producten/product/' + str(id)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'accept-cookies'))).click()
    product_not_found = 'helaas, we konden dit product niet vinden'
    if product_not_found in str(driver.page_source):
        found = False
    driver.quit()
    return found

test1 = check_if_id_exists('wi368')
test2 = check_if_id_exists('wi55960')
print(test1)
# %%
