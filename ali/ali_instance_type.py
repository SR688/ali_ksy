import requests

url = 'https://query.aliyun.com/rest/sell.ecs.allInstanceTypes'
params = {
    'regionId': '',
    'domain': 'aliyun',
    'zoneId': '',
    'saleStrategy': 'PostPaid'
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'cna=eTEcH00rVgMBASQIhPtH68uO; sca=712fcdb5; help_csrf=iX%2BFIIit2GzNg%2Fn7i0F%2BT5ztTBheylY0J6XtFXFN%2F8Df59CjDIpHu%2Fszk%2FFgzP%2B4y47F62EU3HCy%2Fhrfe%2FjNTR2g5BZM0zrRBcBM9p2g4xQ8%2BR%2FhESa1Uf6vkq3Klhsr5E53USJTEZd8%2FvTac%2B2juA%3D%3D; cr_token=f6a26eee-b744-45d7-b68c-e124c8c1e984; channel=7HqqdgOILC%2BWXdOAmm2Lqy3fof0aiCtsMgA%2Fg4nLblY%3D; aliyun_choice=intl; hsite=6; partitioned_cookie_flag=addPartitioned; aliyun_site=INTL; login_aliyunid_ticket=0vpmV*s*CT58JlM_1t$w3xR$UOieXgw8VpGwyhQqrAuHeyODJVgchjoPHwTnom__gfpof_BNTwUhTOoNC1ZBeeMfKJzxdnb95hYssNIZor6q7SCxRtgmGCbifG2Cd4ZWazmBdHI6sgXZqg4XFWQfyKue0; aliyun_lang=zh; hssid=6HC_hL16hmXG3FZOwDDHrlw1; login_aliyunid_pks=BG+UUdJyA0EoHN5w+KWgtMkwL+keLZvl5zRZ0KrweSRDP8=; login_aliyunid_pk=5942834342032124; login_aliyunid_csrf=_csrf_tk_1015834342034304; login_aliyunid=lth****@gmail.com; aliyun_country=HK; yunpk=5942834342032124; atpsida=6c39ceb6e428e9bfbb052d37_1734690745_10; tfstk=g_HtXWZGKHI9NKekIdO3olL4DU-nHxnaRVo5nr4GG23KV07gGCuDHKio-SMgIc0Kcm3tIf2_nSgxz0HGnFe_kq3nJPDmsrvjJ40VIqn2boajlqUmsBvobcy4hU2vELmNwvYTuAefoDwamuC6_TpobcSBX_EbGLbAHYtIfrgb1yZQ0y6bflgbdkZzROZfCo_BvozQhswfhD1Q4lI_lqwXvDaU0-Zs60TYRGacHjYH6P65IrXfhvETOBm_RtZEplFTPcMCJwI4X5USfyTu0JDbMVFtKdQzXXi-Sl32UOy_MfG7CxLJBJirtVZKlUCYRbHZH7D9y_zsQru8CXLCB-wiBbVzHQIaxAnIUSHwW9at8DGuQYTFH4inqAPEHUQQufqzdlhpc6a_GgynEYenIa48m1tpvs541kJnGak-7AVdWkUkXKCVgW-Fn1HY3s541krLrH2fgsPeY; isg=BAMDfjlMYA-GgC0LZmks8_G_ksGteJe6YnqBTDXgX2L99CMWvUgnCuFiboS60e-y',
    'origin': 'https://www.aliyun.com',
    'priority': 'u=1, i',
    'referer': 'https://www.aliyun.com/price/product',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

response = requests.get(url, params=params, headers=headers)

# 打印响应状态码和内容
print(f"Status Code: {response.status_code}")

instance_type_family = response.json()['data']['components']['instance_type']['instance_type_family']

# ['components']['instance_type']['instance_type']['instance_type_family']

print(f"Response Content: {instance_type_family}")