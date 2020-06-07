#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
import urllib.request
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Google
class GoogleThread(QThread):
    def __init__(self, copyright, search, result, driver_path, directory_path, cnt, parent=None): 
        QThread.__init__(self)
        self.copyright = copyright
        self.search = search
        self.result = result
        self.driver_path = driver_path.toPlainText()
        self.directory_path = directory_path.toPlainText()
        self.cnt = cnt.value()

    def run(self):
        self.result.setText(f'Chrome Browser를 시작합니다.\n잠시만 기다려주세요.')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        options.add_argument('--kiosk')
        browser = webdriver.Chrome(self.driver_path, chrome_options=options)
        
        browser.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ei=l1AdWbegOcra8QXvtr-4Cw&ved=0EKouCBUoAQ")
        elem = browser.find_element_by_xpath("//*[@class='gLFyf gsfi']") 
        elem.send_keys(self.search.text())
        elem.submit()
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[2]/div/div'))
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/c-wiz/div/div/div[2]/div/div[3]/div'))
        if self.copyright: 
            browser.execute_script("arguments[0].click();", browser.find_element_by_xpath(f'//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/c-wiz[1]/div/div/div[3]/div/a[{self.copyright}]/div'))
        try: 
            browser.find_element_by_css_selector('#islmp > div > div > p.M5HqZb')
            self.result.setText(f'검색어 \"{self.search.text()}\"와 일치하는 이미지 검색결과가 없습니다.')
        except:
            current_cnt = 1; ad_cnt = 0
            while current_cnt <= self.cnt:
                self.result.setText(f'현재 {current_cnt - ad_cnt}장의 이미지를 저장 중입니다.')
                try: element = browser.find_element_by_xpath(f'//*[@id="islrg"]/div[1]/div[{current_cnt}]/a[1]/div[1]/img')
                except: ad_cnt += 1
                else:
                    try: browser.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
                    except:
                        browser.execute_script("arguments[0].scrollIntoView();", element)
                        image = element.get_attribute('src')
                        urllib.request.urlretrieve(image, self.directory_path + '/' + str(current_cnt - ad_cnt) + ".jpg")
                finally: current_cnt += 1
                    
            if current_cnt - ad_cnt - 1 == self.cnt: self.result.setText(f'작업이 완료되었습니다.\n{current_cnt - ad_cnt - 1}장의 이미지가 저장되었습니다.')
            else: self.result.setText(f'작업이 완료되었습니다.\n검색된 이미지가 부족하여 {current_cnt - ad_cnt - 1}장의 이미지만 저장되었습니다.')
            
        finally: browser.quit()

# Naver
class NaverThread(QThread):
    def __init__(self, search, result, driver_path, directory_path, cnt, parent=None): 
        QThread.__init__(self)
        self.search = search
        self.result = result
        self.driver_path = driver_path.toPlainText()
        self.directory_path = directory_path.toPlainText()
        self.cnt = cnt.value()

    def run(self):
        self.result.setText(f'Chrome Browser를 시작합니다.\n잠시만 기다려주세요.')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        options.add_argument('--kiosk')
        browser = webdriver.Chrome(self.driver_path, chrome_options=options)
        
        browser.get("https://search.naver.com/search.naver?where=image&amp;sm=stb_nmr&amp;")
        elem = browser.find_element_by_xpath('//*[@id="nx_query"]') 
        elem.send_keys(self.search.text())
        elem.submit()
        
        try: 
            browser.find_element_by_css_selector('#notfound')
            self.result.setText(f'검색어 \"{self.search.text()}\"와 일치하는 이미지 검색결과가 없습니다.')
        except:
            current_cnt = 1
            for i in range(2, 13):
                for j in range(50 if i == 2 or i == 12 else 100):
                    try: 
                        if i == 7 and not j: browser.find_element_by_xpath('//*[@id="_sau_imageTab"]/div[2]/div[8]/a').click()
                    except: break
                    
                    self.result.setText(f'현재 {current_cnt}장의 이미지를 저장 중입니다.')
                    try: 
                        element = browser.find_element_by_xpath(f'//*[@id="_sau_imageTab"]/div[2]/div[{i}]/div[{j+1}]/a[1]/img')
                        browser.execute_script("arguments[0].scrollIntoView();", element)
                        image = element.get_attribute('src')
                        urllib.request.urlretrieve(image, self.directory_path + '/' + str(current_cnt) + ".jpg")
                    except: break
                    if current_cnt >= self.cnt: break
                    current_cnt += 1
                if current_cnt >= self.cnt: break

            if current_cnt == self.cnt: self.result.setText(f'작업이 완료되었습니다.\n{current_cnt}장의 이미지가 저장되었습니다.')
            else: self.result.setText(f'작업이 완료되었습니다.\n검색된 이미지가 부족하여 {current_cnt - 1}장의 이미지만 저장되었습니다.')
                
        finally: browser.quit()
    
