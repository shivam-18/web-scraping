from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
place_name="bangalore"
categories={
	"Dance":["Western Dance Academy","Classical Dance Academy","Bollywood Dance Academy","Zumba Academy","Bhangra Academy","Western Dance teachers","Classical Dance Teachers", "Bollywood Dance Teachers", "Zumba Teachers", "Bhangra Teachers"],
	"Foreign Languages":["Learn French", "Learn German", "Learn English", "French Tutors", "German Tutors", "English Tutors"],
	"Story Time":["Story Tellers", "Story Telling Festival"],
	"Singing":["Singing Academy", "Singing Tutors"],
	"Yoga":["Yoga Academy", "Yoga Instructors"],
	"Chess":["Chess Academy", "Learn Chess"]
}
webdriver = "/home/shivam/chromedriver"
driver = Chrome(webdriver)
writer = pd.ExcelWriter('Youtube_'+place_name+'.xlsx', engine='xlsxwriter')
for category in categories:
	total = []
	for sub_cat in categories[category]:
		sub_cat1=sub_cat.replace(' ','+')
		url = "https://www.youtube.com/results?search_query="+sub_cat1+"+"+place_name+"+india"+"&sp=EgIQAg%253D%253D"
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