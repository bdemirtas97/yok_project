from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright

def get_universities():
    with sync_playwright() as p:
        url = "https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp"
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        tree = HTMLParser(page.inner_html("body"))

        name_tags = tree.css(".searchable > tr > td:nth-child(1) > a")
        category_tags = tree.css(".searchable > tr > td:nth-child(3)")
        date_tags = tree.css(".searchable > tr > td:nth-child(4)")
        university_tags = list(zip(name_tags, category_tags, date_tags))
        universities = [(university[0].text(strip=True), university[1].text(strip=True), university[2].text(strip=True)) for university in university_tags]

        browser.close()
        return universities