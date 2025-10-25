from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Setup Chrome WebDriver ---
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.olx.in/items/q-car-cover?isSearchCall=true")

wait = WebDriverWait(driver, 10)

# --- Wait for the <ul> container ---
wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="main_content"]/div/div/section/div/div/div[4]/div[2]/div/div[2]/ul')
))

# --- Get <li> elements ---
ad_lis = driver.find_elements(By.XPATH, '//*[@id="main_content"]/div/div/section/div/div/div[4]/div[2]/div/div[2]/ul/li')

# --- Extract first 12 ad links ---
ad_links = []
MaxAds=28
for li in ad_lis[:MaxAds]:
    try:
        a_tag = li.find_element(By.TAG_NAME, "a")
        href = a_tag.get_attribute("href")
        if href:
            ad_links.append(href)
    except:
        continue

print(f"Found {len(ad_links)} ad links")

results = []

# --- Loop through ad links and filter for "car cover" ---
for link in ad_links:
    driver.get(link)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[data-aut-id='itemTitle']")))
        title = driver.find_element(By.CSS_SELECTOR, "h1[data-aut-id='itemTitle']").text
        if "car cover" not in title.lower():  # filter
            continue
        price = driver.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemPrice']").text
        desc = driver.find_element(By.CSS_SELECTOR, "div[data-aut-id='itemDescriptionContent']").text

        results.append([title, price, desc])

    except Exception as e:
        print(f"Error on {link}: {e}")

# --- Print results ---
print(tabulate(results, headers=["Title", "Price", "Description"], tablefmt="grid"))

driver.quit()
