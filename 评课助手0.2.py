import requests
import re
import time

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding =r.apparent_encoding
        return r.text
    except:
        return "OpenError"

def NumPage(url):
    html=getHTMLText(url)
    try:
        numlt=re.findall(r'page=',html)
        return len(numlt)
    except:
        print("NumError")
    
def parsePage(ilt, html,couse):
    try:
        slt=re.findall(r'rl-pd-sm h4">\d.\d',html)
        nlt = re.findall(r'（[\u4e00-\u9fa5]+',html)
        del nlt[0]
        tlt = re.findall(r'small text-muted">20\d{2}[\u4e00-\u9fa5]',html)
        nanlt=re.findall(r'难度：[\u4e00-\u9fa5]+',html)
        zuolt=re.findall(r'多少：[\u4e00-\u9fa5]+',html)
        geilt=re.findall(r'好坏：[\u4e00-\u9fa5]+',html)
        shoult=re.findall(r'大小：[\u4e00-\u9fa5]+',html)
        for i in range(len(nlt)):
            name = nlt[i]
            time = tlt[i].split('>')
            star=slt[i].split('>')
            nan=nanlt[i].split('：')
            zuo=zuolt[i].split('：')
            gei=geilt[i].split('：')
            shou=shoult[i].split('：')
            ilt.append([name[1:],time[1],star[1],nan[1],zuo[1],gei[1],shou[1]])
    except:
        print("GetError：（1）输出异常（2）部分评课信息缺失")

def printGoodsList(ilt):
    tplt = "{:2}\t{:2}\t{:2}\t{:2}\t{:2}\t{:2}\t{:2}\t{:2}"
    print(tplt.format("[序号]", "[教师]","[时间]","[评分]","[难度]","[作业]","[给分]","[收获]"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1],g[2],g[3],g[4],g[5],g[6]))
        
def main():
    course = input('输入查询课程：')
    start=time.perf_counter()
    start_url = 'https://www.icourse.club/search/?q=' +course
    depth = NumPage(start_url)
    infoList = []
    for i in range(depth):
        try:
            if i==0:
                url = start_url
            else:
                url = start_url + '&term=&page='+str(i+1)
            html = getHTMLText(url)
            parsePage(infoList, html,course)
        except:
            print('Error')
            continue
    printGoodsList(infoList)
    end=time.perf_counter()
    print("程序结束，用时{:.3f}s".format(end-start))
main()
