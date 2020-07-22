import requests
from bs4 import BeautifulSoup

def geturl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Referer':'https://www.baidu.com'
    }
    # 'Referer': 'https://www.mzitu.com/221181'
    req=requests.get(url,headers=headers)


    return req,req.text


#         request=http.request("GET",
def getsoup(text):
    soup=BeautifulSoup(text,"html.parser")
    a_url=soup.findAll('a')
    img_url=soup.findAll('img')
    num=0
    img=dict()
    for i in img_url:
        if i.get('data-original'):
            img[num]={'name':i.get('alt'),'href':i.parent.get('href'),'pho_url':i.get('data-original'),'state':0}
            num+=1
        else:
            img[num] = {'name': i.get('alt'), 'href': i.parent.get('href'), 'pho_url': i.get('src'), 'state': 1}
            num += 1
            pass
        #print(i.get('alt'))
    return img
def Download_img(img_dict):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
        }
    headers['Referer']=img_dict['href']
    req = requests.get(img_dict['pho_url'], headers=headers)
    print("=")
    img_dict['name']=img_dict['name'].replace('?','')
    img_dict['name']=img_dict['name'].replace(' ', '')
    img_dict['name']=img_dict['name'].replace('!','')
    img_dict['name']=img_dict['name'].replace('！', '')
    img_dict['name']=img_dict['name'].replace('？', '')
    try:
        with open("img/"+img_dict['name']+'.jpg', 'wb+') as f:
            f.write(req.content)
    except OSError:
        print('Error')
    pass
#     with open('name', 'wb') as f:
#         f.write(req.content)
def getTxt(url):

    state, text = geturl(url)
    print(state)
    if str(state)!='<Response [200]>':
        print("error")
    else:
        img_txt=getsoup(text)
        if img_txt:
            for i in img_txt:
                Download_img(img_txt[i])
if __name__ == '__main__':
    url='https://www.mzitu.com'
    # url='https://urllib3.readthedocs.io/en/latest/'
    # http = urllib.PoolManager();
    # request = http.request("GET", url)
    # print(request.status)
    for i in range(251):
        print('第',i,'页')
        getTxt('https://www.mzitu.com/page/'+str(i+1)+'/')
