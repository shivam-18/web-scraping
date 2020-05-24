from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
place_name="chennai"
categories={
	"Dance":["Western Dance Academy India","Classical Dance Academy India","Bollywood Dance Academy India","Zumba Academy India","Bhangra Academy India","Western Dance teacher India","Classical Dance Teacher India", "Bollywood Dance Teacher India", "Zumba Teacher India", "Bhangra Teacher India"],
	"Foreign Languages":["Learn French India", "Learn German India", "Learn English India", "French Tutor India", "German Tutor India", "English Tutor India"],
	"Story Time":["Story Telling India", "Story Telling Festival India"],
	"Singing":["Singing academy India", "Singing tutor india"],
	"Yoga":["Yoga Academy India", "Yoga Instructor India"],
	"Chess":["Chess Academy India", "Learn Chess India"]
}
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
writer = pd.ExcelWriter('googleMaps_'+place_name+'.xlsx', engine='xlsxwriter')
for category in categories:
	total = []
	for sub_cat in categories[category]:
		sub_cat1=sub_cat.replace(' ','+')
		url = "https://www.google.com/maps/search/"+sub_cat1+"+in+"+place_name+"/"
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
									votes=None
									try:
										votes = result.find_element_by_class_name('section-result-num-ratings').text
										votes=votes[:-1]
										votes=votes[1:]
										votes=int(votes)
									except:
										votes=None
									finally:
										new = ((name,location,details,contact,rating,votes,sub_cat))
										if(name!=None and votes!=None):
											if(votes>=50):
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
	df = pd.DataFrame(total,columns=['NAME','LOCATION','DETAILS','CONTACT','RATING','VOTES','SUB-CATEGORY'])
	df=df.set_index('NAME')
	df = df.loc[~df.index.duplicated(keep='first')]
	df.to_excel(writer,sheet_name=category)
writer.save()
driver.close()