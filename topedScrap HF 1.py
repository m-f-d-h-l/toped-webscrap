from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime

url = input("Masukkan url toko dengan link www.tokopedia.com/nama_toko/product?perpage=40 : ")
JumlahPage = input("Masukkan jumlah halaman yang ingin diambil: ")

if url :

    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome()
    driver.get(url)

    data= []
    for i in range(0, int(JumlahPage)-1):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('div', attrs={'class': 'gG1uA844gIiB2+C3QWiaKA=='})

        for container in containers:
            try:
                product_name_span = container.find('span', class_='+tnoqZhn89+NHUA43BpiJg==')
                product_name = product_name_span.get_text() if product_name_span else "N/A"
                    
                price_span = container.find('div', class_='urMOIDHH7I0Iy1Dv2oFaNw==')
                price = price_span.get_text() if price_span else "N/A"
                cleaned_price = price.replace("Rp", "").replace(".", "")

                items_sold_span = container.find('span', class_='u6SfjDD2WiBlNW7zHmzRhQ==')
                items_sold = items_sold_span.get_text() if items_sold_span else "N/A"
                cleaned_sold = items_sold.replace(" terjual", "")
                #print(product_name, " * ", cleaned_price, " * ", cleaned_sold)
                data.append ((product_name, cleaned_price, cleaned_sold))
            except AttributeError:
                StopIteration
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'a[data-testid="btnShopProductPageNext"].css-buross').click()
        time.sleep(4)  # Wait for the next page to load
    df = pd.DataFrame(data, columns=['Produk', 'Harga (Rp)', 'Terjual'])
    filename = f"data_scrap_HF_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    df.to_csv('data_scrap_HF',datetime.now().strftime("%Y%m%d_%H%M%S"),'.csv', index=False)
