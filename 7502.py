# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    7502.py
    ~~~~~~~~~~~

    昭通市人民政府
    http://www.zt.gov.cn/
    :author: windy Zeng
    :copyright: (c) 2024, ZC
    :date created: 2024-09-23
    :python version: 3.8
"""
from core.template_spider import TemplateSpider


class _7502Spider(TemplateSpider):
    name = '7502'
    ignore_http_error = [404, 403]
    def_bidding = {
        'source_id': name,
        'province_name': '云南省',
        'city_name': '昭通市'

    }

    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 3
    }

    sync_exec = True

    section_parse = {
        "通知公告": {
            'item_list': {'parse_type': 'css', 'data': ['div.colu-list > div']},
            'public_time': {'parse_type': 'css', 'data': [['div.time-r'], '-']},
            'title': {'parse_type': 'css', 'data': ['div.colu-name > a::text']},
            'source_url': {'parse_type': 'css', 'data': [['div.colu-name > a::attr(href)'], '', 'urljoin']},
            'hit_url': {'parse_type': 'source_url', 'method': 'get'},
            'detail': {'parse_type': 'css', 'data': ['div.deta-bd.wow.fadeInUp > p']},
        },

        "重大建设项目_批准服务": {
            'item_list': {'parse_type': 'css', 'data': ['div.table-wrap > table >tbody > tr:not(:first-child)']},
            'public_time': {'parse_type': 'css', 'data': [['tr > td:nth-child(3)::text'], '-']},
            'title': {'parse_type': 'css', 'data': ['a::text']},
            'source_url': {'parse_type': 'css', 'data': [['a::attr(href)'], '', 'urljoin']},
            'hit_url': {'parse_type': 'source_url', 'method': 'get'},
            'detail': {'parse_type': 'css', 'data': ['div.view.zfxxgk_zn']},
        },

        "重大建设项目_施工信息": "重大建设项目_批准服务",
        "重大建设项目_重大设计变更": "重大建设项目_批准服务",
        "重大建设项目_批准结果": "重大建设项目_批准服务",

        "环境保护_辐射安全": "通知公告",
        "环境保护_行政审批": "通知公告",

    }

    url_list = [
        {
            # "maxRange": 100,
            "section": "通知公告",
            "url": "http://www.zt.gov.cn/lanmu/xwzx/15{}.html",
            'check_title': True,
            'use_bid': False,
            'add_keys': "中标、招标、成交、合同、中标候选人、邀标、资格预审、评标、预公告、邀请、询价、比选、议价、竞价、磋商、采购、招投标、答疑、变更公告、更正公告、竞争性谈判、澄清、单一来源、流标、废标、竟价、开标结果、中选、补遗、竞标、询比、开标、遴选、议标、电子卖场、招租、产权、拍卖".split(
                "、")

        },
        {
            # "maxRange": 13,
            "section": "重大建设项目_批准服务",
            "url": "http://www.zt.gov.cn/channels/5552{}.html",
        },
        {
            # "maxRange": 9,
            "section": "重大建设项目_施工信息",
            "url": "http://www.zt.gov.cn/channels/5555{}.html",
            'check_title': True,
            'use_bid': False,
            'add_keys': ["环境影响"]
        },
        {
            # "maxRange": 3,
            "section": "重大建设项目_重大设计变更",
            "url": "http://www.zt.gov.cn/channels/6372{}.html",
            'check_title': True,
            'use_bid': False,
            'add_keys': ["批复"]
        },
        {
            # "maxRange": 21,
            "section": "重大建设项目_批准结果",
            "url": "http://www.zt.gov.cn/channels/1984{}.html",
        },

        {
            # "maxRange": 15,
            "section": "环境保护_辐射安全",
            "url": "http://www.zt.gov.cn/lanmu/zwgk/333{}.html",
        },

        {
            # "maxRange": 15,
            "section": "环境保护_行政审批",
            "url": "http://www.zt.gov.cn/lanmu/zwgk/331{}.html",
        },
    ]

    def getListData(self, params):
        page = params['page']
        if page == 1:
            p = ''
        else:
            p = f"_{page}"
        # params["auto_page"] = False
        yield self.get(url=params['url'].format(p), callback=self.query_list,
                       meta={"params": params}, headers=self.def_headers, cookies=self.cookie_dict)
