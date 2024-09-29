from queue import Queue
from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import uni_list
from threading import Thread
import json

def page_loader(page, url, selector):
     while True:
            while True:
                status = page.goto(url).status
                if(status == 200): break
            try:
                page.wait_for_selector(selector, timeout=10000)
                break
            except PlaywrightTimeoutError:
                print("Selector not found, trying again...\n")


def get_scholar_links(u_link, result_queue):
    main_page = "https://akademik.yok.gov.tr"
    container = list()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page_loader(page, u_link, ".list-group-item-info")
        tree = HTMLParser(page.inner_html("body"))
        university_name = tree.css_first(".list-group-item-info.active").css_first("span").text()

        while True:
            pagination = tree.css_first("ul.pagination")
            next_page_node = pagination.css_first("li.active + li")
            scholar_nodes = tree.css("#authorlistTb tr td:nth-child(3)")

            for node in scholar_nodes:
                link = main_page + node.css_first("h4 > a").attributes["href"]
                container.append(link)

            if(next_page_node == None): break
            else: 
                target_page = main_page + next_page_node.css_first("a").attributes["href"]
                page_loader(page, target_page, ".img-circle")
                tree = HTMLParser(page.inner_html("body"))
            
        page.close()
        browser.close()
    print(university_name, len(container))
    result_queue.put({"u_name": university_name, "scholar_links": container})


if __name__ == "__main__":
    u_links = uni_list.get_university_links()
    u_scholarslist = [None for _ in range(len(u_links))]
    result_queue = Queue()
    threads = list()

    for i in range(len(u_links)):
        threads.append(Thread(target=get_scholar_links, args=(u_links[i],result_queue,)))
            
    batch_size = 52
    for i in range(0, len(threads), batch_size):
        for thread in threads[i:i+batch_size]:
            thread.start()
        for thread in threads[i:i+batch_size]:
            thread.join()

    for i in range(len(u_scholarslist)):
        u_scholarslist[i] = result_queue.get()

    out_file = open("links_updated.json", "w", encoding="utf-8")
    json.dump(u_scholarslist, out_file, indent=4, ensure_ascii="False")