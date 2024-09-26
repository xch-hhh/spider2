"""
上海市杨浦区人民政府
https://www.shyp.gov.cn/
"""
from core.pipelines.ossPipeline import OssPipeline
from core.template_spider import TemplateSpider


class _7509Spider(TemplateSpider):
    name = '7509'
    duplicate_removal = False
    url_list = [
        {'section': '规划资源局专栏_公示公告', 'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-gtjzl-gsgg/index{}.html'},
        {'section': '规划资源局专栏_规划用地许可证',
         'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-gtjzl-xzxkgk-ghydxkz/index{}.html'},
        {'section': '规划资源局专栏_规划土地意见书',
         'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-gtjzl-xzxkgk-xzyjs/index{}.html'},
        {'section': '规划资源局专栏_规划工程许可证',
         'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-gtjzl-xzxkgk-ghgcxkz/index{}.html'},
        {'section': '生态环境局', 'check_title': True, 'use_bid': False,
         'add_keys': '项目、中标、招标、成交、合同、中标候选人、邀标、资格预审、评标、预公告、邀请、询价、比选、议价、竞价、磋商、采购、招投标、答疑、变更公告、更正公告、竞争性谈判、澄清、单一来源、流标、废标、竟价、开标结果、中选、补遗、竞标、询比、开标、遴选、议标、电子卖场、招租、产权、拍卖'.split('、'),
         'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-hbjzl-wryhjjgxx-ggl/index{}.html'},
        {'section': '建设项目_环境影响评价受理信息公示',
         'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-hbjzl-wryhjjgxx-slxxgs/index{}.html'},
        {'section': '建设项目_环境影响评价拟审批公示',
         'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-hbjzl-wryhjjgxx-spgs/index{}.html'},
        {'section': '建设项目_环境影响评价审批决定公告',
         'url': 'https://www.shyp.gov.cn/shypq/yqyw-wb-hbjzl-wryhjjgxx-spjdgg/index{}.html'},
    ]
    def_bidding = {
        'source_id': name,
        'province_name': '上海市',
        'city_name': '上海市',
    }

    section_parse = {
        '规划资源局专栏_公示公告': {
            'item_list': {'parse_type': 'css', 'data': ['ul.uli16 > li']},
            'public_time': {'parse_type': 'css', 'data': [['*'], '.']},
            'title': {'parse_type': 'css', 'data': ['a::attr(title)', 'a::text']},
            'source_url': {'parse_type': 'css', 'data': [['a::attr(href)'], '', 'urljoin']},
            'hit_url': {'parse_type': 'source_url', 'method': 'get'},
            'detail': {'parse_type': 'json'},
        },
        '规划资源局专栏_规划用地许可证': '规划资源局专栏_公示公告',
        '规划资源局专栏_规划土地意见书': '规划资源局专栏_公示公告',
        '规划资源局专栏_规划工程许可证': '规划资源局专栏_公示公告',
        '生态环境局': '规划资源局专栏_公示公告',
        '建设项目_环境影响评价受理信息公示': '规划资源局专栏_公示公告',
        '建设项目_环境影响评价拟审批公示': '规划资源局专栏_公示公告',
        '建设项目_环境影响评价审批决定公告': '规划资源局专栏_公示公告',
    }

    def getListData(self, params):
        yield self.get(
            url=params['url'].format('' if params['page'] == 1 else params['page']), callback=self.query_list,
            meta={'params': params}, headers=self.def_headers, cookies=self.cookie_dict)

    def additional_processing(self, response, data, bidding):
        if bidding['section'] not in ['生态环境局']:
            bidding['type'] = 3
        if '建设项目_' in bidding['section']:
            bidding['title'] += bidding['section'].split('_', 1)[1]

    def text_splicing(self, response, bidding):
        div = response.css('div#ivs_content') or response.css('div.Article_content')
        bidding['archives'] = []
        for f in response.css('ul.uli16 > li'):
            if not f.css('a::attr(href)') or not f.css('a::attr(href)').get():
                continue
            f_url = response.urljoin(f.css('a::attr(href)').get())
            hit_url = OssPipeline().process_dynamic_file_type(f_url, headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "zh-CN,zh;q=0.9",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            })
            bidding['archives'].append({
                'name': f.css('a::attr(title)').get() or '', 'url': hit_url or f_url, 'raw': True})
        return div.get() if div else None
