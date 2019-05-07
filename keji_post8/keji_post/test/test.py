# infoHeaders = {
#     'Host': 'output.nsfc.gov.cn',
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9'
# }
# from fake_useragent import UserAgent
# ua = UserAgent(verify_ssl=False)
# infoHeaders['User-Agent']=ua.random
# print(infoHeaders)
sq_code = ['A','B']
zz_lei = ['218', '220', '222', '339', '429', '432', '649', '579', '630''631', '632', '2699']  # 资助类别
#
# for sq in sq_code:
#     for zz in zz_lei:
#         for year in range(1981,2019):
#             print(sq,zz,year)

print(len(zz_lei[0]))