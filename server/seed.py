import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import db,Product
from app import app

rows = []

# Kilimall Kenya
kilimall_url = "https://www.kilimall.co.ke/search-result?keyword=wacth&source=search|enterSearch|wacth"

# Alibaba
alibaba_url = "https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.the-new-header_fy23_pc_search_bar.keydown__Enter&tab=all&SearchText=mac+laptop+computer"

# Shopit
shopit_url = "https://shopit.co.ke/?match=all&subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q=phone&dispatch=products.search&security_hash=8eb5027cd936a66cb2edaa8c500b6e36"

# Initialize Firefox WebDriver
driver = webdriver.Firefox()

# Initialize list to store scraped data
scraped_data = []

# Scraping Kilimall
driver.get(kilimall_url)
wait = WebDriverWait(driver, 10)
kilimall_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.product-item')))

for link in kilimall_links:
    scraped_data.append(link.text.split('\n'))

# Scraping Alibaba
driver.get(alibaba_url)
wait = WebDriverWait(driver, 10)
alibaba_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.fy23-search-card')))

for link in alibaba_links:
    scraped_data.append(link.text.split('\n'))

# Scraping Shopit
driver.get(shopit_url)
wait = WebDriverWait(driver, 10)
shopit_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.ut2-gl__body')))

for link in shopit_links:
    scraped_data.append(link.text.split('\n'))

# Quit the WebDriver
driver.quit()

# Writing scraped data to CSV file

with open("scraped_data.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)
print(header)
print(rows)

with app.app_context():
    
    print('Deleting ...')
    
    Product.query.delete()

    for item in rows:
        product = Product(
            name=item[0],
            price=item[1],
            rating=item[2],
            image_url=item[3]
        
        )
        db.session.add(product)
        db.session.commit()


