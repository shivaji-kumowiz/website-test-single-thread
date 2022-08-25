from selenium import webdriver
import logging
import time


class WebsiteSelenium:
    def __init__(self, url):
        self.url = url
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.headless = True
        self.driver = webdriver.Firefox(options=firefox_options)

    def get_page_urls(self):
        self.driver.get(self.url)
        urls_set = set()
        for a in self.driver.find_elements("xpath", ".//a"):
            if (
                a.get_attribute("href") is not None
                and "http" in a.get_attribute("href")
                and "dgraph.io" in a.get_attribute("href")
                and "github" not in a.get_attribute("href")
                and "zip" not in a.get_attribute("href")
                and "https://discuss.dgraph.io/t/" not in a.get_attribute("href")
                and "https://discuss.dgraph.io/u/" not in a.get_attribute("href")
                and "https://discuss.dgraph.io/tag/" not in a.get_attribute("href")
                and "https://discuss.dgraph.io/c/" not in a.get_attribute("href")
                and "https://discuss.dgraph.io/badges/" not in a.get_attribute("href")
                and "https://dgraph.io/docs/" not in a.get_attribute("href")
                and "https://dgraph.io/blog/post" not in a.get_attribute("href")
            ):
                urls_set.add(a.get_attribute("href"))
        return urls_set


def get_page_urls(url):
    logging.basicConfig(filename='out.log', level=logging.INFO)
    logging.info(f"\nchecking {url}")
    website_selenium_obj = WebsiteSelenium(url=url)
    try:
        urls = website_selenium_obj.get_page_urls()
        logging.info(f"page loaded ✅")
        logging.info(f"obtained {len(urls)} urls")
    except Exception as e:
        logging.info(f"page load error ❌ => {str(e)}")
        urls = set()
    website_selenium_obj.driver.close()
    return urls


def recurse_check(url):
    urls = set()
    urls.add(url)
    visited_page_urls = dict()
    while len(urls) > 0:
        url = urls.pop()
        if url in visited_page_urls and visited_page_urls[url] is True:
            continue
        else:
            tmp_urls = get_page_urls(url=url)
            visited_page_urls[url] = True
            urls.update(tmp_urls)
        logging.info(f"total pending urls count {len(urls)}")
        logging.info(f"total crawled urls count {len(visited_page_urls)}")
    return visited_page_urls


if __name__ == "__main__":
    start = time.time()
    visited_page_urls = recurse_check(url="https://www.dgraph.io")
    logging.info("\n\n**********\n\n")
    logging.info("routes:")
    for key, value in visited_page_urls.items():
        logging.info(key)
    end = time.time()
    my_logger.info("The time of execution of above program is :" + str( (end - start)/60))