# Bing
class BingThread(QThread):
    pass

# UI
class Image_Scrapper(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('Image_Scrapper.ui', self)
        self.ui.show()
        # 어플리케이션 이름
        self.setWindowTitle('Image Scrapper')
        # 어플리케이션 아이콘
        self.setWindowIcon(QtGui.QIcon('app_icon.jpg'))
        # github 이미지
        self.github.setStyleSheet('image:url(github.png);border:0px;')
        # driver 경로 text browser
        self.driver_path.clear()
        # 저장 경로 text browser
        self.directory_path.clear()
        # 검색어 line edit
        self.search.clear()
        
        # driver 경로 버튼 클릭
        self.select_driver.clicked.connect(self.select_driver_clicked)
        # 저장 경로 버튼 클릭
        self.select_folder.clicked.connect(self.select_folder_clicked)
        # 사진 저장 버튼 클릭
        self.download.clicked.connect(self.download_clicked)
        # engine radio 선택
        self.google.clicked.connect(self.radio_clicked)
        self.naver.clicked.connect(self.radio_clicked)
        self.bing.clicked.connect(self.radio_clicked)
        # copyright box 잠금
        self.copyright_box.setEnabled(False)
        # copyright radio 선택
        self.google_0.clicked.connect(self.copyright_clicked)
        self.google_1.clicked.connect(self.copyright_clicked)
        self.google_2.clicked.connect(self.copyright_clicked)
        self.google_3.clicked.connect(self.copyright_clicked)
        self.google_4.clicked.connect(self.copyright_clicked)
        # github 버튼 클릭
        self.github.clicked.connect(self.github_clicked)
        
    # driver 경로 버튼 클릭 시 동작
    def select_driver_clicked(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()[0]
        print(fname)
        self.driver_path.setPlainText(fname)
        
    # 저장 경로 버튼 클릭 시 동작
    def select_folder_clicked(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory()
        self.directory_path.setPlainText(fname)
    
    # 사진 저장 버튼 클릭 시 동작
    def download_clicked(self):
        if not self.search.text(): QtWidgets.QMessageBox.about(self, '경고', "검색어를 입력하세요.")
        elif not self.directory_path.toPlainText(): QtWidgets.QMessageBox.about(self, '경고', "저장 경로를 선택하세요.")
        else:
            select_engine = [i.isChecked() for i in self.engine_box.children()]
            if not select_engine.count(True): QtWidgets.QMessageBox.about(self, '경고', "검색 엔진을 선택하세요.")
            elif select_engine.index(True) == 0: 
                select_copyright = [i.isChecked() for i in self.copyright_box.children()]
                if not select_copyright.count(True): QtWidgets.QMessageBox.about(self, '경고', "Google 이미지 사용권을 선택하세요.")
                else:
                    # google thread
                    self.googlethread = GoogleThread(select_copyright.index(True), self.search, self.result, self.driver_path, self.directory_path, self.cnt)
                    self.googlethread.start()
            elif select_engine.index(True) == 1: 
                self.naverthread = NaverThread(self.search, self.result, self.driver_path, self.directory_path, self.cnt)
                self.naverthread.start()
            elif select_engine.index(True) == 2: 
                self.bingthread = BingThread(self.search, self.result, self.driver_path, self.directory_path, self.cnt)
                self.bingthread.start()

    # engine radio 선택 시 동작
    def radio_clicked(self, engine):
        if self.google.isChecked():
            self.copyright_box.setEnabled(True)
        else:
            reply = QtWidgets.QMessageBox.question(self, '경고', '저작권 문제가 있을 수 있습니다.\n계속 진행하시겠습니까?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                self.google.setChecked(True)
                self.copyright_box.setEnabled(True)
            else:
                self.copyright_box.setEnabled(False)
            
    # copyright radio 선택 시 동작
    def copyright_clicked(self, n):
        if self.google_0.isChecked():
            reply = QtWidgets.QMessageBox.question(self, '경고', '저작권 문제가 있을 수 있습니다.\n계속 진행하시겠습니까?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                self.google_1.setChecked(True)
    
    # github 버튼 클릭 시 동작
    def github_clicked(self):
        import webbrowser
        webbrowser.open('https://github.com/IllIIIllll/image_scrapper')
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Image_Scrapper()
    app.exec_()

