from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.trendyol.com/sr?wc=114&os=1&sk=1")

time.sleep(5)  # Dinamik içerik yüklendiğinde yeterli zaman sağlamak için

try:
    # Ürün kartlarını bul
    products = driver.find_elements(By.CSS_SELECTOR, "div.p-card-wrppr")

    for index, product in enumerate(products):
        # Ürün adını ve fiyatını bul
        title = product.find_element(By.CSS_SELECTOR, "span.prdct-desc-cntnr-ttl").text
        price = product.find_element(By.CSS_SELECTOR, "div.prc-box-dscntd").text

        # Ürün detay linkini bul
        detail_link = product.find_element(By.CSS_SELECTOR, "a").get_attribute('href')

        # Yeni sekmede detay linkini aç
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(detail_link)

        time.sleep(3)  # Detay sayfasının yüklenmesini bekleyin

        # Detay sayfasından bilgileri çek (örnek olarak ürün özelliklerini alalım)

        print(f"Ürün Adı: {title} - Fiyat: {price} - Link: {detail_link}")

        # Detay sekmesini kapat ve ana sayfaya geri dön
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Çok fazla istek göndermemek için bekle
        time.sleep(1)

except Exception as e:
    print("Bir hata oluştu:", e)

driver.quit()
