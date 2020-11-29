import re,urllib,urllib.request
import requests,xlwt#写入excel
import random
from bs4 import BeautifulSoup


findLink=re.compile(r'<a href="(.*?)">')  # 匹配规则 每一个a标签对应一部电影 获取链接
findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S)# 匹配图片标签  re.忽略换行
findTitle=re.compile(r'<span class="title">(.*?)</span>')# 匹配span 片名
findScore=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')# 匹配评分
findJudge=re.compile(r'<span>(\d*?)人评价</span>')# 找到评价人数
findInfo=re.compile(r'<span class="inq">(.*?)</span>')# 描述
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)# 背景

def main():
    #豆瓣电影
    baseurl="https://movie.douban.com/top250?start="
    datalist=getData(baseurl)
    print(datalist)
    savepath="获取豆瓣电影表格.xls"
    savePath(datalist,savepath)#保存

def getData(baseurl):
    datalist=[] #抓取的结果返回
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askUrl(url)#逐个访问
        data=htmlData(html)#两层
        datalist.append(data)#添加变为三层
    #降级
    datalist=[x for y in datalist for x in y]#降一级
    return datalist

#解析html为soup节点对象
def htmlData(html):
    datalist = []
    soup = BeautifulSoup(html, "html.parser")  # 解析html
    for item in soup.find_all('div', class_="item"):
        data=[]
        item = str(item)  # 转化为字符串进行字符串的匹配
        link=re.findall(findLink,item)[0]
        data.append(link)
        imgsrc=re.findall(findImgSrc,item)[0]
        data.append(imgsrc)
        titles=re.findall(findTitle,item)
        if len(titles)==2:
            cn=titles[0]
            data.append(cn)
            en=titles[1].replace('/','')#把/替换
            en = "".join(en.split())#\xa0
            data.append(en)
        else:
            data.append(titles[0])
            data.append(" ")#加个空格
        score=re.findall(findScore,item)[0]
        data.append(score)
        judeNum=re.findall(findJudge,item)[0]
        data.append(judeNum)
        info=re.findall(findInfo,item)
        data.append(info[0])
        # if len(info)!=0:
        #     info=info[0].replace('.','')
        #     data.append(info)
        # else:
        #     data.append(' ')
        bd=re.findall(findBd,item)[0]
        bd=re.sub('<br(\s+)?/>(\s+)?','',bd)
        bd=re.sub('/',' ',bd)# 替换
        #\xa0的问题
        bd="".join(bd.split())#trip去掉前后空格拼接
        data.append(bd)#
        datalist.append(data)
    print(datalist)#打印获取的数据
    return datalist

def askUrl(url):
    # 模拟header
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    request = urllib.request.Request(url,headers=header)
    r=requests.get(url,headers=header)
    code=r.apparent_encoding
    r.code=code
    print(r.status_code)
    try:
        response = urllib.request.urlopen(request)
        html=""
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html


#-*- coding:utf-8 -*-
#加上编码格式
def savePath(datalist,savepath):#传入参数
    # return True
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)#创建workbook对象
    sheet=book.add_sheet("获取豆瓣电影投票250",cell_overwrite_ok=True)#创建工作表
    col=["电影详情链接","图片链接","中文名","英文名","评分",'评价数',"概述","背景"]
    length=len(datalist)
    print(length)
    for i in range(0,8):
        sheet.write(0,i,col[i])#添加属性列
    for i in range(0,length):#250条,会超出
        data=datalist[i]
        print(data)
        for j in range(0,8):
            print(data[j])
            sheet.write(i+1,j,data[j])#添加
    book.save(savepath)
    return True


#执行main
main()
