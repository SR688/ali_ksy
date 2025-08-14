import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import os
from io import StringIO
url_type= ["X6E","SE9", "C9a", "AC5", "X9a", "X6S", "HKEC", "AC4", "X6", "X8", "X7", "N3", "S6", "S4E", "S4", "S3", "A6", "C7", "C5", "C4", "I6", "I4", "I3", "P4V", "P6V", "GN6I", "GN7I", "GN8I"]
url='https://docs.ksyun.com/documents/37393?type=3'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'ksc_lang=zh; kscdigest=77385ef38a79fa654c21b97dd754a08b-843486820; uid=2000183027',
    # Replace with your actual cookie
    'referer':'https://docs.ksyun.com/documents/37393?type=3',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
}

def extract_pay_as_you_go_tables(matches_html):
    """
    仅返回“机器类型”在 url_type 中的按量付费表格（DataFrame dict 形式）
    key = 机器类型，value = 对应 DataFrame
    """
    soup = BeautifulSoup(matches_html, 'html.parser')

    for tag in soup.find_all(['td', 'th']):
        for attr in ['rowspan', 'colspan']:
            if attr in tag.attrs:
                try:
                    int(tag.attrs[attr])
                except ValueError:
                    del tag.attrs[attr]

    tables = soup.find_all('table')
    results = {}

    for tbl in tables:
        prev = tbl.find_previous(['h4', 'h3', 'h2'])
        if not prev:
            continue
        section_title = prev.get_text(strip=True)

        # 只保留 url_type 里出现的
        if not any(sec in section_title for sec in url_type):
            continue

        ahead = str(prev) + str(tbl.previous_sibling or '')
        if '按量付费' not in ahead[-200:]:
            continue

        df = pd.read_html(StringIO(str(tbl)))[0]

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [' '.join(col).strip() for col in df.columns]

        # 无表头时用第一行当表头
        has_th = tbl.find('th') is not None
        if not has_th:
            df.columns = df.iloc[0]
            df = df.drop(index=0).reset_index(drop=True)
            df = df.iloc[:, 1:]

        results[section_title] = df

    return results


def main_code():
    response = requests.get(url, headers=headers)
    print(f'Status Code: {response.status_code}')
    html_content = response.text

    pattern1 = r'<div\s+class="ks-doc-main">(.*?)</div>'
    matches1 = re.search(pattern1, html_content, re.S)
    if not matches1:
        print('未匹配到文档主体')
        return

    # 获取 dict {机器类型: DataFrame}
    dfs = extract_pay_as_you_go_tables(matches1.group(1))
    if not dfs:
        print('未命中任何 url_type 中的机器类型')
        return

    # 保存目录
    save_dir = r'E:\mini_tencent\ksyun\ksyun_price'
    os.makedirs(save_dir, exist_ok=True)

    for mt, df in dfs.items():
        # 去掉文件名中的非法字符
        safe_name=''
        for i in url_type:
            if(i in mt):
                safe_name=i
                break
        file_path = os.path.join(save_dir, f'{safe_name}.csv')
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f'已保存 {file_path}')

if __name__ == '__main__':
    main_code()
