### urllib库 
python自带的urllib库，urllib使用request去访问url，也可以用requests库获取其它库。
### 思路
模仿request请求去访问网页，避免让服务器知道时python脚本写的，重写user-agent，得到html的页面代码，使用BeauSoup把html的标签信息转换为python节点对象，对想要的信息转换为字符串使用正则表达式提取想要的信息，最后使用xlwt写入excel


### 模拟headers
模拟headers中的user-agent（伪装成浏览器访问）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201128215514147.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4ODcwMTQ1,size_16,color_FFFFFF,t_70)
### 访问豆瓣网返回html
伪造request，分别访问豆瓣网页html，将html的数据保留
```python
url="https://movie.douban.com/top250?start=22"
header = {
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}
request = urllib.request.Request(url, headers=header)
request2 = urllib.request.Request(url2, headers=header)
try:
    response = urllib.request.urlopen(request)
    response2 = urllib.request.urlopen(request2)
    # html = response.read().decode("utf-8")
except urllib.error.URLError as e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)
```

### BeautifuSoup获取html节点
应用正则表达式获取相应的节点信息
```python
findLink=re.compile(r'<a href="(.*?)">')  # 匹配规则 每一个a标签对应一部电影 获取链接
findImgSrc=re.compile(r'<img.*src="(.*?)"',re.S)# 匹配图片标签  re.忽略换行
findTitle=re.compile(r'<span class="title">(.*?)</span>')# 匹配span 片名
findScore=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')# 匹配评分
findJudge=re.compile(r'<span>(\d*?)人评价</span>')# 找到评价人数
findInfo=re.compile(r'<span class="inq">(.*?)</span>')# 描述
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)# 背景
```

### 获取豆瓣电影的信息并写入excel
```python
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
    for i in range(0,1):
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
```
### 过滤获取成功

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201129102923455.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4ODcwMTQ1,size_16,color_FFFFFF,t_70)
### 加入excel成功
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201129105407591.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4ODcwMTQ1,size_16,color_FFFFFF,t_70)
