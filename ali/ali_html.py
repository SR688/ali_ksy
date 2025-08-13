import csv
from io import StringIO
import re
from bs4 import BeautifulSoup

import requests
import pandas as pd


def preprocess_html(html_content):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 移除包含无效rowspan属性值的标签
    for td in soup.find_all('td'):
        if 'rowspan' in td.attrs:
            try:
                int(td.attrs['rowspan'])
            except ValueError:
                del td.attrs['rowspan']
        if 'colspan' in td.attrs:
            try:
                int(td.attrs['colspan'])
            except ValueError:
                del td.attrs['colspan']

    return str(soup)


url_type = ['general-purpose-instance-families', 'compute-optimized-instance-families',
            'memory-optimized-instance-families-1', 'big-data-instance-families', 'instance-families-with-local-ssds',
            'instance-families-with-high-clock-speeds', 'enhanced-instance-families', 'gpu-accelerated-compute-optimized-and-vgpu-accelerated-instance-families-1',
            'elastic-bare-metal-server-overview', 'super-computing-cluster-instance-type-family',
            'shared-instance-families']

for url_type in url_type:
    url = 'https://www.alibabacloud.com/help/json/document_detail.json' \
          '?alias=%2Fecs%2Fuser-guide%2F{type_url}' \
          '&pageNum=1&pageSize=20&website=intl&language=zh&channel='.format(type_url=url_type)

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'bx-v': '2.5.22',
        'cookie': 'aliyun_choice=intl; _alicloud_ab_trace_id=e6248e40-4da6-11ef-b9c0-9b3ceffa2c04; '
                  '_bl_uid=p6l9az6z6Xez661Xz8Xst4zzm0d3; cna=VnouHzWIC0cCASuEjRkjQ70u; '
                  '_hjid=beb27c57-c91f-4e11-bcf1-b00db3f9d1fc; yunqi_csrf=97GQ2BKXPL; _ali_s_gray_v=onesite,au,in,'
                  'vn; _ali_enable_ai=1; _ali_s_gray_t=59; _gcl_au=1.1.486799242.1731479087; '
                  '_ga_HHXQMRFV4P=GS1.2.1731479086.1.0.1731479086.0.0.0; partitioned_cookie_flag=addPartitioned; '
                  'login_aliyunid_csrf=_csrf_tk_1952731479087824; _uab_collina=173392948744952507960636; '
                  'notice_behavior=implied,eu; '
                  'help_csrf=r8kNUtr4Mam2B%2F19sYqh3A2P9pHVmIZOYgtq3ZNJhPpImezb6KDUQGPXUIZMc3MKw7qzBV'
                  '%2BXPmhRLzaTQkG1Ccy4f5eQzHT985q5SLHGBFDP9fZNGG6buO%2B5K236wbgk0nNM9k51oZE4wNzn0ggQ8A%3D%3D; '
                  'cr_token=ebcb3b1d-b571-4847-a0cb-f5c1878ba246; _hjTLDTest=1; '
                  'channel=7HqqdgOILC%2BWXdOAmm2Lqy3fof0aiCtsMgA%2Fg4nLblY%3D; aliyun_lang=zh; aliyun_intl_choice=intl; '
                  'alicloud_deploy_r_s=sg; TAsessionID=0254f37c-ac4f-40dc-a92e-d12bd292a98c|NEW; '
                  '_umdata=99090CDCA81839685AB063E9F33E92D119149ABB4FB530B8B3ABA6989C88AB4D7083340EF2F359B2CD43AD3E795C914C56C5A3CFF9355F70750792F0E1AB90B1; xlly_s=1; _hjAbsoluteSessionInProgress=0; _gid=GA1.2.2092328482.1734317265; notice_preferences=2:; notice_gdpr_prefs=0,1,2::implied,eu; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; X-XSRF-TOKEN=987fc2f5-0876-40f5-9138-263d4fa7456d; _uetsid=2086bb10bb5811efa89bd16190098b73; _uetvid=e80c08304da611efa9753f8417aa3891; _ga_K73QREWZ1D=GS1.1.1734317264.6.1.1734317537.60.0.0; _ga=GA1.1.1475158885.1722256474; _hjIncludedInSessionSample=0; _gat_gtag_UA_69110890_1=1; tfstk=gCaqRAVB9V25hPUVIb0wz0Ix1m0x-qXCIPMss5ViGxDDlE9g4RwuG1IAXVkae8Kb55XYQPkunogs5qjM_Y2UlEgmGAYa_YyXco6978y3LcZjfiCaz5FE1Aaa6FlgsRCxCsI7MS3tS96QQwNYMzMzbwaqm3YuwXcMSgic0Avoh96CRasDZVWVd-_xaoWr6YcDofDca0cxgI0imEAlafc6nhD0I7frefpDIjcmE4cEiI0iSRVlafHoifcTi5YrOmfdTzfQJ3Ex0vVmUeP8zjXSLwHWSF4rgl0UihLMSzlqmPtRQMsSSoVbUDZVLEuTikett-vc3bz4TPr3EaTq77q3744lEQM0v7zZlrf1o4443rmzICBtwkGU_DZ5sHk7j7Ur4rSB6bUbsrnI-wpmCuNU7fzOBayUi-rnxrvV4RJtZG48WoJMbmc-av1Pa2q45gJcKj19XhnoJbkCGjtMjpVrav1PahKtDNlrdsGf.; isg=BHV',
        # Replace with your actual cookie
        'eagleeye-pappname': 'fq234nz6x8@da4913253508f58',
        'eagleeye-sessionid': 'eRmb84RgqsjfwwwL61yqpFtrI56m',
        'eagleeye-traceid': '9b8b2f1d1734317549562101108f58',
        'priority': 'u=1, i',
        'referer': 'https://www.alibabacloud.com/help/zh/ecs/user-guide/general-purpose-instance-families?spm=a2c63.p38356.help-menu-25365.d_4_1_2_2.74ff662bIUrjTN',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    # 打印响应状态码
    print(f'Status Code: {response.status_code}')

    html_content = response.text
    # print(html_content)
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到表格
    tables = soup.find_all('table')

    # 遍历每个表格并转换为CSV
    for i, table in enumerate(tables):
        # 使用StringIO包装HTML字符串
        table_html = preprocess_html(str(table))
        table_io = StringIO(table_html)

        # 解析表格
        df = pd.read_html(table_io)[0]
        print(df)
        df.columns = df.iloc[0]
        df = df[1:]

        # 重置索引
        df.reset_index(drop=True, inplace=True)
        try:
            df = df.reset_index(drop=True)
            first_spec_name = df.iloc[0]['实例规格']
            filename = first_spec_name.split('.')[1] + '.csv'
            path = '/Users/chenguanjin/Desktop/ali/aliinstance/{title}'.format(title=filename)
            df.to_csv(path, index=False)
        except Exception as e:
            print(i)
            print(e)

print('All tables have been converted to CSV files.')

#
# # 提取表头
# headers = []
# for th in table.find('th'):
#     headers.append(th.get_text(strip=True))
#
# # 提取表格内容
# rows = []
# for tr in table.find('tr')[1:]:  # 跳过表头行
#     cells = tr.find_all('td')
#     row = [cell.get_text(strip=True) for cell in cells]
#     rows.append(row)
#
# print(rows)