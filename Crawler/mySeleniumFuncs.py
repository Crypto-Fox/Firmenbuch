from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://google.com")
html = driver.page_source
print html