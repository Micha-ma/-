# -诗词名句上书籍爬虫案例
小白的python爬虫学习笔记的第一篇，水平有限，望看客见谅~
这个爬虫主要用到了requests,Beautifulsoup和os三个库，具体代码中有比较详细的注释。
这个爬虫程序的功能其实很简单，首先爬取网页上所有名著典籍的url，再逐个爬取典籍的所有章节，并将章节内容保存在本地。
这个爬虫的小亮点就是断点爬取书籍的功能（瞎琢磨），想到这个是因为初期调试程序的时候经常出错，导致一直重复的抓取下载已经成功的页面和数据。
如果对这个程序有什么建议，欢迎指点~~~
