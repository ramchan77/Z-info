from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.common.proxy import Proxy,ProxyType
import time
import cookielib
import requests
import csv
import xlsxwriter
from xlutils.copy import copy
from xlrd import open_workbook
import sys

input_file_name1 = sys.argv[1]
input_file_name=input_file_name1+'.csv'
print 'Input File Nmae : '+input_file_name
#output_file_name = raw_input("Enter The file Name (with xls Extention ) : ")
output_file_name=input_file_name1+'_output.xls'
print 'Output File Nmae : '+output_file_name
workbook = xlsxwriter.Workbook(output_file_name)
worksheet = workbook.add_worksheet()
workbook.close()
book_ro = open_workbook(output_file_name)
book = copy(book_ro)
sheet1 = book.get_sheet(0)
count=0
roww=0
coll=0
#page_content=''
print 'Launching Chrome..'
#prox = Proxy()
#prox.proxy_type = ProxyType.MANUAL
#prox.http_proxy = "127.0.0.1:9667"
#prox.socks_proxy = "127.0.0.1:9667"
#prox.ssl_proxy = "127.0.0.1:9667"
#capabilities = webdriver.DesiredCapabilities.CHROME
#prox.add_to_capabilities(capabilities)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
browser = webdriver.Chrome(executable_path='C:\Users\lenovo\Desktop\python\chromedriver.exe',chrome_options=options,desired_capabilities=capa)
print 'Waiting for 2 mins...'
time.sleep(90)
print 'Entering to zoominfo...'
with open(input_file_name, "r") as f:
    reader=csv.reader(f)
    for row in reader:
        site = row[0]
        checker={'value': 1}
        attempt_count={'value': 1}
        count+=1
        def page_l():
            if attempt_count['value']<3:
               try:
                   time.sleep(2)
                   browser.get(site)
                   wait = WebDriverWait(browser, 15)
                   wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[2]/section[1]")))
                   browser.execute_script("window.stop();")
               except TimeoutException:
                   attempt_count['value']+=1
                   page_l()
            else:
                pass
        try:
            time.sleep(2)
            browser.get(site)
            wait = WebDriverWait(browser, 15)
            wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[2]/section[1]")))
            browser.execute_script("window.stop();")
        except TimeoutException:
            page_l()
        #time.sleep(3)
        el_count={'value': 1}
        el_count1={'value': 1}
        def element_fun():
            try:
                elements=browser.find_element_by_xpath("/html/body/div/div[2]/section[1]")
                checker['value']=0
                #page_content=browser.find_element_by_xpath("/html/body/div/div[2]/section[1]").get_attribute("outerHTML")
            except NoSuchElementException:
                if el_count['value']<2:
                    el_count['value']+=1
                    print '~~~~~~~~Waiting For 10 Seconds~~~~~~~~~~'
                    #time.sleep(8)
                    page_l()
                    element_fun()
                elif (el_count['value']==2) and (el_count1['value']==1):
                    print '~~~~~~~~Retrying~~~~~~~~~~'
                    el_count['value']=1
                    el_count1['value']+=1
                    try:
                        time.sleep(2)
                        browser.get(site)
                        wait = WebDriverWait(browser, 15)
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[2]/section[1]")))
                        browser.execute_script("window.stop();")
                        element_fun()
                    except TimeoutException:
                        pass
                        #element_fun()
                #page_content=browser.find_element_by_xpath("/html/body/div/div[2]/section[1]").get_attribute("outerHTML")
        try:
            element_fun()
        except TimeoutException:
            page_l()
            element_fun()
        if checker['value']==0:
            #print str(count)+' '+site
            try:
                elems=browser.find_elements_by_class_name("readMore_links")
                for elem in elems:
                    try:
                        elem.click()
                    except:
                        continue
            except:
                pass
            page_content=browser.find_element_by_xpath("/html/body/div/div[2]/section[1]").get_attribute("outerHTML")
            if page_content!='<section></section>':
                print str(count)+' '+site
                sheet1.write(roww,coll,page_content)
                sheet1.write(roww,coll+1,site)
                roww+=1
                book.save(output_file_name)
            else:
                time.sleep(5)
                print 'Access Denied... Waiting for 10 seconds...'
                try:
                    browser.get(site)
                    wait = WebDriverWait(browser, 15)
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[2]/section[1]")))
                    browser.execute_script("window.stop();")
                    element_fun()
                except TimeoutException:
                    page_l()
                    element_fun()
        else:
            print str(count)+' *** '+site+' *** Element Not Found'
            pass
print 'Closing Chrome..'
browser.close()
