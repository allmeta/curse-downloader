import sys
import time
import os
from pathlib import Path
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def download_addon(driver, addon):
    driver.get(f"https://www.curseforge.com/wow/addons/{addon}/download")

    if driver.title == "Not found - CurseForge":
        print(f"<{addon}> Not found ")
        return False
    if driver.title == "Just a moment...":
        print("cloudflare shit D:")
        return False

    url = driver.find_element(By.CSS_SELECTOR, "a.alink.underline").get_attribute('href')
    driver.get(url)


    print(f"<{addon}> Downloading...")
    return True


addons = len(sys.argv) > 1 and sys.argv[1]
ddir = len(sys.argv) > 2 and sys.argv[2]

if not addons or not ddir:
    print("Usage: curse-downloader.py \"list of addons\" download-dir")
    sys.exit(1)

try:
    ddir = Path(ddir).resolve(strict=True)
except Exception as e:
    print(e)
    sys.exit(1)


shutil.rmtree(ddir)
os.mkdir(ddir)

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_experimental_option(
    "prefs",
    {
        "profile.managed_default_content_settings.javascript": 2,
        "download.prompt_for_download": False,
        "download.default_directory": str(ddir)
    }
)

driver = webdriver.Chrome(options=chrome_options)

succeeded_addons = []
for addon in addons.split(" "):
    if download_addon(driver, addon):
        succeeded_addons.append(addon)

driver.quit()

if len(succeeded_addons) == 0:
    sys.exit(1)
while len(list(ddir.glob("*.zip"))) != len(succeeded_addons):
    time.sleep(0.1)

sys.exit(0)
