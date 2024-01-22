'''
东方财富股吧综合信息爬取
多协程爬取，东方财富股吧网站：热门话题、动态、要闻、情绪指数数据、股吧热榜、用户推荐（关注）等
'''
import requests
import re
import json
import os
import csv
import urllib.parse


headers = {
    'Referer':'http://guba.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
#headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive', 'Content-Length': '244', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'qgqp_b_id=49c3d4505c9b14fd126d92202f1a5454; rankpromt=1; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; mtp=1; ct=XF-nbwGdn5mz8NlJqhuPJuO-w4HQw7TkFc-Yr0BZLdvU2L5xBEB5gFLcUUJPN6r8WExeiVszQhGyB7y7WtcFy8WDsF8100t9I7b2RdyBGE69oom-Dqi05pSfPLDKmLHYFspfltM55m7IE3qR-SWOhLiQfPJ6G6nMjXMXNJWvCOM; ut=FobyicMgeV5ghfUPKWOH57DWvABp9u_NbE2jsMUROhXXKp8ws0AZ_YARcyRR9vspc6NHj8KE0JyrAz7H-FMaGnW3aSeQrAm-hGFJPIGudhPnZKgHytL2FhRXl8iAkV0RBvmoUgCHMLtF7QbGCvh8pHcsci1sWLOhA8ZcTfS1hbWIa_T5nvh5aajwidB7SBthBuFh3fxYdrUXnHnpJ1opWRlbbSqS6OAl4tcgzTfyKbq-2e8dLKkr-Hlnk9W_kbwjx5V6lMAA5KnbFbEuSdv5X5V_4S0szRLH; pi=2869094228770900%3Bm2869094228770900%3B%E4%B8%8D%E5%BF%AE%E6%B1%82%3BHaaipa1qpwsoNv4NVYWxrt5yWur5zd4NojwwPBUFAFvLbjdZDL2FTidD6ypzSlghQRR7VHqfQ03Q9zn6aQYDU74AU6Gs7YoB3pXPkklMoMKP6KMe8x49WJ62G7MkTj%2FShudgkpDSvrI%2F80fAWa5grksbYUJoOvN8%2FCI4ByVjo403xd0gcJH2Ku78%2BsOdsyxtax57a51D%3B7lPk0C5x%2FZLZLXmCTEsP8lYE0UmnM%2FCXfI1TuBSBpJIOi5f9HO%2Fhhac8r3%2BibTV5IkyFIVKjcUBbhgbqLtzjr%2FxVd10%2BCZaE9u243sDDk5RoGbVyQ4sdk9yPIfzs8GdmYsrml0gHHPg0V2vcAz415Im1lfuZJw%3D%3D; uidal=2869094228770900%e4%b8%8d%e5%bf%ae%e6%b1%82; sid=3690518; vtpst=|; emshistory=%5B%22%E6%94%B9%E7%89%88%22%2C%22%E8%82%A1%E5%90%A7%E6%94%B9%E7%89%88%22%5D; listtype=0; update_time=2023-08-19%2017%3A53%3A17; st_si=99485931141435; st_pvi=29862703569868; st_sp=2023-08-21%2008%3A21%3A02; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=1; st_psi=20230821082101773-117001350220-4028836725; st_asi=delete', 'Host': 'guba.eastmoney.com', 'Origin': 'http://guba.eastmoney.com', 'Referer': 'http://guba.eastmoney.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}


def getgz():
    '''爬取关注信息数据：动态'''

    url = "http://guba.eastmoney.com/api/dynamicInfo"
    headers = {
    'Referer':'http://guba.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    #之前用上面的请求头爬取的内容对不上，全部复制网页的完整请求头，爬取正常，看来请求头非常重要。
    headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive', 'Content-Length': '244', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'qgqp_b_id=49c3d4505c9b14fd126d92202f1a5454; rankpromt=1; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; mtp=1; ct=XF-nbwGdn5mz8NlJqhuPJuO-w4HQw7TkFc-Yr0BZLdvU2L5xBEB5gFLcUUJPN6r8WExeiVszQhGyB7y7WtcFy8WDsF8100t9I7b2RdyBGE69oom-Dqi05pSfPLDKmLHYFspfltM55m7IE3qR-SWOhLiQfPJ6G6nMjXMXNJWvCOM; ut=FobyicMgeV5ghfUPKWOH57DWvABp9u_NbE2jsMUROhXXKp8ws0AZ_YARcyRR9vspc6NHj8KE0JyrAz7H-FMaGnW3aSeQrAm-hGFJPIGudhPnZKgHytL2FhRXl8iAkV0RBvmoUgCHMLtF7QbGCvh8pHcsci1sWLOhA8ZcTfS1hbWIa_T5nvh5aajwidB7SBthBuFh3fxYdrUXnHnpJ1opWRlbbSqS6OAl4tcgzTfyKbq-2e8dLKkr-Hlnk9W_kbwjx5V6lMAA5KnbFbEuSdv5X5V_4S0szRLH; pi=2869094228770900%3Bm2869094228770900%3B%E4%B8%8D%E5%BF%AE%E6%B1%82%3BHaaipa1qpwsoNv4NVYWxrt5yWur5zd4NojwwPBUFAFvLbjdZDL2FTidD6ypzSlghQRR7VHqfQ03Q9zn6aQYDU74AU6Gs7YoB3pXPkklMoMKP6KMe8x49WJ62G7MkTj%2FShudgkpDSvrI%2F80fAWa5grksbYUJoOvN8%2FCI4ByVjo403xd0gcJH2Ku78%2BsOdsyxtax57a51D%3B7lPk0C5x%2FZLZLXmCTEsP8lYE0UmnM%2FCXfI1TuBSBpJIOi5f9HO%2Fhhac8r3%2BibTV5IkyFIVKjcUBbhgbqLtzjr%2FxVd10%2BCZaE9u243sDDk5RoGbVyQ4sdk9yPIfzs8GdmYsrml0gHHPg0V2vcAz415Im1lfuZJw%3D%3D; uidal=2869094228770900%e4%b8%8d%e5%bf%ae%e6%b1%82; sid=3690518; vtpst=|; emshistory=%5B%22%E6%94%B9%E7%89%88%22%2C%22%E8%82%A1%E5%90%A7%E6%94%B9%E7%89%88%22%5D; listtype=0; update_time=2023-08-19%2017%3A53%3A17; st_si=99485931141435; st_pvi=29862703569868; st_sp=2023-08-21%2008%3A21%3A02; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=1; st_psi=20230821082101773-117001350220-4028836725; st_asi=delete', 'Host': 'guba.eastmoney.com', 'Origin': 'http://guba.eastmoney.com', 'Referer': 'http://guba.eastmoney.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    data = {
        'param': 'uid=2869094228770900&keychainId=&condition=null&isReload=true&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=1000', #最大1700，可尝试
        #'param': 'uid=2869094228770900&keychainId=&condition=null&isReload=true&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=30',
        #'param': 'uid=2869094228770900&keychainId=&condition=%7B%22dynamicCountScore%22%3A1692554319235000%2C%22dynamicScore%22%3A1692533760000580%2C%22personalScore%22%3A1692554319235000%2C%22prli%22%3A0%7D&isReload=false&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=600',
        #'param': 'uid=2869094228770900&keychainId=&condition={"dynamicCountScore":1692554319235000,"dynamicScore":1692533760000580,"personalScore":1692554319235000,"prli":0}&isReload=false&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=10',
        'origin': '',
    }
    res = requests.post(url, data=data, headers=headers)  #这里post 和get 一样的效果？？
    print(res)
    response=res.text
    #print(response)
    js_data = json.loads(response)['data']['items']
    #print(js_data)
    savepath = os.getcwd() + r'\data'
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    fp = open(savepath + r'\DFCF_gz.csv', 'w', encoding='utf-8-sig', newline='')
    fw = csv.writer(fp)
    fw.writerow(['序号','标题','内容'])
    i = 0
    src_security_code_dict = {}
    
    for item in js_data:
        i += 1
        xh = i       # 序号
        #zz = item['itemData']['title']         # 作者
        #print(zz)
        #gpdm = item['gubaId']                  # 股票代码
        #gpmc = item['securityName']            # 股票名称

        try:
            bt = item['itemData']['title']      # 标题
        except:
            try:
                bt = item['itemData']['postTopic'] 
            except:
                try:     
                    bt = item['itemData']['questionContent'] #没有title找postTopic，还没有找questionContent
                except:
                    bt='无标题'
        #sj = item['itemData']['summary']        #内容
        try:   
            sj = item['itemData']['summary']     #内容
        except:
            sj='内容见标题'
        content = [xh, bt, sj]
        #content = [xh, bt]
        print(content)
        fw.writerow(content)

def getgztop2():
    '''爬取关注信息数据'''

    url = "http://guba.eastmoney.com/api/dynamicInfo"
    headers = {
    'Referer':'http://guba.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive', 'Content-Length': '244', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'qgqp_b_id=49c3d4505c9b14fd126d92202f1a5454; rankpromt=1; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; mtp=1; ct=XF-nbwGdn5mz8NlJqhuPJuO-w4HQw7TkFc-Yr0BZLdvU2L5xBEB5gFLcUUJPN6r8WExeiVszQhGyB7y7WtcFy8WDsF8100t9I7b2RdyBGE69oom-Dqi05pSfPLDKmLHYFspfltM55m7IE3qR-SWOhLiQfPJ6G6nMjXMXNJWvCOM; ut=FobyicMgeV5ghfUPKWOH57DWvABp9u_NbE2jsMUROhXXKp8ws0AZ_YARcyRR9vspc6NHj8KE0JyrAz7H-FMaGnW3aSeQrAm-hGFJPIGudhPnZKgHytL2FhRXl8iAkV0RBvmoUgCHMLtF7QbGCvh8pHcsci1sWLOhA8ZcTfS1hbWIa_T5nvh5aajwidB7SBthBuFh3fxYdrUXnHnpJ1opWRlbbSqS6OAl4tcgzTfyKbq-2e8dLKkr-Hlnk9W_kbwjx5V6lMAA5KnbFbEuSdv5X5V_4S0szRLH; pi=2869094228770900%3Bm2869094228770900%3B%E4%B8%8D%E5%BF%AE%E6%B1%82%3BHaaipa1qpwsoNv4NVYWxrt5yWur5zd4NojwwPBUFAFvLbjdZDL2FTidD6ypzSlghQRR7VHqfQ03Q9zn6aQYDU74AU6Gs7YoB3pXPkklMoMKP6KMe8x49WJ62G7MkTj%2FShudgkpDSvrI%2F80fAWa5grksbYUJoOvN8%2FCI4ByVjo403xd0gcJH2Ku78%2BsOdsyxtax57a51D%3B7lPk0C5x%2FZLZLXmCTEsP8lYE0UmnM%2FCXfI1TuBSBpJIOi5f9HO%2Fhhac8r3%2BibTV5IkyFIVKjcUBbhgbqLtzjr%2FxVd10%2BCZaE9u243sDDk5RoGbVyQ4sdk9yPIfzs8GdmYsrml0gHHPg0V2vcAz415Im1lfuZJw%3D%3D; uidal=2869094228770900%e4%b8%8d%e5%bf%ae%e6%b1%82; sid=3690518; vtpst=|; emshistory=%5B%22%E6%94%B9%E7%89%88%22%2C%22%E8%82%A1%E5%90%A7%E6%94%B9%E7%89%88%22%5D; listtype=0; update_time=2023-08-19%2017%3A53%3A17; st_si=99485931141435; st_pvi=29862703569868; st_sp=2023-08-21%2008%3A21%3A02; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=1; st_psi=20230821082101773-117001350220-4028836725; st_asi=delete', 'Host': 'guba.eastmoney.com', 'Origin': 'http://guba.eastmoney.com', 'Referer': 'http://guba.eastmoney.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    data = {
        'param': 'uid=2869094228770900&keychainId=&condition=null&isReload=true&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=30',
        #'param': 'uid=2869094228770900&keychainId=&condition=null&isReload=true&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=30',
        #'param': 'uid=2869094228770900&keychainId=&condition=%7B%22dynamicCountScore%22%3A1692554319235000%2C%22dynamicScore%22%3A1692533760000580%2C%22personalScore%22%3A1692554319235000%2C%22prli%22%3A0%7D&isReload=false&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=600',
        #'param': 'uid=2869094228770900&keychainId=&condition={"dynamicCountScore":1692554319235000,"dynamicScore":1692533760000580,"personalScore":1692554319235000,"prli":0}&isReload=false&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=10',
        'origin': '',
    }
    res = requests.post(url, data=data, headers=headers)  #这里post 和get 一样的效果？？
    print(res)
    response=res.text  #字符串
    #print(response)
    #js_data = json.loads(response)['data']['realTimeFixedItems'] #将字符串转换为列表并剥洋葱，json.dumps(a)--将列表转换成json字符串
    js_data = res.json()['data']['realTimeFixedItems'] #l另一种方法：直接将response对象转换为列表并剥洋葱
    #print(js_data)
    savepath = os.getcwd() + r'\data'
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    fp = open(savepath + r'\DFCF_gztop2.csv', 'w', encoding='utf-8-sig', newline='')
    fw = csv.writer(fp)
    fw.writerow(['序号','标题','评论数'])
    i = 0
    src_security_code_dict = {}
    
    for item in js_data:
        i += 1
        xh = i       # 序号
        #zz = item['itemData']['title']              # 作者
        #print(zz)
        #gpdm = item['gubaId']                       # 股票代码
        #gpmc = item['securityName']                 # 股票名称
        try:
            bt = item['itemData']['title']           # 标题
        except:
            bt = item['itemData']['postTopic'] 

        sj = item['itemData']['commentCount']         #评论数
        content = [xh, bt, sj]
        print(content)
        fw.writerow(content)



def getrmht():
    '''爬取热门话题数据'''

    url = "http://gubatopic.eastmoney.com/interface/GetData.aspx"
    headers = {
    'Referer':'http://guba.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    headers={'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive', 'Content-Length': '85', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'qgqp_b_id=49c3d4505c9b14fd126d92202f1a5454; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; mtp=1; ct=XF-nbwGdn5mz8NlJqhuPJuO-w4HQw7TkFc-Yr0BZLdvU2L5xBEB5gFLcUUJPN6r8WExeiVszQhGyB7y7WtcFy8WDsF8100t9I7b2RdyBGE69oom-Dqi05pSfPLDKmLHYFspfltM55m7IE3qR-SWOhLiQfPJ6G6nMjXMXNJWvCOM; ut=FobyicMgeV5ghfUPKWOH57DWvABp9u_NbE2jsMUROhXXKp8ws0AZ_YARcyRR9vspc6NHj8KE0JyrAz7H-FMaGnW3aSeQrAm-hGFJPIGudhPnZKgHytL2FhRXl8iAkV0RBvmoUgCHMLtF7QbGCvh8pHcsci1sWLOhA8ZcTfS1hbWIa_T5nvh5aajwidB7SBthBuFh3fxYdrUXnHnpJ1opWRlbbSqS6OAl4tcgzTfyKbq-2e8dLKkr-Hlnk9W_kbwjx5V6lMAA5KnbFbEuSdv5X5V_4S0szRLH; pi=2869094228770900%3Bm2869094228770900%3B%E4%B8%8D%E5%BF%AE%E6%B1%82%3BHaaipa1qpwsoNv4NVYWxrt5yWur5zd4NojwwPBUFAFvLbjdZDL2FTidD6ypzSlghQRR7VHqfQ03Q9zn6aQYDU74AU6Gs7YoB3pXPkklMoMKP6KMe8x49WJ62G7MkTj%2FShudgkpDSvrI%2F80fAWa5grksbYUJoOvN8%2FCI4ByVjo403xd0gcJH2Ku78%2BsOdsyxtax57a51D%3B7lPk0C5x%2FZLZLXmCTEsP8lYE0UmnM%2FCXfI1TuBSBpJIOi5f9HO%2Fhhac8r3%2BibTV5IkyFIVKjcUBbhgbqLtzjr%2FxVd10%2BCZaE9u243sDDk5RoGbVyQ4sdk9yPIfzs8GdmYsrml0gHHPg0V2vcAz415Im1lfuZJw%3D%3D; uidal=2869094228770900%e4%b8%8d%e5%bf%ae%e6%b1%82; sid=3690518; vtpst=|; isRecommendArr=; emshistory=%5B%22%E6%94%B9%E7%89%88%22%2C%22%E8%82%A1%E5%90%A7%E6%94%B9%E7%89%88%22%5D; st_si=99485931141435; st_pvi=29862703569868; st_sp=2023-08-21%2008%3A21%3A02; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=1; st_psi=20230821082101773-117001350220-4028836725; st_asi=delete', 'Host': 'gubatopic.eastmoney.com', 'Origin': 'http://gubatopic.eastmoney.com', 'Referer': 'http://gubatopic.eastmoney.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
    data = {
        #'param': 'uid=2869094228770900&keychainId=&condition=null&isReload=true&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=30',
        #'param': 'uid=2869094228770900&keychainId=&condition=%7B%22dynamicCountScore%22%3A1692554319235000%2C%22dynamicScore%22%3A1692533760000580%2C%22personalScore%22%3A1692554319235000%2C%22prli%22%3A0%7D&isReload=false&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=600',
        'param': 'ps=100&p=1&type=0',
        'path': 'newtopic/api/Topic/HomePageListRead',
        'env':'2'
    }
    res = requests.post(url, data=data, headers=headers)  #这里post 和get 一样的效果？？
    print(res)
    response=res.text
    #print(response)
    js_data = json.loads(response)['re']
    #print(js_data)
    savepath = os.getcwd() + r'\data'
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    fp = open(savepath + r'\DFCF_rmht.csv', 'w', encoding='utf-8-sig', newline='')
    fw = csv.writer(fp)
    fw.writerow(['序号','标题','内容'])
    i = 0
    src_security_code_dict = {}
    
    for item in js_data:
        i += 1
        xh = i       # 序号
        #zz = item['itemData']['title']         # 作者
        #print(zz)
        #gpdm = item['gubaId']                  # 股票代码
        #gpmc = item['securityName']            # 股票名称
        bt = item['nickname'] 
        '''
        try:
            bt = item['nickname']               # 标题
        except:
            pass
        ''' 
        sj = item['desc']                        #时间
        content = [xh, bt, sj]
        print(content)
        fw.writerow(content)


def getgbrb():
    '''爬取股吧热榜数据'''

    url = "http://guba.eastmoney.com/api/hotArticleRank"
    headers = {
    'Referer':'http://guba.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive', 'Content-Length': '244', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'qgqp_b_id=49c3d4505c9b14fd126d92202f1a5454; rankpromt=1; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; mtp=1; ct=XF-nbwGdn5mz8NlJqhuPJuO-w4HQw7TkFc-Yr0BZLdvU2L5xBEB5gFLcUUJPN6r8WExeiVszQhGyB7y7WtcFy8WDsF8100t9I7b2RdyBGE69oom-Dqi05pSfPLDKmLHYFspfltM55m7IE3qR-SWOhLiQfPJ6G6nMjXMXNJWvCOM; ut=FobyicMgeV5ghfUPKWOH57DWvABp9u_NbE2jsMUROhXXKp8ws0AZ_YARcyRR9vspc6NHj8KE0JyrAz7H-FMaGnW3aSeQrAm-hGFJPIGudhPnZKgHytL2FhRXl8iAkV0RBvmoUgCHMLtF7QbGCvh8pHcsci1sWLOhA8ZcTfS1hbWIa_T5nvh5aajwidB7SBthBuFh3fxYdrUXnHnpJ1opWRlbbSqS6OAl4tcgzTfyKbq-2e8dLKkr-Hlnk9W_kbwjx5V6lMAA5KnbFbEuSdv5X5V_4S0szRLH; pi=2869094228770900%3Bm2869094228770900%3B%E4%B8%8D%E5%BF%AE%E6%B1%82%3BHaaipa1qpwsoNv4NVYWxrt5yWur5zd4NojwwPBUFAFvLbjdZDL2FTidD6ypzSlghQRR7VHqfQ03Q9zn6aQYDU74AU6Gs7YoB3pXPkklMoMKP6KMe8x49WJ62G7MkTj%2FShudgkpDSvrI%2F80fAWa5grksbYUJoOvN8%2FCI4ByVjo403xd0gcJH2Ku78%2BsOdsyxtax57a51D%3B7lPk0C5x%2FZLZLXmCTEsP8lYE0UmnM%2FCXfI1TuBSBpJIOi5f9HO%2Fhhac8r3%2BibTV5IkyFIVKjcUBbhgbqLtzjr%2FxVd10%2BCZaE9u243sDDk5RoGbVyQ4sdk9yPIfzs8GdmYsrml0gHHPg0V2vcAz415Im1lfuZJw%3D%3D; uidal=2869094228770900%e4%b8%8d%e5%bf%ae%e6%b1%82; sid=3690518; vtpst=|; emshistory=%5B%22%E6%94%B9%E7%89%88%22%2C%22%E8%82%A1%E5%90%A7%E6%94%B9%E7%89%88%22%5D; listtype=0; update_time=2023-08-19%2017%3A53%3A17; st_si=99485931141435; st_pvi=29862703569868; st_sp=2023-08-21%2008%3A21%3A02; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=1; st_psi=20230821082101773-117001350220-4028836725; st_asi=delete', 'Host': 'guba.eastmoney.com', 'Origin': 'http://guba.eastmoney.com', 'Referer': 'http://guba.eastmoney.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    data = {
        'param': 'pageSize=500&condition=',
        'origin': '',
    }
    res = requests.post(url, data=data, headers=headers)  #这里post 和get 一样的效果？？
    print(res)
    response=res.text
    #print(response)
    js_data = json.loads(response)['data']['items']
    #print(js_data)
    savepath = os.getcwd() + r'\data'
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    fp = open(savepath + r'\DFCF_gbrb.csv', 'w', encoding='utf-8-sig', newline='')
    fw = csv.writer(fp)
    fw.writerow(['序号','标题','内容'])
    i = 0
    src_security_code_dict = {}
    
    for item in js_data:
        i += 1
        xh = i       # 序号
        #zz = item['itemData']['title']         # 作者
        #print(zz)
        #gpdm = item['gubaId']                  # 股票代码
        #gpmc = item['securityName']            # 股票名称
        bt = item['title']  
        '''
        try:
            bt = item['title']                  # 标题
        except:
            pass
        ''' 
        nr = item['digest']                      #内容
        content = [xh, bt,nr]
        #content = [xh, bt]
        print(content)
        fw.writerow(content)


def getyhtj():
    '''爬取用户推荐数据'''

    url = "http://guba.eastmoney.com/api/everybodylook"
    headers = {
    'Referer':'http://guba.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }
    #之前用上面的请求头爬取的内容对不上，全部复制网页的完整请求头，爬取正常，看来请求头非常重要。
    headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive', 'Content-Length': '66', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'qgqp_b_id=49c3d4505c9b14fd126d92202f1a5454; rankpromt=1; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; mtp=1; ct=XF-nbwGdn5mz8NlJqhuPJuO-w4HQw7TkFc-Yr0BZLdvU2L5xBEB5gFLcUUJPN6r8WExeiVszQhGyB7y7WtcFy8WDsF8100t9I7b2RdyBGE69oom-Dqi05pSfPLDKmLHYFspfltM55m7IE3qR-SWOhLiQfPJ6G6nMjXMXNJWvCOM; ut=FobyicMgeV5ghfUPKWOH57DWvABp9u_NbE2jsMUROhXXKp8ws0AZ_YARcyRR9vspc6NHj8KE0JyrAz7H-FMaGnW3aSeQrAm-hGFJPIGudhPnZKgHytL2FhRXl8iAkV0RBvmoUgCHMLtF7QbGCvh8pHcsci1sWLOhA8ZcTfS1hbWIa_T5nvh5aajwidB7SBthBuFh3fxYdrUXnHnpJ1opWRlbbSqS6OAl4tcgzTfyKbq-2e8dLKkr-Hlnk9W_kbwjx5V6lMAA5KnbFbEuSdv5X5V_4S0szRLH; pi=2869094228770900%3Bm2869094228770900%3B%E4%B8%8D%E5%BF%AE%E6%B1%82%3BHaaipa1qpwsoNv4NVYWxrt5yWur5zd4NojwwPBUFAFvLbjdZDL2FTidD6ypzSlghQRR7VHqfQ03Q9zn6aQYDU74AU6Gs7YoB3pXPkklMoMKP6KMe8x49WJ62G7MkTj%2FShudgkpDSvrI%2F80fAWa5grksbYUJoOvN8%2FCI4ByVjo403xd0gcJH2Ku78%2BsOdsyxtax57a51D%3B7lPk0C5x%2FZLZLXmCTEsP8lYE0UmnM%2FCXfI1TuBSBpJIOi5f9HO%2Fhhac8r3%2BibTV5IkyFIVKjcUBbhgbqLtzjr%2FxVd10%2BCZaE9u243sDDk5RoGbVyQ4sdk9yPIfzs8GdmYsrml0gHHPg0V2vcAz415Im1lfuZJw%3D%3D; uidal=2869094228770900%e4%b8%8d%e5%bf%ae%e6%b1%82; sid=3690518; vtpst=|; emshistory=%5B%22%E6%94%B9%E7%89%88%22%2C%22%E8%82%A1%E5%90%A7%E6%94%B9%E7%89%88%22%5D; listtype=0; st_si=99485931141435; st_pvi=29862703569868; st_sp=2023-08-21%2008%3A21%3A02; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=1; st_psi=20230821082101773-117001350220-4028836725; st_asi=delete; update_time=2023-08-21%2021%3A01%3A50', 'Host': 'guba.eastmoney.com', 'Origin': 'http://guba.eastmoney.com', 'Referer': 'http://guba.eastmoney.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    data = {
        'param': 'uid=2869094228770900&pageSize=600&condition=', #
        #'param': 'uid=2869094228770900&keychainId=&condition=null&isReload=true&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=30',
        #'param': 'uid=2869094228770900&keychainId=&condition=%7B%22dynamicCountScore%22%3A1692554319235000%2C%22dynamicScore%22%3A1692533760000580%2C%22personalScore%22%3A1692554319235000%2C%22prli%22%3A0%7D&isReload=false&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=600',
        #'param': 'uid=2869094228770900&keychainId=&condition={"dynamicCountScore":1692554319235000,"dynamicScore":1692533760000580,"personalScore":1692554319235000,"prli":0}&isReload=false&fundLogin=false&hffCloseTime=0&deviceId=guba_home&fundIds=&fundId=&hkFundLogin=&hkFundId=&mbid=&line=5&pageSize=10',
        'origin': '',
    }
    res = requests.post(url, data=data, headers=headers)  #这里post 和get 一样的效果？？
    print(res)
    response=res.text
    #print(response)
    js_data = json.loads(response)['data']['dataList']
    #print(js_data)
    savepath = os.getcwd() + r'\data'
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    fp = open(savepath + r'\DFCF_yhtj.csv', 'w', encoding='utf-8-sig', newline='')
    fw = csv.writer(fp)
    fw.writerow(['序号','推荐用户名','粉丝数量 '])
    i = 0
    src_security_code_dict = {}
    
    for item in js_data:
        i += 1
        xh = i       # 序号
        #zz = item['itemData']['title']         # 作者
        #print(zz)
        #gpdm = item['gubaId']                  # 股票代码
        #gpmc = item['securityName']            # 股票名称
        bt = item['nickName']                   #推荐用户名
        sj = item['follower']                   #粉丝数量 
        '''
        try:
            bt = item['itemData']['title']            # 标题
        except:
            try:
                bt = item['itemData']['postTopic'] 
            except:
                 bt = item['itemData']['questionContent'] #没有title找postTopic，还没有找questionContent
        
        #sj = item['itemData']['summary']               #内容
        try:   
            sj = item['itemData']['summary']           #内容
        except:
            pass
        '''
        content = [xh, bt, sj]
        #content = [xh, bt]
        print(content)
        fw.writerow(content)



# 爬取关注信息数据
getgz()   #爬取关注
getgztop2() #爬取关注top2，评论最多的2个
getrmht() #爬取热门话题
getgbrb() #爬取股吧热榜
getyhtj() #爬取用户推荐

#ut_fields ={'ut':'f057cbcbce2a86e2866ab8877db1d059','fields':'f14,f148,f3,f12,f2,f13','globalId':'786e4c21-70dc-435a-93bb-38'}
# 调用函数获取股票代码
#secids = getSecids(ut_fields)

# 调用函数获取股票数据，并保存到CSV文件中
#src_security_code_dict = getData(ut_fields, secids)

# 调用函数获取当前股票排名数据，并保存到CSV文件中
#getCurrentList(src_security_code_dict, ut_fields)

# 调用函数获取历史股票排名数据，并保存到CSV文件中
#getHisList(src_security_code_dict, ut_fields)