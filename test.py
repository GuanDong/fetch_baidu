#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

from baidu.baidu_browser import BaiduBrowser
from utils.log import logger


baidu = BaiduBrowser()
baidu.login('lingzantian', '123456Gd')

for keyword in [u'遵义', u'秦皇岛']:
    try:
        trend_dict = baidu.fetch_an_week_trend(keyword)
        for date, value in trend_dict.iteritems():
            logger.info(
                'keyword:%s date:%s, value:%s' % (keyword, date, value)
            )

        age_dict, sex_dict = baidu.fetch_an_week_crowd(keyword)
        logger.info("======crowd age======")
        for date, value in age_dict.iteritems():
            logger.info(
                'keyword:%s date:%s, value:%s' % (keyword, date, value)
            )

        logger.info("======crowd sex_dict======")
        for date, value in sex_dict.iteritems():
            logger.info(
                'keyword:%s date:%s, value:%s' % (keyword, date, value)
            )
    except:
        print traceback.format_exc()
