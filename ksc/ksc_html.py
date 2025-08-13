import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from io import StringIO
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


# 金山云文档地址
BASE_URL = "https://docs.ksyun.com/documents/705?type=3"

# 实例类型列表（可扩展）
fuzha=['星河云服务器-HKEC']

url ='https://docs.ksyun.com/documents/705?type=3#{type_url}'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'ksc_lang=zh; kscdigest=77385ef38a79fa654c21b97dd754a08b-843486820; uid=2000183027',
    # Replace with your actual cookie
    'referer': 'https://docs.ksyun.com/documents/705?type=3',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
}
response = requests.get(url, headers=headers)
# 打印响应状态码
print(f'Status Code: {response.status_code}')
html_content = response.text
# print(html_content)
soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.find_all('table')
# print(tables)
for i, table in enumerate(tables):
    # print("id:"+str(i));
    if i == 0  or i==1:
        continue

    table_html = preprocess_html(str(table))
    table_io = StringIO(table_html)
    # 解析表格
    df = pd.read_html(table_io)[0]
    #对比较复杂的表格特殊处理
    for i in fuzha:
        if(df.iloc[0,0]==i):
            df = df[1:]
    #判断有没有表头
    first_tr = table.find('tr')
    if ( first_tr.find('th') is None):
        df.columns = df.iloc[0]
        df = df[1:]
    # print(df)
    # 重置索引
    df.reset_index(drop=True, inplace=True)
    if df.columns[0]=='可用区域':
        continue
    # print(df)
    try:
        temp=df.columns[0]
        first_spec_name = df.iloc[0][temp]
        filename = first_spec_name.split('.')[0] + '.csv'

        # 统一名称
        # cols = list(df.columns)
        # cols[0] = '套餐类型名'
        # df.columns = cols

        path = r'E:\mini_tencent\ksyun\ksyun_instance\{title}'.format(title=filename)
        df.to_csv(path, index=False)
    except Exception as e:
        print(i)
        print(e)
