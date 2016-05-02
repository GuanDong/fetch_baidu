#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib
import re

import utils
import img_util

from .. import browser

# 登录页面URL
LOGIN_URL = ('https://passport.baidu.com/v2/?login&tpl=mn&u='
             'http%3A%2F%2Fwww.baidu.com%2F')

# 7天搜索趋势页面
ONE_WEEK_TREND_URL = {
    'TREND_PAGE': ('http://index.baidu.com/?tpl=trend&type=0'
                      '&area=0&time=12&word={word}'),
    'TREND_CHART_DATA': ('http://index.baidu.com/Interface/Search/getAllIndex/'
                 '?res={res}&res2={res2}&startdate={start_date}'
                 '&enddate={end_date}'),
    'TREND_POINT_DATA': ('http://index.baidu.com/Interface/IndexShow/show/?res='
                  '{res}&res2={res2}&classType=1&res3[]={enc_index}'
                  '&className=view-value&{t}'),
}

# 人群画像
ONE_WEEK_CROWD_URL = {
    'CROWD_PAGE': ('http://index.baidu.com/?tpl=crowd&type=0'
                      '&area=0&time=12&word={word}'),
    'CROWD_CHART_DATA': ('http://index.baidu.com/Interface/Social/getSocial/'
                 '?res={res}&res2={res2}'),
}

# 百度地图POI
POI_QUERY_URL = ('http://api.map.baidu.com/place/v2/search?q={query}&scope=1'
                 '&region={city}&city_limit=true'
                 '&page_num={page_num}&page_size=20&output=json&ak={ak}')
POI_DETAIL_URL = ('http://api.map.baidu.com/place/v2/detail?uid={uid}&scope=2'
                 '&output=json&ak={ak}')
# 航班迁移信息

# $('#grp_social_l svg text[text-anchor=middle] tspan').text()
# window.G.chart.CONFIG.ICON_AGE_TEXT
# "19岁及以下20~29岁30~39岁40~49岁50岁及以上"
# ecmpData[53]['Ct'][5301]['Nm']
# cmpDataPts.cityIDs
# ecmpDataPts.cityPts
# BID.cmapIDs.strArr
# http://index.baidu.com/Interface/Region/getRegion/?res=LHlQBVARUDUJRjURNnQWZhQNR1AUIkhENFQQBXFOPkZjXyg%2BHxonOzAwRx4zfgBbdHd0ZgBCayYjIh5cIho3WzAmcQkpZAAqU0ATaBZHCGZ3RkUNXx9nIRgIAWQII#
# http://index.baidu.com/Interface/Social/getSocial/?res=LHlQBVARUDUJRjURNnQWZhQNR1AUIkhENFQQBXFOPkZjXyg%2BHxonOzAwRx4zfgBbdHd0ZgBCayYjIh5cIho3WzAmcQkpZAAqU0ATaBZHCGZ3RkUNXx9nIRgIAWQII#

