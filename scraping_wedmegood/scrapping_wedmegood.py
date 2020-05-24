from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
def change(driver,ind):
	t1=driver.find_elements_by_class_name("vendor-pagination")
	if(len(t1)==0):
		return False
	else:
		t2=t1[0].find_element_by_class_name('paginate-active').text
		if(t2==str(index)):
			print(t2)
			return True
		else:
			print(t2,index)
			return False
place_name="bangalore"
shops={
	"wedding venues":["wedding-venues/all/",["banquet hall","lawn farmhouse","resort","small function halls","destination wedding venues","kalyan mandapam","five star"]],
	"photographers":["",["wedding photographers","wedding videography","pre wedding shoot"]],
	"food at wedding":["",["wedding catering","wedding cakes","bartenders wedding"]],
	"planning & decor":["",["planners","wedding decorators"]],
	"mehendi artists":["",["mehendi artists"]],
	"makeup":["",["bridal makeup"]],
	"music & dance":["",["djs","sangeet choreographers","wedding entertainment"]],
	"jewellery & accessories":["",["wedding jewellery","wedding accessories"]],
	"wedding pandits":["",["pandit wedding"]],
	"invites & gifts":["",["wedding cards","wedding favors","trousseau packers"]],
	"bridal wear":["bridal-wear/all/",["bridal lehenga stores","kanjeevaram sarees stores","wedding gowns shopping","wedding dress rentals"]],
	"groom wear":["groom-wear/all/",["sherwani for groom","wedding suits tuxes","sherwani on rent"]]
}

path_to_extension = r'/home/shivam/intern/1.5_0'

chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)


driver = webdriver.Chrome(executable_path='/home/shivam/chromedriver',chrome_options=chrome_options)
driver.create_options()

writer = pd.ExcelWriter('wedMeGood.xlsx', engine='xlsxwriter')
for shop in shops:
	total = []
	for shop_type in shops[shop][1]:
		shop_type1=shop_type.replace(' ','-')
		url = "https://www.wedmegood.com/vendors/"+place_name+"/"+shops[shop][0]+shop_type1+"/"
		driver.get(url)
		index=2
		while True:
			results = driver.find_elements_by_class_name("vendor-info")
			for result in results:
				details=shop_type
				name=None
				location=None
				charges=""
				try:
					temp=result.find_elements_by_class_name('vendor-detail')
					name=temp[0].text
					location=temp[1].text
					charges=temp[2].text
				except:
					name=None
					location=None
					charges=""
				finally:
					charge_temp=""
					try:
						charge_temp=result.find_elements_by_class_name('text-primary')
						charges=charges+" "+charge_temp[1].text
					except:
						charge_temp=""
					finally:
						rating=None
						try:
							rating=result.find_element_by_class_name('StarRating').text
						except:
							rating=None
						finally:
							new = ((name,location,details,rating,charges))
							total.append(new)
			try:
				driver.find_element_by_class_name("next").click()
			except:
				break
			finally:
				try:
				    element = WebDriverWait(driver, 20).until(
				        lambda driver: change(driver,index)
				    )
				except:
					break
				finally:
				    driver.implicitly_wait(1)
				    index+=1
	df = pd.DataFrame(total,columns=['NAME','LOCATION','DETAILS','RATING','CHARGES'])
	df=df.set_index('NAME')
	df = df.loc[~df.index.duplicated(keep='first')]
	df.to_excel(writer,sheet_name=shop)
writer.save()
driver.close()
