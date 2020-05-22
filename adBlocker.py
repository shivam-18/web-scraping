from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path_to_extension = r'/home/shivam/intern/1.5_0'

chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)


driver = webdriver.Chrome(executable_path='/home/shivam/chromedriver',chrome_options=chrome_options)
driver.create_options()
driver.get("http://www.google.com")