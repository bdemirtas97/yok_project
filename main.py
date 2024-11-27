from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import utilities
import db_handler
import psycopg2
import json

def page_loader(page, url, selector):
    for i in range(5):
            while True:
                status = page.goto(url).status
                if(status == 200): break
            if not(HTMLParser(page.inner_html("body")).css_first(".logo")): continue
            try:
                page.wait_for_selector(selector, timeout=4000)
                return True
            except PlaywrightTimeoutError:
                print("Selector not found, trying again...\n")
    return False

def create_scholar(page, url, university_name):
    if not (page_loader(page, url, "#authorlistTb")): return None
    tree = HTMLParser(page.inner_html("body"))

    main_page_link = "https://akademik.yok.gov.tr"
    tabs = [main_page_link + tag.attributes["href"] for tag in tree.css(".nav-pills.nav-stacked > [id] > a")[1:]]

    scholar = dict()
    scholar["university"] = university_name

    utilities.get_personal_info(tree, scholar)
    print(scholar["name"])
    page_loader(page, tabs[0], "span.label.kitap")
    utilities.get_books(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[1], "#makaleTab")
    utilities.get_articles(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[2], "#makaleTab")
    utilities.get_papers(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[3], ".col-lg-6.col-md-6.col-sm-10.col-xs-12")
    utilities.get_projects(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[4], ".col-lg-6.col-md-6.col-sm-10.col-xs-12")
    utilities.get_lectures(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[5], ".col-lg-6.col-md-6.col-sm-10.col-xs-12")
    utilities.get_supervised_thesises(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[6], "span.label.kitap")
    utilities.get_rewards(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[7], "span.label.kitap")
    utilities.get_patents(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[8], "span.label.kitap")
    utilities.get_memberships(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[9], "span.label.kitap")
    utilities.get_artistic_activities(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[10], ".col-lg-6.col-md-6.col-sm-10.col-xs-12")
    utilities.get_administrative_duties(HTMLParser(page.inner_html("body")), scholar)
    page_loader(page, tabs[11], "span.label.kitap")
    utilities.get_non_college_experience(HTMLParser(page.inner_html("body")), scholar)
    return scholar


if __name__ == "__main__":
    u_scholarslist = json.load(open("links_updated.json", "r"))
    db_handler.create_tables()
    for i in range(151, len(u_scholarslist)):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            start = 0
            for j in range(start, len(u_scholarslist[i]["scholar_links"])):
                start = time.time()
                scholar = create_scholar(page, u_scholarslist[i]["scholar_links"][j], u_scholarslist[i]["u_name"])
                if(scholar):
                    try:
                        db_handler.insert_scholar(scholar)
                    except psycopg2.Error as e:
                        print(e.diag.message_primary)
                print(time.time() - start)
            browser.close()
