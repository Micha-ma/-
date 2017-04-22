import requests
import os
from bs4 import BeautifulSoup

#解析书籍的目录
def book_spider(menucode):
    soup = BeautifulSoup(menucode, 'lxml')
    menu = soup.find_all('div', {'class': 'bookyuanjiao', 'id': 'mulu'})
    soup2 = menu[0].ul
    bookMenu = []   #章节的标题
    bookMenuUrl = [] #章节对应的链接
    for i in range(1, len(soup2.contents) - 1):
        bookMenu.append(soup2.contents[i].string)
        if(soup2.contents[i].find('a')):    #针对部分书籍目录的标签不是a，没有href的情况
            bookMenuUrl.append(soup2.contents[i].a['href'])
        else:
            bookMenuUrl.append('Error!')
    return bookMenu, bookMenuUrl

url = 'http://www.shicimingju.com/book/'    #爬虫的原网页链接
mainmenu = requests.get(url).content.decode('utf-8')
mainsoup = BeautifulSoup(mainmenu, 'lxml')
mainpage = mainsoup.find('div', class_='bookyuanjiao')
#打开data.txt，其中保存了上次爬虫结束的节点，这些节点分别是书籍的编号、章节的编号以及段落的编号，实现断点爬取内容
with open('G:\\data.txt', 'r') as fd:
    data = fd.read().split()

flag = 1  #章节序号是否需要置0的标志
flag2 = 1 #段落序号是否需要置0的标志

bookList = [] #专题中的书籍
bookLink = [] #书籍对应的链接
for i in range(1, len(mainpage.ul.contents)-1):
    bookList.append(mainpage.ul.contents[i].get_text())
    bookLink.append(mainpage.ul.contents[i].a['href'])

#遍历专题中的书籍
for i in range(int(data[0]), len(bookLink)):
    #创建目录
    sub_folder = os.path.join('G:\\诗词名句\\', bookList[i])
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    #获取某本书籍的页面
    menucode = requests.get('http://www.shicimingju.com' + bookLink[i]).content.decode('utf-8')
    bookMenu, bookMenuUrl = book_spider(menucode)

    urlBegin = "http://www.shicimingju.com"
    #flag为0时，说明i+1,加载下一本书
    if flag == 0:
        data[1] = 0
    #遍历书籍中所有的章节
    for j in range(int(data[1]), len(bookMenuUrl)):

        if j == len(bookMenuUrl)-1:  #flag为0时，说明i+1,加载下一本书
            flag = 0

        if bookMenuUrl[j] == 'Error!':
            with open(sub_folder + '\\' + 'Reade.txt', 'a', encoding='utf8') as fr:
                fr.write("本书的章节源码没有href元素，不存在链接\n")
            continue
        chapterCode = requests.get(urlBegin + bookMenuUrl[j]).content.decode('utf-8') #获取每一章节的具体内容的网页源码
        chaptersoup = BeautifulSoup(chapterCode, 'lxml')
        chapterData = chaptersoup.find('div', {'id': 'con2'})
        chapterData = chapterData.find_all('p')

        # f.write(bookMenu[i])
        if chapterData == []:  #大部分的内容都在标签p内，不过水浒传例外
            with open(sub_folder + '\\' + 'Reade.txt', 'a', encoding='utf8') as fe:
                fe.write("网页解析错误，请查看源码，修改解析方法！\n")
            break
        #打开txt文件，保存内容
        f = open(sub_folder + '\\' + bookMenu[j] + '.txt', 'a', encoding='utf8')

        if flag2 == 0:#作用与flag相似
            data[2] = 0
        #遍历每一章节的所有段落
        for k in range(int(data[2]), len(chapterData)):
            '''
            #用这个方法，爬完一本，生成器抛出就不能再继续了
            chaptertext = chapterData[k].stripped_strings  # 该方法可以取出空格和空行，但返回一个生成器，故用next获取内容
            # print(next(chaptertext))
            f.write('    ')  # 原先是tab，8个空格，不习惯，改为4个空格
            try:
                f.write(next(chaptertext))
            except TypeError:
                break
                '''
            if k == len(chapterData)-1:
                flag2 = 0

            chaptertext = chapterData[k].string  # 加了strip（）,爬取速度慢很多，会出错
            if chaptertext:
                f.write(chaptertext)
            f.write('\n')
            #将结束时的3个序号写入data.txt
            with open('G:\\data.txt', 'w') as fd:
                fd.write(str(i) + ' ')
                fd.write(str(j) + ' ')
                fd.write(str(k))
        f.close()
