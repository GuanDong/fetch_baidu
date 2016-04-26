#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

def get_date_info(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.strptime(end_date, '%Y%m%d')

    date_list = []
    temp_date = start_date
    while temp_date <= end_date:
        date_list.append(temp_date.strftime("%Y-%m-%d"))
        temp_date += timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return start_date, end_date, date_list
