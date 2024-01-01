from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars"

# Webdriver
browser = webdriver.Chrome("")
browser.get(START_URL)

time.sleep(10)
scraped_data = []

def scrape():
    while True:
        for i in range(1,2):
            print(f'Scrapping page {i+1} ...' )
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            
            if current_page_num < i:
               browser.find_element(By.XPATH, value='//*[@id="mw-content-text"]/div[1]/table[4]').click()
            elif current_page_num > i:
               browser.find_element(By.XPATH, value='//*[@id="mw-content-text"]/div[1]/table[4]').click()
            else:
                break
            
            for bright_star_table in soup.find_all("ul", attrs={"class", "wikitable"}):
                table_body = bright_star_table.find_all("tbody")
                table_rows = table_body.find_all("tr")
                temp_list = []
                
                for row in table_rows:
                    table_cols = row.find_all('td')
                    temp_list = []
                    
                    for col_data in table_cols:
                        data = col_data.text.strip()
                        temp_list.append(data)
                        
                    scraped_data.append(temp_list)
                
stars_data = []

for i in range(0,len(scraped_data)):
    Star_Names = scraped_data[i][1]
    Distance = scraped_data[i][3]
    Mass = scraped_data[i][5]
    Radius = scraped_data[i][6]
    Lum = scraped_data[i][7]
    
    required_data = [Star_Names, Distance, Mass, Radius, Lum]
    stars_data.append(required_data)
    
    hyperlink_li_tag = required_data[0]
            
    required_data.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
    browser.find_element(by=By.XPATH, value='//*[@id="mw-content-text"]/div[1]/table[4]').click()
    print(f"Page {i} scraping completed")
    
# Calling Method    
scrape()

# Define Header
headers = ["Star_Name", "Distance", "Mass", "Radius", "Luminosity"]

# Define pandas DataFrame   
star_df_1 = pd.DataFrame(stars_data, columns=headers)

# Convert to CSV
star_df_1.to_csv('scraped_data.csv',index=True, index_label="id")