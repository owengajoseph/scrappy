from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time

# ------- Configuration ---------
START_URL = "https://peopledaily.digital/"
OUTPUT_CSV = "/home/user/webscraping/scraps/scraped_data.csv6"
MAX_LINKS = 10   # limit to avoid infinite crawling
# -------------------------------

options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()), options=options
)

def scrape_page(url):
    """Scrapes one page and returns list of dicts"""
    scraped_data = []
    try:
        driver.get(url)
        time.sleep(3)

        tags_to_scrape = [
            "a", "img", "p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "div", "li"
        ]

        for tag in tags_to_scrape:
            elements = driver.find_elements(By.TAG_NAME, tag)
            for el in elements:
                entry = {"url": url, "tag": tag}
                if tag == "a":
                    entry["text"] = el.text.strip()
                    entry["attribute"] = el.get_attribute("href")
                elif tag == "img":
                    entry["text"] = el.get_attribute("alt") or ""
                    entry["attribute"] = el.get_attribute("src")
                else:
                    entry["text"] = el.text.strip()
                    entry["attribute"] = ""

                if entry["text"] or entry["attribute"]:
                    scraped_data.append(entry)
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
    return scraped_data

try:
    # Step 1: scrape the start page
    all_data = []
    all_data.extend(scrape_page(START_URL))

    # Step 2: collect links from the first page
    links = [el["attribute"] for el in all_data if el["tag"] == "a" and el["attribute"]]
    visited = set()

    # Step 3: visit each link (limit to MAX_LINKS)
    for link in links[:MAX_LINKS]:
        if link.startswith("http") and link not in visited:
            visited.add(link)
            print(f"🔗 Visiting {link}")
            all_data.extend(scrape_page(link))

    # Step 4: save all data to CSV
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"✅ Data saved to {OUTPUT_CSV}")

finally:
    driver.quit()
