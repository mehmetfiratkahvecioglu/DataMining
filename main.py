from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.trendyol.com/sr?wc=114&os=1&sk=1")

try:
    # Ürün kartlarını bul
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-card-wrppr"))
    )
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

        # Detay sayfasının yüklenmesini bekleyin
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.detail-attr-container li.detail-attr-item"))
        )
        feature_items = driver.find_elements(By.CSS_SELECTOR, "ul.detail-attr-container li.detail-attr-item")

        feature_list = {}
        for item in feature_items:
            feature_name = item.find_element(By.CSS_SELECTOR, "span").text
            # 'b' etiketinin varlığını kontrol edin ve ona göre değer alın
            feature_value_elements = item.find_elements(By.CSS_SELECTOR, "b")
            if feature_value_elements:
                feature_value = feature_value_elements[0].text
                feature_list[feature_name] = feature_value

        print(f"Ürün Adı: {title} - Fiyat: {price} - Link: {detail_link} - Özellikler: {feature_list}")

        # Detay sekmesini kapat ve ana sayfaya geri dön
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Çok fazla istek göndermemek için bekle
        time.sleep(1)

except Exception as e:
    print("Bir hata oluştu:", e)

driver.quit()
