#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
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

    # proxy={'host':'localhost', 'port':80,
    #        'user': 'guandong', 'password': 'password'}
    def __init__(self, proxy=None):
        self.logger = log.logger
        self.proxy = proxy
        self.session = requests.Session()
        if self.proxy is not None:
            if self.proxy.get('user', None) is None:
                proxy_str = '{{"http":"http://{host}:{port}","https":"http://{host}:{port}"}}'
            else:
                proxy_str = '{{"http":"http://{user}:{password}@{host}:{port}","https":"http://{user}:{password}@{host}:{port}"}}'
            self.logger.info(proxy_str.format(**self.proxy))
            self.session.proxies = json.loads(proxy_str.format(**self.proxy))
        self.session.headers.update(HUMAN_HEADERS)
        self.logger.info("Browser inited.")

    @property
    def browser(self):
        if getattr(self, '_browser', None) is None:
            if self.proxy is None:
                browser = webdriver.PhantomJS()
            else:
                proxy_str = ('--proxy=https://{host}:{port},--proxy-type=http,'
                    '--ssl-protocol=any,--ignore-ssl-errors=true')
                if self.proxy.get('user', None) is not None:
                    proxy_str += ',--proxy-auth={user}:{password}',
                proxy_args = proxy_str.format(**self.proxy).split(',')
                browser = webdriver.PhantomJS(service_args=proxy_args)
            browser.set_page_load_timeout(50)
            browser.set_script_timeout(10)
            self._browser = browser
        return self._browser

    def close(self):
        self.browser.quit()

    def get_current_cookie_str(self):
        cookies = self.browser.get_cookies()
        return '; '.join(['%s=%s' % (item['name'], item['value'])
                        for item in cookies])

    def refresh_browser_headers(self):
	    self.session.headers.update({'Cookie': self.get_current_cookie_str()})

