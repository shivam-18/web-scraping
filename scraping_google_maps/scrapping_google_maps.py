from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
place_name="bangalore"
place=["Koramangala","Indiranagar","M.G. Road","HSR Layout","Richmond Town","Jayanagar","BTM Layout","Sarjapur","Whitefield","Bannerghatta Road","Malleswaram","Kammanahalli","Basavanagudi","Marathahalli","Bellandur","Yelahanka","Hebbal","KR Puram","Banashankari","Electronic City"]
shops=["event planner","fashion designer","salon","photographer","dj","bakery","coaching","web designer","graphic designer","interior designer","rental properties","chemist","florist","decor","venue","caterer","av"]
webdriver = "/home/shivam/chromedriver"
def change(driver,ind):
	t1=driver.find_elements_by_class_name("gm2-caption")
	if(len(t1)==0):
		return False
	else:
		t2=t1[0].find_element_by_class_name('n7lv7yjyC35__left').text
		temp="Showing results "+str((1+ind)*20+1)+" "
		if(t2.split('-')[0]==temp):
			print(temp)
			return True
		else:
			print(t2,temp)
			return False

driver = Chrome(webdriver)
writer = pd.ExcelWriter('googleMaps.xlsx', engine='xlsxwriter')
for shop in shops:
	total = []
	for area in place:
		place1=(shop+" in "+place_name+" "+area).replace(' ','+')
		url = "https://www.google.com/maps/search/"+place1+"/"
		driver.get(url)
		index=0
		while True:
			results = driver.find_elements_by_class_name("section-result-text-content")
			for result in results:
				name=None
				try:
					name = result.find_element_by_class_name('section-result-title').text
				except:
					name=None
				finally:
					location=None
					try:
						location = result.find_element_by_class_name('section-result-location').text
					except:
						location=None
					finally:
						details=None
						try:
							details = result.find_element_by_class_name('section-result-details').text
						except:
							details=None
						finally:
							contact=None
							try:
								contact = result.find_element_by_class_name('section-result-phone-number').text
							except:
								contact=None
							finally:
								rating=None
								try:
									rating = result.find_element_by_class_name('section-result-rating').text
								except:
									rating=None
								finally:
									new = ((name,location,details,contact,rating,area))
									if(name!=None):
										total.append(new)
			try:
				driver.find_element_by_id("n7lv7yjyC35__section-pagination-button-next").click()
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
	df = pd.DataFrame(total,columns=['NAME','LOCATION','DETAILS','CONTACT','RATING','AREA'])
	df=df.set_index('NAME')
	df = df.loc[~df.index.duplicated(keep='first')]
	df.to_excel(writer,sheet_name=shop)
writer.save()
driver.close()