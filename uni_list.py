from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright

def get_university_links():
    with sync_playwright() as p:
        url = "https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp"
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        tree = HTMLParser(page.inner_html("body"))

        link_tags = tree.css(".searchable > tr > td:nth-child(1) > a")
        links = ["https://akademik.yok.gov.tr" + tag.attributes["href"] for tag in link_tags]

        browser.close()
        return links