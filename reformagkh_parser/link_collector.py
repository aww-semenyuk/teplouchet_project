#!/usr/bin/env python
# coding: utf-8

# ### Collecting links for search results from  www.reformagkh.ru.
# ### Saving to `links.txt`.
# ### `chromedriver.exe` must be in same folder.

from bs4 import BeautifulSoup
from selenium import webdriver
import requests


driver = webdriver.Chrome()
driver.delete_all_cookies()
driver.get('https://www.reformagkh.ru/search/houses-advanced')

driver.implicitly_wait(5)

# entering region in corresponding field
reg = driver.find_element_by_name('region')
reg.send_keys("Томская (обл)")

# selecting region from pop-up menu
reg_popup = driver.find_element_by_xpath('/html/body/ul/li/div')
reg_popup.click()

# clicking on settlement field in order to get a pop-up menu
sett = driver.find_element_by_name('settlement')
sett.click()

# selecting settlement from pop-up menu
sett_popup = driver.find_element_by_xpath('/html/body/ul[3]/li[5]/div')
sett_popup.click()

# clicking FIND button
find = driver.find_element_by_xpath(
    '/html/body/section[2]/div/div/div/form/div/button')
find.click()

# clicking on SHOW-BY field in order to get a pop-up menu
showby = driver.find_element_by_css_selector(
    '#paginatorForm > div > div > div > button')
showby.click()

# selecting '100' from pop-up menu
showby100 = driver.find_element_by_css_selector(
    '#bs-select-1 > ul > li:nth-child(4)')
showby100.click()

# list for links from every search result page
links = []

# while 'last page' button is present on the page (means that we aren't at last page)
while (len(driver.find_elements_by_css_selector(
        '#paginatorForm > div > ul > li.page-item.last-pagination')) != 0):
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # finding all elements with results links
    a_s = soup.find('body').find('section', class_='').table.find_all('a')

    # extracting the links
    links += [elem['href'] for elem in a_s]

    # clicking on 'next page' button
    nxt = driver.find_element_by_css_selector(
        '#paginatorForm > div > ul > li.page-item.next')
    nxt.click()

# working with last page with same approach
soup = BeautifulSoup(driver.page_source, 'lxml')
a_s = soup.find('body').find('section', class_='').table.find_all('a')
links += [elem['href'] for elem in a_s]

driver.close()

# formatting links and saving them to 'links.txt' file
links_new = ['https://www.reformagkh.ru' + l for l in links]
with open('links.txt', 'w') as file:
    file.write("\n".join(links_new))

print('Done! Check "links.txt"')
