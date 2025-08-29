from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time

# ------- Configuration ---------
URLS = [
    " https://peopledaily.digital/inside-politics/salasya-to-ruto-silence-on-hospital-collapse-kills-your-war-on-corruption",
    "https://peopledaily.digital/news/mudavadi-demands-answers-over-millions-in-questionable-claims-at-mumias-hospital",
    "https://peopledaily.digital/inside-politics/salasya-to-ruto-silence-on-hospital-collapse-kills-your-war-on-corruption",
    "https://peopledaily.digital/sports/mbadi-clarifies-source-of-funds-for-rutos-incentives-to-harambee-stars",
    "https://peopledaily.digital/inside-politics/natembeya-urges-fresh-leadership-says-wetangula-and-mudavadi-belong-to-old-guard-of-kenyan-politics",
    "https://peopledaily.digital/inside-politics/wavinya-ndeti-condemns-attack-on-kalonzo-calls-out-political-intolerance",
    "https://peopledaily.digital/inside-politics/kericho-impeachment-drama-sen-cherargei-threatens-mca-with-arrest",
    "https://peopledaily.digital/sports/chan-3rd-place-playoff-the-millions-senegal-will-bag-if-they-beat-sudan-today",
]  # 👈 Add more links here

OUTPUT_CSV = "/home/user/webscraping/scraps/scraped_data.csv"
# -------------------------------

options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()), options=options
)

data = []

try:
    for url in URLS:
        print(f"🔗 Scraping: {url}")
        driver.get(url)
        time.sleep(3)

        tags_to_scrape = [
            "a",
            "img",
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "span",
            "div",
            "li",
        ]

        for tag in tags_to_scrape:
            elements = driver.find_elements(By.TAG_NAME, tag)
            for el in elements:
                entry = {"url": url, "tag": tag}  # 👈 add url column

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
                    data.append(entry)

    # Save once after all URLs are scraped
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"✅ Data saved to {OUTPUT_CSV}")

finally:
    driver.quit()
