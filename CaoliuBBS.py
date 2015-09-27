#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WebSpider import WebSpider
import requests
from lxml import etree
import os
import sys

class CaoliuBBSSpider(WebSpider):
    def __init__(self):
        startURL = 'http://cl.blos.pw/'
        WebSpider.__init__(self, startURL)
        self.forumList = self.getForumList()
        self.downFilePath = os.getcwd() + '/caoliu'

    def getForumList(self):
        ''' 获取板块列表
        '''
        print '>>>正在获取【栏目】...'
        indexHtml = self.requests_get(self.startURL+'index.php')
        indexHtml.encoding = 'gbk'
        indexTree = etree.HTML(indexHtml.text)
        forumList = indexTree.xpath("//*/tr[@class='tr3 f_one']")
        forumInfo = {}
        for forum in forumList:
            name = forum.xpath("*/h2/a/text()")
            url = forum.xpath('*/h2/a/@href')
            forumInfo[name[0]] = self.startURL + url[0]
            print '+ %s' % (name[0])
        print '< -----------------------------------------------:)'
        return forumInfo

    def getPostList(self, url):
        ''' 获取帖子列表
        '''
        postListHtml = self.requests_get(url)
        postListHtml.encoding = 'gbk'
        postListTree = etree.HTML(postListHtml.text)
        postList = postListTree.xpath('//*[@id="ajaxtable"]/*/*/*/h3/a')
        postInfoList = []
        for post in postList:
            name = post.xpath('text()')
            url = post.xpath('@href')
            if len(name) > 0 and len(url) > 0:
                postInfo = {'name':'', 'url':''}
                postInfo['name'] = name[0]
                postInfo['url'] = self.startURL + url[0]
                postInfoList.append(postInfo)
        return postInfoList

    def getPostContent(self, url):
        ''' 获取帖子内容
        '''
        postContentHtml = self.requests_get(url)
        postContentHtml.encoding = 'gbk'
        #print postContentHtml.text
        try:
            postContentTree = etree.HTML(postContentHtml.text)
            postMain = postContentTree.xpath('//*[@id="main"]')
            postContentList = postMain[0].xpath('//*[@class="tpc_content do_not_catch"]|//*[@class="tpc_content"]')
        except:
            postContentList = []
        return postContentList

    def getStory(self, postContents):
        story = ''
        for post in postContents:
            postTextList = post.xpath('text()')
            for postText in postTextList:
                if len(postText) > 18:
                    story += '    '
                    story += postText.strip()
                    story += '\n'
        return story

    def downStoryByUrl(self, storyUrl):
        storyDownloadPath = self.downFilePath + '/story'
        self.createDir(storyDownloadPath)
        storyList = self.getPostList(storyUrl)
        print '>>>正在下载【小说】...'
        for story in storyList:
            print '+ %s' % (story['name'])
            # 首页内容
            postContents = self.getPostContent(story['url'])
            storyText = self.getStory(postContents)
            # 其它页内容
            postID = story['url'].split('/')[-1].split('.')[0]
            pageNum = 2
            while len(postContents) > 0:
                pageUrl = '%sread.php?tid=%s&page=%d' % (self.startURL, postID, pageNum)
                postContents = self.getPostContent(pageUrl)
                storyText += self.getStory(postContents)+'\n\n'
                if self.isEndPage(pageUrl):
                    break
                pageNum += 1
            #写入文件
            if len(storyText) > 50:
                with open(storyDownloadPath+'/'+story['name'], 'wb') as file:
                    file.write(storyText)
        print '< -----------------------------------------------:)'
        return

    def downStory(self):
        page=1
        while True:
            #print '正在下载第%d页' % (page)
            storyurl = '%s&search=&page=%d' % (self.forumList[u'成人文學交流區'], page)
            self.downStoryByUrl(storyurl)
            if self.isEndPage(storyurl):
                break
            page += 1
        return

    def isEndPage(self, url):
        html = self.requests_get(url)
        htmlTree = etree.HTML(html.text)
        pageValueTag = htmlTree.xpath('//*[@class="pages"]/a/input/@value')
        try:
            pageValue = pageValueTag[0].split('/')
            #print pageValue[0],'/',pageValue[1]
            if pageValue[0] != pageValue[1]:
                return False
        except IndexError as EXC:
            pass
        return True

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    spider = CaoliuBBSSpider()
    spider.downStory()