class BaiduBrowser(browser.Browser):

    def login(self, user_name, password):
        self.browser.get(LOGIN_URL)
        user_name_obj = self.browser.find_element_by_id(
            'TANGRAM__PSP_3__userName'
        )
        user_name_obj.send_keys(user_name)
        ps_obj = self.browser.find_element_by_id('TANGRAM__PSP_3__password')
        ps_obj.send_keys(password)
        sub_obj = self.browser.find_element_by_id('TANGRAM__PSP_3__submit')
        sub_obj.click()
        self.logger.info(u'请确保能够成功登陆百度，输入你的账号和密码，有验证码要手动输入一下')
        while self.browser.current_url == LOGIN_URL:
            time.sleep(1)

    def login_with_cookie(self, baidu_account, baidu_password):
        self.browser.get('https://www.baidu.com/')
        cookie_dict_list = self.cookie_dict_list
        for cookie_dict in cookie_dict_list:
            try:
                self.browser.add_cookie(cookie_dict)
            except:
                continue
        self.login(baidu_account, baidu_password)

    def fetch_an_week_trend(self, keyword):
        self.refresh_browser_headers()

        res, res2, start_date, end_date = self._trend_params(keyword)
        start, end_date, date_list = utils.get_date_info(start_date, end_date)

        enc_s = self._trend_encs(res, res2, start_date, end_date)

        trend_dict = dict()
        for i, enc in enumerate(enc_s):
            img_url, val_info = self._trend_imge_url(res, res2, enc)
            value = self._trend_value(img_url, val_info)
            trend_dict[date_list[i]] = value.replace(',', '')
        return trend_dict

    def _trend_params(self, keyword):
        page_url = ONE_WEEK_TREND_URL['TREND_PAGE'].format(
            word=urllib.quote(keyword.encode('gbk'))
        )
        self.browser.get(page_url)
        res = self.browser.execute_script('return PPval.ppt;')
        res2 = self.browser.execute_script('return PPval.res2;')
        start_date, end_date = self.browser.execute_script(
            'return BID.getParams.time()[0];'
        ).split('|')
        return res, res2, start_date, end_date

    def _trend_encs(self, res, res2, start_date, end_date):
        url = ONE_WEEK_TREND_URL['TREND_CHART_DATA'].format(
            res=res, res2=res2, start_date=start_date, end_date=end_date
        )

        r = self.session.get(url).json()
        enc_s = r['data']['all'][0]['userIndexes_enc'].split(',')
        return enc_s

    def _trend_imge_url(self, res, res2, enc):
        url = ONE_WEEK_TREND_URL['TREND_POINT_DATA'].format(
            res=res, res2=res2, enc_index=enc, t=int(time.time()) * 1000
        )
        r = self.session.get(url)
        content = r.json()['data']['code'][0]
        img_url = re.findall('(?is)"(/Interface/IndexShow/img/[^"]*?)"', content)
        img_url = "http://index.baidu.com%s" % img_url[0]

        regex = ('(?is)<span class="imgval" style="width:(\d+)px;">'
                 '<div class="imgtxt" style="margin-left:-(\d+)px;">')
        result = re.findall(regex, content)
        skip_info = result if result else list()
        return img_url, skip_info

    def _trend_value(self, img_url, skip_info):
        r = self.session.get(img_url)
        return img_util.get_num(r.content, skip_info)

    def fetch_an_week_crowd(self, keyword):
        res, res2, age_axis = self._crowd_params(keyword)

        age_data, sex_data = self._crowd_data(res, res2)

        age_dict = dict()
        for i, age in enumerate(age_axis):
            age_dict[age] = age_data['%s' % (i+1)]
        return age_dict, sex_data

    def _crowd_params(self, keyword):
        url = ONE_WEEK_CROWD_URL['CROWD_PAGE'].format(
            word=urllib.quote(keyword.encode('gbk'))
        )
        self.browser.get(url)
        res = self.browser.execute_script('return PPval.ppt;')
        res2 = self.browser.execute_script('return PPval.res2;')
        age_axis = self.browser.execute_script('return G.chart.CONFIG.ICON_AGE_TEXT;')
        return res, res2, age_axis

    def _crowd_data(self, res, res2):
        url = ONE_WEEK_CROWD_URL['CROWD_CHART_DATA'].format(
            res=res, res2=res2
        )

        r = self.session.get(url).json()
        return r['data'][0]['str_age'], r['data'][0]['str_sex']

    def fetch_poi_list_by_city(self, query, city, ak):
        results = []
        query = urllib.quote(query.encode('utf8'))
        city = urllib.quote(city.encode('utf8'))
        page_num = 0
        while (True):
            url = POI_QUERY_URL.format(
                query = query,
                city = city,
                page_num = page_num,
                ak = ak
            )
            r = self.session.get(url).json()
            if (r['status'] != 0 or not r['results']):
                break
            results.extend(r['results'])
            page_num += 1
        return results

    def fetch_poi_detail(self, uid, ak):
        url = POI_DETAIL_URL.format(
            uid = uid,
            ak = ak
        )
        r = self.session.get(url).json()
        if (r['status'] != 0 or not r['result']):
            return None
        return r['result']
