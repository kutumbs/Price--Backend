from bs4 import BeautifulSoup
import requests
import pandas as pd


current_page = 1

data = []

proceed = True

while(proceed):
    print('Currently scraping page: '+str(current_page)) 
    
    url = 'https://nairobicomputershop.co.ke/catalogue/category/laptops/?sort_by=popularity&items_per_page=20&page='+str(current_page)+''

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')


    if soup.title.text == '404 Not Found':
        proceed = False
    else:
        all_laptops = soup.find_all('div', class_='product-list row')
        
        for laptop in all_laptops:
            iteam = {}

            
            iteam['Image'] = laptop.find_all('div', class_='product-card-img-container')
            
            iteam['Title'] = laptop.find_all('h5', class_='card-title product-card-name')

            iteam['Price'] = laptop.find_all('span', class_='stockrecord-price-current')

            iteam['Link'] = laptop.find_all('div', class_='card product-card')

            data.append(iteam)
            # proceed = False
            
            # print(iteam['Image'])
            # print(iteam['Title'])
            # print(iteam['Price'])
            # print(iteam['Link'])

           
        
        
    current_page 
    proceed = False
    

df = pd.DataFrame(data)
df.to_csv('csv')


