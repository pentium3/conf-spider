from bs4 import BeautifulSoup
import requests

# https://mp.weixin.qq.com/s?__biz=MzU5MTM5MTQ2MA==&mid=2247485254&idx=1&sn=64c1e0f3360daecdc7a7b033aedcb40a&chksm=fe2ef8cdc95971db84e960bf4528cc22342d73a0c3a81240bf054128b3232ab0467977d43baa&mpshare=1&scene=1&srcid=11077Rk7l668kJs4ZcsNWRQ4&sharer_sharetime=1604926307289&sharer_shareid=9e6cb69be846e73fca0b8a3ae617f26b&key=9f9748e97f7020ea0b010e2838d9f64f4c34133971e7d96b560921c812903a510d24156f7ed21917dbc74f005e5ece8bfb8a438e312679a08953b79250e1440b55c65d11e93ccd3d3bc0ce3079d3136d1bc76897752bb95b56afd98330b7ef7dcd8c96acc9f4e9d6aef823fb02c375c533e58e79dcae4ed0762d8766e4bb67d5&ascene=1&uin=NzczMTcxOTQ0&devicetype=Windows+7+x64&version=6300002f&lang=en&exportkey=AS6JqP3vj82WwnNUyTz%2FPWA%3D&pass_ticket=E6PLq8xKmzNbSCZvAyil3Tmw9DLyAJwyftOCF%2F91sY25EQotxh8G%2Ff4J22BHvi1C&wx_header=0


dlist=[
'https://dblp.uni-trier.de/db/conf/sosp/sosp2019.html',
'https://dblp.uni-trier.de/db/conf/eurosys/eurosys2020.html',
'https://dblp.uni-trier.de/db/conf/cloud/socc2018.html',
'https://dblp.uni-trier.de/db/conf/sigmod/sigmod2020.html',
]

ulist=[
'https://www.usenix.org/conference/atc20/',
'https://www.usenix.org/conference/osdi20/',
'https://www.usenix.org/conference/nsdi20/',
]

def getHTMLText(url):
    try:
        r= requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding= r.apparent_encoding
        return r.text
    except:
        return "getHTMLText error!"

def getdblp(_url):
    html= getHTMLText(_url)
    soup= BeautifulSoup(html, 'html.parser')
    paper_url_list= []
    for content in soup.find_all('a'):
        url= content.get('href')
        if (url!=None) and (url[0:16]=='https://doi.org/'):
            paper_url_list.append(url)
    paper_url_list= list(set(paper_url_list))
    # for url in paper_url_list:
    #     print(url)
    print(len(paper_url_list))
    return(paper_url_list)

def getusenix(_url):
    html= getHTMLText(_url+'technical-sessions')
    soup= BeautifulSoup(html, 'html.parser')
    paper_url_list= []
    for content in soup.find_all('a'):
        url= content.get('href')
        if (url!=None) and ('presentation' in url):
            paper_url_list.append('https://www.usenix.org'+url)
    paper_url_list= list(set(paper_url_list))
    # for url in paper_url_list:
    #     print(url)
    print(len(paper_url_list))
    return(paper_url_list)

def absdoi(_url):
    html= getHTMLText(_url)
    soup= BeautifulSoup(html, 'html.parser')
    ll=[]
    for _i,cnt in enumerate(soup.find_all(name='div', attrs={'class':'abstractSection abstractInFull'})):
        cnt=str(cnt).replace('<div class="abstractSection abstractInFull"><p>','').replace('</p></div>','').replace('\n',' ')
        ll.append(cnt)
    return(ll[0])

def titledoi(_url):
    html= getHTMLText(_url)
    soup= BeautifulSoup(html, 'html.parser')
    ll=[]
    for _i,cnt in enumerate(soup.find_all(name='h1')):
        cnt=str(cnt).replace('<h1 class="citation__title">','').replace('</h1>','')
        ll.append(cnt)
    return(ll[0])

def absusenix(_url):
    html= getHTMLText(_url)
    soup= BeautifulSoup(html, 'html.parser')
    ll=[]
    for _i,cnt in enumerate(soup.find_all(name='div', attrs={'class':'field-item odd'})):
        cnt=str(cnt).replace('<div class="field-item odd"><p>','').replace('</p></div>','').replace('\n',' ')
        ll.append(cnt)
    return(ll[1])

def titleusenix(_url):
    html= getHTMLText(_url)
    soup= BeautifulSoup(html, 'html.parser')
    ll=[]
    for _i,cnt in enumerate(soup.find_all(name='h1')):
        cnt=str(cnt).replace('<h1 id="page-title">','').replace('</h1>','')
        ll.append(cnt)
    return(ll[0])


for uu in ulist:
    urls=getusenix(uu)
    for url in urls:
        abst=titleusenix(url)
        print(url,abst)

for uu in dlist:
    urls=getdblp(uu)
    for url in urls:
        abst=titledoi(url)
        print(url,abst)
