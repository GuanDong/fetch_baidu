#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

import json
from fetch_browser.baidu.baidu_browser import BaiduBrowser
from fetch_browser.utils.log import logger


baidu = BaiduBrowser()

logger.info('POI start')
jiayouzhan = baidu.fetch_poi_list_by_city(u'加油站',u'遵义','D4a1c2333a46a5181944baeb808043f1')
jingdian = baidu.fetch_poi_list_by_city(u'旅游景点',u'遵义','D4a1c2333a46a5181944baeb808043f1')
jiudian= baidu.fetch_poi_list_by_city(u'酒店',u'遵义','D4a1c2333a46a5181944baeb808043f1')
yiyuan = baidu.fetch_poi_list_by_city(u'医院',u'遵义','D4a1c2333a46a5181944baeb808043f1')
yinhang = baidu.fetch_poi_list_by_city(u'银行',u'遵义','D4a1c2333a46a5181944baeb808043f1')
pois = {}
pois[u'加油站']=[{'name': p['name'], 'value':[p['location']['lng'], p['location']['lat'], 1]} for p in jiayouzhan]
pois[u'旅游景点']=[{'name': p['name'], 'value':[p['location']['lng'], p['location']['lat'], 1]} for p in jingdian]
pois[u'酒店']=[{'name': p['name'], 'value':[p['location']['lng'], p['location']['lat'], 1]} for p in jiudian]
pois[u'医院']=[{'name': p['name'], 'value':[p['location']['lng'], p['location']['lat'], 1]} for p in yiyuan]
pois[u'银行']=[{'name': p['name'], 'value':[p['location']['lng'], p['location']['lat'], 1]} for p in yinhang]
f = file('poi.json','w')
f.write(json.dumps(pois, ensure_ascii=False).encode('utf8'))
f.close()

#jingdian = baidu.fetch_poi_list_by_city(u'旅游景点',u'遵义','D4a1c2333a46a5181944baeb808043f1')
#j_details = [baidu.fetch_poi_detail(j['uid'], 'D4a1c2333a46a5181944baeb808043f1') for j in jingdian]
#f = file('jingdian1.json','w')
#f.write(json.dumps(j_details, ensure_ascii=False, indent=4).encode('utf8'))
#f.close()
logger.info('POI end')


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
