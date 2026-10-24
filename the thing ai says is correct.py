import re
from urllib.parse import quote
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

print("Paste your heat sheet below.")
print("When you are done, type 'END' on a new line.")

lines = []

while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

heatsheetdump = "\n".join(lines)

athletes = []

for line in heatsheetdump.strip().splitlines():
    match = re.match(r"^(.*?)\s+(\d{1,2})\s+(.+)$", line.strip())
    if match:
        name = match.group(1).strip()
        school = match.group(3).strip()
        athletes.append((name, school))

if not athletes:
    print("No athletes found. Check the heat sheet format.")
    input("Press Enter to exit...")
    raise SystemExit

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    for name, school in athletes:
        query = quote(f"{unquote(name)} {school}")
        

        driver.get(f"https://www.athletic.net/Search.aspx#?q={query}")
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            if f"{(name.replace(',', ' '))}" in link.text:
                link.click()
        break

        input("Review this page in Chrome, then press Enter for the next athlete...")

    input("All athletes processed. Press Enter to close Chrome.")

finally:
    driver.quit()