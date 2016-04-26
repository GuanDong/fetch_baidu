#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from selenium import webdriver
from utils import log

HUMAN_HEADERS = {
    'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
               'image/webp,*/*;q=0.8'),
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
             'like Gecko) Chrome/32.0.1700.76 Safari/537.36'),
    'Accept-Encoding': 'gzip,deflate,sdch'
}

class Browser(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS()
        self.browser.set_page_load_timeout(50)
        self.browser.set_script_timeout(10)
        self.headers = copy.deepcopy(HUMAN_HEADERS)
        self.logger = log.logger
        self.logger.info("Browser inited.")

    def close(self):
        self.browser.quit()

    def get_current_cookie_str(self):
        cookies = self.browser.get_cookies()
        return '; '.join(['%s=%s' % (item['name'], item['value'])
                        for item in cookies])

    def refresh_browser_headers(self):
	    self.headers.update({'Cookie': self.get_current_cookie_str()})

