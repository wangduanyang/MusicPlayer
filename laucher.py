#!/usr/bin/env python
# encoding='utf-8'
import codecs
import json
import os
import sys
import platform
from threading import Thread

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFileDialog, QListWidgetItem, QMessageBox, QDialog
from PyQt4.phonon import Phonon

from SongModel import SongModel
import pycurl
from io import BytesIO
from xml.etree import ElementTree
print(sys.getdefaultencoding())
# reload(sys)
# enc = sys.getdefaultencoding()
# print(enc)
sysname = platform.system()
print(sysname)
# from main import Ui_MainWindow
basedir = os.path.split(os.path.abspath(__file__))[0]
print(basedir)
qtCreateFile = os.path.join(basedir, 'main.ui')
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreateFile)
qtCreateDiaSearchFile = os.path.join(basedir, 'diag_search.ui')
Ui_Dialog, QtBaseClass2 = uic.loadUiType(qtCreateDiaSearchFile)

class SearchDiag(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.flag = False
        self.pushButton_save_path.clicked.connect(self.set_save_path)
        self.lineEdit_save_path.setText(basedir)
        # self.connect(self.pushButton_accept, QtCore.SIGNAL('clicked()'), self.close)

    def set_save_path(self):
        dlg = QFileDialog(self)
        dir = dlg.getExistingDirectory(self,
                                            "选取文件夹",
                                            "/home/magicyang/Music",
                                            )
        print('save to ', dir)
        self.lineEdit_save_path.setText(dir)

    def accept(self):
        self.search_author = self.lineEdit_author.text()
        self.search_m_name = self.lineEdit_m_name.text()
        self.save_path = self.lineEdit_save_path.text()
        if(not self.search_author or not self.search_m_name or not self.save_path):
            msg = "作者，歌曲和保存路径都不能为空"
            msg_box = QMessageBox(QMessageBox.Information, "Info", msg)
            msg_box.exec_()
        else:
            self.flag = True
            self.close()



class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        # QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.songModel = SongModel()
        self.initPlaylist()#初始化播放列表
        self.player = Phonon.MediaObject()
        self.output = Phonon.AudioOutput(Phonon.MusicCategory)
        self.player.setCurrentSource(Phonon.MediaSource(self.url))
        Phonon.createPath(self.player, self.output)
        # Phonon.createPath(self.mediaObject, self.player)
        self.player.setTickInterval(1000)
        self.player.tick.connect(self.tock)
        self.pushButton_play.clicked.connect(self.play_clicked)#播放按钮单击信号
        self.player.stateChanged.connect(self.state_changed)#播放状态改变信号
        self.player.finished.connect(self.finished)#播放结束信号
        # Phonon.SeekSlider(self.player, self)#进度条
        # self.seekSlider2 = Phonon.SeekSlider(self)
        self.seekSlider2.setMediaObject(self.player)
        self.seekSlider2.setTracking(True)
        # self.seekSlider2.show()
        # self.listWidget.itemSelectionChanged.connect(self.item_changed)#列表选项改变信号
        self.listWidget.itemClicked.connect(self.item_clicked)#列表选项点击信号
        self.pushButton_open_files.clicked.connect(self.open_files)#打开文件
        self.pushButton_open_dir.clicked.connect(self.open_dir)#打开文件夹
        self.pushButton_remove.clicked.connect(self.remove_item) #移除当前选中
        self.volumeSlider.setAudioOutput(self.output)#音量控制器
        self.pushButton_sort.clicked.connect(self.sort)#排序
        self.pushButton_search.clicked.connect(self.search_music)#在线歌曲搜索
        self.init_btn_enabled()
        self.dst = os.path.join(basedir, 'tmp.txt')

    #判断网络情况
    def if_net_avalible(self):
        return1=os.system('ping 8.8.8.8 -c 1')
        #return1=os.system('ping 192.168.88.1 -c 2')
        if return1:
            print('ping fail')
            return False
        else:
            print('ping ok')
            return True

    #在线歌曲搜索
    def search_music(self):
        self.search_dial = SearchDiag(self)
        self.search_dial.setWindowTitle('在线歌曲搜索')
        self.search_dial.exec()
        # self.search_dial.show()
        print(self.search_dial.flag)
        if(self.search_dial.flag):
            #判断是否有网络连接
            if(not self.if_net_avalible()):
                msg = '网络不可达'
                msg_box = QMessageBox(QMessageBox.Information, 'Info', msg)
                msg_box.exec_()
                return False
            self.search_author = self.search_dial.search_author
            self.search_m_name = self.search_dial.search_m_name
            self.save_path = self.search_dial.save_path
            print(self.save_path)
            #百度music api
            url = "http://box.zhangmen.baidu.com/x?op=12&count=1&title="+\
                  self.search_m_name+"$$"+self.search_author+"$$$$"
            print(url)
            c = pycurl.Curl()
            burl = bytes(url, encoding='utf-8')
            #获取搜索结果
            c.setopt(c.URL, burl)
            b3 = BytesIO()
            c.setopt(c.WRITEFUNCTION, b3.write)
            c.perform()
            http_code = c.getinfo(pycurl.HTTP_CODE)
            if(http_code == 404):
                msg = '找不到服务器'
                msg_box = QMessageBox(QMessageBox.Information, 'Info', msg)
                msg_box.exec_()
                return False
            res = b3.getvalue().decode('utf-8')
            b3.close()
            print(res)
            root = ElementTree.fromstring(res)
            #获取count节点
            node_count = root.find('count')
            print(node_count.text)
            #有搜索结果
            if(node_count.text == '1'):
                #获取url节点
                node_url = root.find('url')
                print(node_url)
                #获取encode节点
                node_encode = node_url.find('encode')
                print(node_encode)
                print(node_encode.text)
                url_encode = node_encode.text
                #获取decode节点
                node_decode = node_url.find('decode')
                print(node_decode)
                print(node_decode.text)
                url_decode = node_decode.text

                url0 = url_encode.rsplit('/', 1)[0]
                print(url0)
                url_new = url0+'/'+url_decode
                print(url_new)
                #下载歌曲
                # burl_new = bytes(url_new, encoding='utf-8')
                c.setopt(c.URL, url_new)
                b4 = BytesIO()
                c.setopt(c.WRITEFUNCTION, b4.write)
                c.perform()
                res = b4.getvalue()
                b4.close()
                # print(res)
                #把mp3写入文件
                filename = self.search_author+'-'+self.search_m_name+'.mp3'
                path = os.path.join(self.save_path, filename)
                fn = codecs.open(path, 'wb')
                fn.write(res)
                fn.close()
                print('歌曲获取成功,保存至' + path)
                msg = '歌曲获取成功,保存至' + path
                msg_box = QMessageBox(QMessageBox.Information, "Info", msg)
                msg_box.exec_()
            else:
                msg = '未找到'+self.search_author+'的歌曲'+self.search_m_name
                msg_box = QMessageBox(QMessageBox.Information, "Info", msg)
                msg_box.exec_()

    #显示歌词
    def show_lrc(self, src):
        if(sysname == 'Linux'):
            self.GBK_2_UTF8(src, self.dst)
            lrc_file = open(self.dst)
        else:
            lrc_file = open(src)
        for line in lrc_file.readlines():
            if(line.strip() != ''):
                item = QListWidgetItem(line)
                self.listWidget_lrc.insertItem(self.listWidget_lrc.count(), item)

    #清除歌词
    def clr_lrc(self):
        i = 0
        while i < self.listWidget_lrc.count():
            self.listWidget_lrc.takeItem(i)

    def ReadFile(self, filePath, encoding="gbk"):
        with codecs.open(filePath,"r",encoding) as f:
            return f.read()

    def WriteFile(self, filePath,u,encoding="utf-8"):
        with codecs.open(filePath,"w",encoding) as f:
            f.write(u)

    def GBK_2_UTF8(self, src, dst):
        content = self.ReadFile(src, "gbk")
        self.WriteFile(dst,content, "utf-8")

    def finished(self):
        # print('finished')
        c_index = self.comboBox.currentIndex()
        #print(c_index)
        #单曲循环
        if(c_index == 1):
            # self.url = self.songModel.get_url(self.listWidget.item(self.listWidget.currentRow()+1).text())
            # print(self.url)
            self.player.play()
        #列表循环
        if(c_index == 2):
            # self.player.pause()
            c_row = self.listWidget.currentRow()
            # print(c_row)
            if(c_row != -1):
                self.listWidget.setCurrentRow((self.listWidget.currentRow()+1) % self.listWidget.count())
            else:
                self.url = self.listWidget.setCurrentRow(1)
            self.url = self.songModel.get_item(self.listWidget.item(self.listWidget.currentRow()).text())['url']
            self.lrc = self.songModel.get_item(self.listWidget.item(self.listWidget.currentRow()).text())['lrc']
            # print(self.url)
            self.player.setCurrentSource(Phonon.MediaSource(self.url))
            Phonon.createPath(self.player, self.output)
            self.player.play()
            self.clr_lrc()
            if(self.lrc):
                self.show_lrc(self.lrc)


    def sort(self):
        self.listWidget.sortItems(Qt.AscendingOrder)

    def init_btn_enabled(self):
         if(self.listWidget.count() == 0):
             self.pushButton_remove.setEnabled(False)
             self.pushButton_sort.setEnabled(False)
             self.pushButton_play.setEnabled(False)
         else:
             self.pushButton_sort.setEnabled(True)
             self.pushButton_play.setEnabled(True)
             if(self.listWidget.selectedItems()):
                self.pushButton_remove.setEnabled(True)
             else:
                self.pushButton_remove.setEnabled(False)

    def initPlaylist(self):
        # #清空列表
        # i = 0
        # while i < self.listWidget.count():
        #     self.listWidget.takeItem(i)
        #     i += 1
        # print(self.listWidget.count())
        songs = self.songModel.get_items()
        # print(songs)
        if(songs):
            #添加到播放列表
            for song in songs:
                #查找是否已存在item
                if (self.listWidget.findItems(song, Qt.MatchExactly) == []):
                    item = QListWidgetItem(song)
                    self.listWidget.insertItem(0, item)
                    # print(song)
            # c_item = QListWidgetItem(songs.pop())
            self.music = self.listWidget.item(0).text()
            self.url = self.songModel.get_item(self.music)['url']
            self.listWidget.setCurrentRow(0)
        else:
            self.url = None
         #更新按钮状态
        self.init_btn_enabled()

    def play_clicked(self):
        if self.player.state() == Phonon.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def state_changed(self, new, old):
        if new == Phonon.PlayingState:
            self.pushButton_play.setText('pause')
            self.statusBar.showMessage(self.music + ' is Playing')
        else:
            self.pushButton_play.setText('play')
            self.statusBar.showMessage('Pause')

    def tock(self, time):
        time = int(time)
        # print(time)
        time = (time//1000) #seconds total
        h = time//3600
        m = (time - 3600*h)//60
        s = (time - 3600*h - m*60)
        self.label_time.setText('%02d:%02d:%02d' % (h, m, s))

    def search_lrc(self, filename, lrc):
        #判断是否有网络连接
        if(not self.if_net_avalible()):
            msg = '网络不可达'
            # msg_box = QMessageBox(QMessageBox.Information, 'Info', msg)
            # msg_box.exec_()
            self.statusBar.showMessage(msg)
            return False
        #如果没有歌词就在线获取歌词
        # [author, name] = os.path.splitext(filename)[0].split('-')
        list = os.path.splitext(filename)[0].split('-')
        # print(author+':'+name)
        # print(repr(name))
        # url= BytesIO()
        print(list)
        if(len(list) == 2):
            author = list[0]
            name = list[1]
            print(name)
            url = 'http://geci.me/api/lyric/'+name+'/'+author
        else:
            name = os.path.splitext(filename)[0]
            url = 'http://geci.me/api/lyric/'+name
        burl =  bytes(url, encoding = "utf8")
        print(url)
        c = pycurl.Curl()
        #获取搜索结果
        c.setopt(c.URL, burl)
        # c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
        b = BytesIO()
        c.setopt(c.WRITEFUNCTION, b.write)
        c.perform()
        http_code = c.getinfo(pycurl.HTTP_CODE)
        print(http_code)
        # print(b.getvalue().decode('utf-8')
        res = b.getvalue().decode('utf-8')
        b.close()
        res_json = json.loads(res)
        print(res_json)
        count = res_json['count']
        # print(res_json['result'][0]['lrc'])
        if(http_code == 200):

            #根据搜索结果中的url获取歌词
            for i in range(0, count):
                b2 = BytesIO()
                # print(b.getvalue().decode('utf-8'))
                lrc_url = res_json['result'][i]['lrc']
                c.setopt(c.URL, lrc_url)
                c.setopt(c.WRITEFUNCTION, b2.write)
                c.perform()
                res = b2.getvalue().decode('utf-8')
                # print(res)
                b2.close()
                http_code = c.getinfo(pycurl.HTTP_CODE)
                print(http_code)
                # break
                if(http_code == 404):
                    continue
                elif(http_code == 200):
                    print('found')
                    print(res)
                    #把歌词写入文件
                    print(lrc)
                    fn = codecs.open(lrc, 'w', 'gbk')
                    fn.write(res)
                    fn.close()
                    print('歌词获取成功')
                    # msg_box = QMessageBox(QMessageBox.Information, "Info", "歌词获取成功")
                    # msg_box.exec_()
                    self.statusBar.showMessage('歌词获取成功')
                    return True
            else:
                print('找不到对应歌词')
                # msg_box = QMessageBox(QMessageBox.Information, "Info", "没有对应歌词")
                # msg_box.exec_()
                self.statusBar.showMessage('找不到对应歌词')
                return False
        else:
            print('连接歌词服务器失败')
            # msg_box = QMessageBox(QMessageBox.Information, "Info", "找不到歌词服务器")
            # msg_box.exec_()
            self.statusBar.showMessage('连接服务器失败')
            return False
        # print(self.contents)


    def open_files(self):
        dlg = QFileDialog(self)
        filepaths = dlg.getOpenFileNames(self,
                                              "多文件选择",
                                              "/home/magicyang/Music",
                                              "Mp3 Files (*.mp3)",
                                              )
        # self.statusBar.showMessage(filepaths)
        if(filepaths):
            for filepath in filepaths:
                filename = os.path.basename(filepath)
                filedir = os.path.split(os.path.abspath(filepath))[0]
                if(filename):
                    self.lrc = os.path.join(filedir, os.path.splitext(filename)[0] + '.lrc')
                    # print(self.lrc)
                    if(os.path.exists(self.lrc)):
                        dic = {'name':filename, 'url':filepath, 'lrc':self.lrc}
                        # msg_box = QMessageBox(QMessageBox.Information, "Info", "本地歌词")
                        # msg_box.exec_()
                    else:
                        # t = Thread(target=self.search_lrc, args=(filename, self.lrc))
                        if(self.search_lrc(filename, self.lrc)):
                            dic = {'name':filename, 'url':filepath, 'lrc':self.lrc}
                        else:
                            dic = {'name':filename, 'url':filepath, 'lrc':''}
                    self.songModel.put_item(dic)#添加到数据库
            #更新播放列表
            self.initPlaylist()
            self.music = self.listWidget.item(0).text()#获得首列表项
            self.url = self.songModel.get_item(self.music)['url']#获得首列表项url
            self.lrc = self.songModel.get_item(self.music)['lrc']#获得首列表项lrc
            self.player.setCurrentSource(Phonon.MediaSource(self.url))
            Phonon.createPath(self.player, self.output)
            self.player.play()
            if(self.lrc):
                self.show_lrc(self.lrc)
            #更新当前播放标签
            self.label_cur_song.setText(self.music)
            # #添加到播放列表
            # item = QListWidgetItem(self.filename)
            # self.listWidget.insertItem(0, item)

    # def curl_lyc_callback(self, buf):
    #     self.contents = ''
    #     self.contents = self.contents + buf

    def open_dir(self):
        dlg = QFileDialog(self)
        dir = dlg.getExistingDirectory(self,
                                            "选取文件夹",
                                            "/home/magicyang/Music",
                                            )
        self.walk_dir(dir)

    #遍历目录
    def walk_dir(self, root_dir):
        for parent, dirnames, filenames in os.walk(root_dir):
            for dirname in dirnames:
                self.walk_dir(os.path.join(parent, dirname))
            for filename in filenames:
                ext = os.path.splitext(filename)[1][1:]
                if(ext == 'mp3'):
                    self.lrc = os.path.join(parent, os.path.splitext(filename)[0] + '.lrc')
                    # print(self.lrc)
                    filepath = os.path.join(parent, filename)
                    if(os.path.exists(self.lrc)):
                        dic = {'name':filename,
                               'url': filepath,
                               'lrc':self.lrc}
                    else:
                        if(self.search_lrc(filename)):
                            dic = {'name':filename, 'url':filepath, 'lrc':self.lrc}
                        else:
                            dic = {'name':filename, 'url':filepath, 'lrc':''}
                            # dic = {'name':filename,
                            #        'url':os.path.join(parent, filename),
                            #        'lrc':''}
                    self.songModel.put_item(dic)#添加到数据库
        self.initPlaylist()

    # def item_changed(self):
    #     self.init_btn_enabled()
    #     c_item = self.listWidget.currentItem()
    #     if(c_item):
    #         item = c_item.text()
    #         # print(item)
    #         self.url = self.songModel.get_url(item)
    #         self.player.setCurrentSource(Phonon.MediaSource(self.url))
    #         Phonon.createPath(self.player, self.output)
    #         self.player.play()


    def item_clicked(self):
        self.init_btn_enabled()
        c_item = self.listWidget.currentItem()
        if(c_item):
            item = c_item.text()
            # print(item)
            self.music = item
            self.url = self.songModel.get_item(item)['url']
            self.lrc = self.songModel.get_item(item)['lrc']
            self.player.setCurrentSource(Phonon.MediaSource(self.url))
            Phonon.createPath(self.player, self.output)
            self.player.play()
            self.clr_lrc()
            print(self.lrc)
            if(self.lrc):
                self.show_lrc(self.lrc)
            #更新当前播放标签
            self.label_cur_song.setText(item)

    def remove_item(self):
        s_item = self.listWidget.selectedItems()
        for citem in s_item:
            item = citem.text()
            # print(item)
            self.songModel.remove_item(item)#从数据库中删除
            #takeitem
            self.listWidget.takeItem(self.listWidget.row(citem))
        #如果播放列表为空停止播放
        if(self.listWidget.count() == 0):
            self.player.pause()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
