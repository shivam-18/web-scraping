from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
place_name="kolkata"
categories={
	"Dance":["Western Dance Academy India","Classical Dance Academy India","Bollywood Dance Academy India","Zumba Academy India","Bhangra Academy India","Western Dance teacher India","Classical Dance Teacher India", "Bollywood Dance Teacher India", "Zumba Teacher India", "Bhangra Teacher India"],
	"Foreign Languages":["Learn French India", "Learn German India", "Learn English India", "French Tutor India", "German Tutor India", "English Tutor India"],
	"Story Time":["Story Telling India", "Story Telling Festival India"],
	"Singing":["Singing academy India", "Singing tutor india"],
	"Yoga":["Yoga Academy India", "Yoga Instructor India"],
	"Chess":["Chess Academy India", "Learn Chess India"]
}
#categories={"Dance":["Western Dance Academy India","Classical Dance Academy India"],"Foreign Languages":["Learn French India"]}
webdriver = "/home/shivam/chromedriver"
driver = Chrome(webdriver)
writer = pd.ExcelWriter('Youtube_'+place_name+'.xlsx', engine='xlsxwriter')
for category in categories:
	total = []
	for sub_cat in categories[category]:
		sub_cat1=sub_cat.replace(' ','+')
		url = "https://www.youtube.com/results?search_query="+sub_cat1+"+in+"+place_name+"&sp=EgIQAg%253D%253D"
		driver.get(url)
		
		SCROLL_PAUSE_TIME = 5
		last_height = driver.execute_script("return document.documentElement.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
			time.sleep(SCROLL_PAUSE_TIME)
			new_height = driver.execute_script("return document.documentElement.scrollHeight")
			print(new_height)
			if (new_height == last_height):
				print("break")
				break
			last_height = new_height

		results = driver.find_elements_by_id("content-section")
		for result in results:
			name=None
			try:
				name = result.find_element_by_id('text').text
			except:
				name=None
			finally:
				subscribers=None
				try:
					subscribers = result.find_element_by_id('subscribers').text
				except:
					subscribers=None
				finally:
					videos=None
					try:
						videos = result.find_element_by_id('video-count').text
					except:
						videos=None
					finally:
						description=None
						try:
							description = result.find_element_by_id('description').text
						except:
							description=None
						finally:
							link=None
							try:
								link=result.find_element_by_css_selector('a').get_attribute('href')
							except:
								link=None
							finally:
								new = ((name,subscribers,videos,description,sub_cat,link))
								if(subscribers!=None and name!=None):
									try:
										tempp1=subscribers.split(' ')
										tempp2=tempp1[0]
										tempp3=tempp2[-1]
										tempp4=float(tempp2[:-1])
										if(tempp3=='K' and tempp4>=100):
											total.append(new)
										if(tempp3=='M' and tempp4<=5):
											total.append(new)
									except:
										new=None
	df = pd.DataFrame(total,columns=['NAME','SUBSCRIBERS','VIDEOS','DESCRIPTION','SUB-CATEGORY','LINK'])
	df=df.set_index('NAME')
	df = df.loc[~df.index.duplicated(keep='first')]
	df.to_excel(writer,sheet_name=category)
writer.save()
driver.close()