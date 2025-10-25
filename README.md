# OLX Car Cover Scraper

This is a simple Python script to scrape **car cover ads** from OLX India.  
It collects the **title, price, and description** of the first 12 car cover listings from the search results.

---

## Features

- Scrapes only **car cover ads**.
- Collects **title, price, and description** for each ad.
- Uses **Selenium** with `webdriver_manager` for automatic ChromeDriver setup.
- Prints results in a **table format** using `tabulate`.
- Simple and easy-to-understand code.
  
## Configurables
- MaxAds = 28  # change this number if you want more or fewer ads


---

## Requirements

- Python 3.8+
- Google Chrome installed
- Packages:

```bash
pip install selenium webdriver-manager tabulate
