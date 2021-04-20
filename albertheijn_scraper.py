# %%
from selenium import webdriver

browser = webdriver.Chrome()

test_url = 'https://www.ah.nl/producten/product/wi368'

browser.get(test_url)
# accept cookies button


product_not_found = 'helaas, we konden dit product niet vinden'
if product_not_found in str(browser.page_source):
    print('product not found')
#%%
