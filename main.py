from selenium import webdriver
import time
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.trendyol.com/sr?wc=114&os=1&sk=1")


time.sleep(5)  # Dinamik içerik yüklendiğinde yeterli zaman sağlamak için

# Ürün bilgilerini çek
try:
    # Ürün kartlarını bul
    products = driver.find_elements(By.CSS_SELECTOR, "div.p-card-wrppr")

    for product in products:
        # Ürün adını ve fiyatını bul
        # CSS seçicileri güncellendi
        title = product.find_element(By.CSS_SELECTOR, "span.prdct-desc-cntnr-ttl").text
        price = product.find_element(By.CSS_SELECTOR, "div.prc-box-dscntd").text

        print(f"Ürün Adı: {title} - Fiyat: {price}")

except Exception as e:
    print("Bir hata oluştu:", e)

# İşiniz bittiğinde tarayıcıyı kapatın
driver.quit()