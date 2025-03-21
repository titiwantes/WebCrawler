import urllib.parse
import api.models.crawl_task as crawl_mdl
import api.crud.page_crud as page_crud
import api.services.page_services as page_srv
import db.sessions as db
import requests
import bs4
import urllib
import logging
import validators

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


class Crawler:
    def __init__(self, dbs, task_id: int, urls: set[str] = set()):
        if len(urls) == 0:
            raise ValueError("No urls to crawl")
        self.urls_to_crawl: set[tuple[str, int | None]] = {(url, None) for url in urls}
        self.dbs = dbs
        self.page_service = page_srv.PageService(dbs=self.dbs)
        self.reader, self.writer = dbs
        self.visited_urls = set(page_crud.PageCrud.get_all_urls(self.reader))
        self.task_id = task_id

    def download_url(self, url):
        return requests.get(url).text

    def get_links(self, url, html):
        soup = bs4.BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a"):
            path = link.get("href")

            if not validators.url(path):
                continue
            if path and path.startswith("/"):
                path = urllib.parse.urljoin(url, path)

            yield path

    def crawl(self, url_to_crawl):
        url, from_ = url_to_crawl

        html = self.download_url(url)
        title, content = self.parse(html)
        page_id = self.page_service.create_from_scrapping(url, title, content)

        if from_:
            self.page_service.add_link(from_page_id=from_, to_page_id=page_id)

        for link in self.get_links(url, html):
            self.page_service.add_incoming_link(link)

            if link not in self.visited_urls:
                self.urls_to_crawl.add((link, page_id))

    def parse(self, html):
        soup = bs4.BeautifulSoup(html, "html.parser")
        title = soup.find("title")
        content = soup.find("body")

        title = title.text if title else str()
        content = content.text if content else str()

        return title, content

    def run(self):
        while self.urls_to_crawl:
            url_to_crawl = self.urls_to_crawl.pop()
            url, _ = url_to_crawl

            if url in self.visited_urls:
                continue
            try:
                self.crawl(url_to_crawl)

            except Exception as e:
                logging.error(f"Failed to crawl {url}: {e}")

            finally:
                self.visited_urls.add(url)
