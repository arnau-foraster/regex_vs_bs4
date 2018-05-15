# -*- coding: utf-8 -*-
import bs4
import re
import timeit
import utils


class BaseCrawler(object):
    def __init__(self, page):
        self.page = page

    def get_extra_info_patterns(self):
        raise NotImplementedError()

    def extract(self):
        raise NotImplementedError()


class DummyRegexCrawler(BaseCrawler):
    def get_extra_info_patterns(self) -> dict:
        """Return regex based extra_info patterns."""
        return {
            'title': re.compile(r'<h1 class="title-link">(.*?)</h1>'),
            'postingDate': re.compile(r'date:</strong>\s*?(.+)</div>'),
            'postingUser': re.compile(r'posted by:\s*?</strong>\s*?<a href=".*?">(.*)</a>'),
            'postingUserUrl': re.compile(r'posted by:\s*?</strong>\s*?<a href="(.*?)">'),
        }

    def extract(self):
        results = []
        for key, pattern in self.get_extra_info_patterns().items():
            data = pattern.search(self.page)
            if data:
                results.append(data.group(0))
        return results


class DummyBs4Crawler(BaseCrawler):
    def get_extra_info_patterns(self) -> dict:
        return {
            'title': self.page.find('h1', class_='title-link'),
            'postingDate': self.page.find('div', class_='post-date'),
            'postingUser': self.page.find('div', class_='author'),
            'postingUserUrl': self.page.find('div', class_='author').find('a').get('href'),
        }

    def extract(self):
        results = []
        for key, pattern in self.get_extra_info_patterns().items():
            if pattern:
                results.append(pattern)
        return results


def performance_test(crawler):
    results = crawler.extract()

    assert len(results) == 4

    return results


if __name__ == '__main__':
    # https://avxhm.se/music/Monty_Python_Soundtracks_Collection.html
    some_page = utils.load_html('page.html').lower()
    regex_crawler = DummyRegexCrawler(some_page)

    soup = bs4.BeautifulSoup(some_page, 'lxml')
    bs4_crawler = DummyBs4Crawler(soup)

    print(timeit.timeit('performance_test(regex_crawler)', number=100, globals=globals()))
    print(timeit.timeit('performance_test(bs4_crawler)', number=100, globals=globals()))

    assert performance_test(regex_crawler) == performance_test(bs4_crawler)
