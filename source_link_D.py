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

#input_file_name = raw_input("Enter The Input file Name (with csv Extention ): ")
start_url=int(sys.argv[1])
temp=start_url%5000
end_url=(start_url-temp)+5000
print 'Starting Source Number : '+str(start_url)
print 'It Will Run Upto : '+str(end_url)
#end_url=input("Enter The Rabge Limit URL Count (just Enter The Integer ) : ")
#output_file_name = raw_input("Enter The file Name (with xls Extention ) : ")
output_file_name ='Source_'+str(end_url-5000)+'.xls'
print 'Output File Name : '+output_file_name
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
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
browser = webdriver.Chrome(executable_path='C:\Users\lenovo\Desktop\python\chromedriver.exe',desired_capabilities=capa)
print 'Waiting for 2 mins...'
time.sleep(90)
print 'Entering to zoominfo...'
#with open(input_file_name, "r") as f:
    #reader=csv.reader(f)
for i in range(start_url,end_url):
    site = 'https://www.zoominfo.com/people_directory/professional_profile/E-2-'+str(i)
    checker={'value': 1}
    attempt_count={'value': 1}
    attempt_count1={'value': 1}
    count+=1
    def page_l1():
        if attempt_count1['value']<3:
            try:
                browser.get(page_content)
                wait = WebDriverWait(browser, 15)
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div[2]/div/div/div[1]/a")))
                browser.execute_script("window.stop();")
            except TimeoutException:
                attempt_count1['value']+=1
                page_l1()
        else:
            pass
    def page_l():
        if attempt_count['value']<3:
            try:
                browser.get(site)
                wait = WebDriverWait(browser, 15)
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div[2]")))
                #time.sleep(6)
                browser.execute_script("window.stop();")
            except TimeoutException:
                attempt_count['value']+=1
                page_l()
        else:
            pass
            #continue
    #time.sleep(2)
    try:
        browser.get(site)
        wait = WebDriverWait(browser, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div[2]")))
        browser.execute_script("window.stop();")
    except TimeoutException:
        page_l()
    el_count={'value': 1}
    el_count1={'value': 1}
    def element_fun():
        try:
            elements=browser.find_element_by_xpath("/html/body/section[1]/div[2]")
            checker['value']=0
            #page_content=browser.find_element_by_xpath("/html/body/div/div[2]/section[1]").get_attribute("outerHTML")
        except NoSuchElementException:
            if el_count['value']<2:
                el_count['value']+=1
                print '~~~~~~~~Waiting For 10 Seconds~~~~~~~~~~'
                #browser.get(site)
                #time.sleep(6)
                #wait = WebDriverWait(browser, 15)
                #wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div[2]")))
                #browser.execute_script("window.stop();")
                page_l()
                element_fun()
            elif (el_count['value']==2) and (el_count1['value']==1):
                print '~~~~~~~~Retrying~~~~~~~~~~'
                el_count['value']=1
                el_count1['value']+=1
                try:
                    browser.get(site)
                    wait = WebDriverWait(browser, 15)
                    #time.sleep(6)
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div[2]")))
                    browser.execute_script("window.stop();")
                    element_fun()
                except TimeoutException:
                    pass
            #page_content=browser.find_element_by_xpath("/html/body/div/div[2]/section[1]").get_attribute("outerHTML")
    element_fun()
    if checker['value']==0:
        print str(count)+' '+site
        page_content_check=browser.find_element_by_xpath("/html/body/section[1]/div[2]").get_attribute("outerHTML")
        if page_content_check!='<section></section>':
            #elems=browser.find_elements_by_xpath("/html/body/section[1]/div[2]/div/div/p/a")
            elems=[link.get_attribute('href') for link in browser.find_elements_by_xpath("/html/body/section[1]/div[2]/div/div/p/a")]
            #print elems
            for elem in elems:
                page_content=elem #.get_attribute("href")
                #sheet1.write(roww,coll,page_content)
                #sheet1.write(roww,coll+1,site)
                #roww+=1
                #book.save(output_file_name)
                url_check=page_content[25:27]
                #print url_check
                if url_check=='pe':
                    try:
                        browser.get(page_content)
                        #time.sleep(6)
                        wait = WebDriverWait(browser, 15)
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div[2]/div/div/div[1]/a")))
                        browser.execute_script("window.stop();")
                        element_fun()
                    except TimeoutException:
                        page_l1()
                        element_fun()
                    if checker['value']==0:
                        elems1=browser.find_elements_by_xpath("/html/body/section[1]/div[2]/div/div/div[1]/a")
                        for elem1 in elems1:
                            people_link=elem1.get_attribute("href")
                            sheet1.write(roww,coll,site)
                            sheet1.write(roww,coll+1,people_link)
                            roww+=1
                            book.save(output_file_name)
                            #print people_link
                        browser.back()
                        time.sleep(2)
                elif url_check=='p/':
                    #print page_content
                    sheet1.write(roww,coll,site)
                    sheet1.write(roww,coll+1,page_content)
                    roww+=1
                    book.save(output_file_name)


        else:
            time.sleep(10)
            try:
                browser.get(site)
                #time.sleep(5)
                wait = WebDriverWait(browser, 15)
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/section[1]/div[2]")))
                browser.execute_script("window.stop();")
                element_fun()
            except TimeoutException:
                continue
    else:
        print str(count)+' *** '+site+' *** Element Not Found'
        pass
print 'Closing Chrome..'
browser.close()
