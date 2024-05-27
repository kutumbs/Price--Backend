import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from model import db,Product
from app import app

rows = []

# Kilimall Kenya
kilimall_url = "https://www.kilimall.co.ke/search-result?keyword=wacth&source=search|enterSearch|wacth"

# Alibaba
# alibaba_url = "https://ovostore.co.ke/products/search"

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
    kilImg = link.find_element(By.CLASS_NAME,'product-image')
    kilimall_images = kilImg.find_element(By.CSS_SELECTOR, '.product-item .product-image img')
    print(kilimall_images, "Image element")
    driver.implicitly_wait(11)
    print(kilimall_images.get_attribute('src'), "The Actual Image Link")
    image_link = kilimall_images.get_attribute('src')or "google.com"
    scraped_data.append(link.text.split('\n')+ image_link.split('\n'))
    
    
    # if image_link:
    #     scraped_data.append(kilimall_images.get_attribute('src').split('\n'))
    # else:
    #     scraped_data.append("google.com".split('\n'))

# Scraping Alibaba
# driver.get(alibaba_url)
# wait = WebDriverWait(driver, 10)
# alibaba_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.grid-product__wrap-inner')))

# for link in alibaba_links:
#     aliImg = link.find_element(By.CLASS_NAME,'grid-product__shadow ec-text-muted')
#     alibaba_images = aliImg.find_element(By.CSS_SELECTOR, '.grid-product__wrap-inner.grid-product__shadow ec-text-muted img')
#     driver.implicitly_wait(3)
#     print(alibaba_images.get_attribute('src'), "The Actual Image Link")
#     image_link = alibaba_images.get_attribute('src')or "google.com"
#     scraped_data.append(link.text.split('\n')+ image_link.split('\n'))



# Scraping Shopit
driver.get(shopit_url)
wait = WebDriverWait(driver, 10)
shopit_links = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.ut2-gl__item ')))

for link in shopit_links:
    shopImg = link.find_element(By.CLASS_NAME,'ut2-gl__image')
    shopi_images = shopImg.find_element(By.CSS_SELECTOR, '.ut2-gl__item .ut2-gl__image img')
    print(shopi_images, "Image element")
    driver.implicitly_wait(30)
    print(shopi_images.get_attribute('src'), "The Actual Image Link")
    image_link = shopi_images.get_attribute('src')or "google.com"
    scraped_data.append(link.text.split('\n')+ image_link.split('\n'))
    

# Quit the WebDriver
driver.quit()

# Writing scraped data to CSV file
with open("scraped_data.csv", 'w', newline='') as file:
    csvwriter = csv.writer(file)
    header = ['Name', 'Price', 'Rating', 'Image URL','image_link']
    csvwriter.writerow(header)
    csvwriter.writerows(scraped_data)



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


