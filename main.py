from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

# --- Setup Chrome ---
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.olx.in/spare-parts_c1585/q-car-cover")

wait = WebDriverWait(driver, 15)
time.sleep(3)  # wait for page to load properly

# --- Find all ads in the list ---
ul = driver.find_element(By.XPATH, '//*[@id="main_content"]/div/div/section/div/div/div[4]/div[2]/div/div[2]/ul')
lis = ul.find_elements(By.TAG_NAME, "li")

# --- Set how many ads you want to scrape ---
MAX_ADS = 28  # change this number here if you want more/less ads

ad_links = []
for li in lis[:MAX_ADS]:
    try:
        a = li.find_element(By.TAG_NAME, "a")
        href = a.get_attribute("href")
        if href:
            ad_links.append(href)
    except:
        pass

print("Found links:", len(ad_links))

# --- Loop through each ad and get details ---
results = []
for link in ad_links:
    driver.get(link)
    time.sleep(2)  # wait for ad page to load
    try:
        title = driver.find_element(By.CSS_SELECTOR, "h1[data-aut-id='itemTitle']").text
        if "car cover" not in title.lower():  # filter only car cover ads
            continue
        price = driver.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemPrice']").text
        desc = driver.find_element(By.CSS_SELECTOR, "div[data-aut-id='itemDescriptionContent']").text

        results.append([title, price, desc])
    except:
        print("Error reading ad:", link)
        continue

# --- Print results ---
print(tabulate(results, headers=["Title", "Price", "Description"], tablefmt="grid"))

driver.quit()

# --- Save results to Excel ---
if results:
    df = pd.DataFrame(results, columns=["Title", "Price", "Description"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"OLX_CarCovers_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")
else:
    print("No results to save.")
