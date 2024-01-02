from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv  # CSV işlemleri için modülü içe aktar

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.trendyol.com/sr?wc=114&os=1&sk=1&pi=7")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  

# CSV dosyasını aç ve bir yazıcı nesnesi oluştur
with open('urunler.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # CSV dosyasının başlığını yaz
    writer.writerow(['Ürün Adı', 'Fiyat', 'Link', 'Özellikler'])

    try:
        # Ürün kartlarını bul
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-card-wrppr"))
        )
        products = driver.find_elements(By.CSS_SELECTOR, "div.p-card-wrppr")
        print("Toplam {} ürün bulundu.".format(len(products)))

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
                feature_value_elements = item.find_elements(By.CSS_SELECTOR, "b")
                if feature_value_elements:
                    feature_value = feature_value_elements[0].text
                    feature_list[feature_name] = feature_value

            # CSV dosyasına yaz
            writer.writerow([title, price, detail_link, feature_list])
            #boşluk bırak her ürün arasında
            writer.writerow([])
            print("{}. ürün eklendi".format(index + 1))

            # Detay sekmesini kapat ve ana sayfaya geri dön
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Çok fazla istek göndermemek için bekle
            time.sleep(1)

    except Exception as e:
        print("Bir hata oluştu:", e)

    driver.quit()


