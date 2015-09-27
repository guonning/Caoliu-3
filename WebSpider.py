#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import sys
import os
import datetime
import errno

class WebSpider:

    def __init__(self, startURL=''):
        self.header = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
        }
        self.startURL = startURL #开始URL

    #下载图片
    def saveImg(self, imgURL, imgName = '', savePath = ''):
        '''下载图片到本地
        @imgURL 图片的URL
        @imgName 保存名称
        @savePath 保存路径
        '''
        #构造默认存储路径
        urlBlock = imgURL.split('/')
        if imgName == '':
            imgName = urlBlock[-1]
        if savePath == '':
            savePath = os.getcwd() + '/img'
            for dir in urlBlock[3:-1]:
                savePath += '/' + dir
        filePath = savePath+'/'+imgName
        self.createDir(savePath)

        #下载保存图片
        request = requests.get(imgURL,stream=True)
        with open(filePath, 'wb') as fd:
            for chunk in request.iter_content():
                fd.write(chunk)
        print '图片: '+ filePath

    def createDir(self, dirPath):
        #创建目录
        try:
            os.makedirs(dirPath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dirPath):
                pass
            else: raise
        return

    def requests_get(self, url):
        try:
            return requests.get(url, headers = self.header)
        except requests.exceptions.ConnectionError as exc:
            return requests.get(url, headers = self.header)

if __name__ == '__main__':
    spider = WebSpider()
    spider.saveImg('https://www.baidu.com/img/bd_logo1.png', 'logo.png')

