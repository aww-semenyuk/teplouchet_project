#!/usr/bin/env python
# coding: utf-8

# ### Parsing collected links for www.reformagkh.ru from `links.txt` file.
# ### Saving to `inhabitants.csv`.
# ### Make sure that `Tor Browser` is running all the time.

from stem import Signal
from stem.control import Controller

from bs4 import BeautifulSoup
import requests

from tqdm import tqdm

import pandas as pd
import numpy as np


def change_proxy():
    """
    This function enables us to change the address from which requests are sent.
    It is required to avoid being blocked for multiple requests from one address
    which is considered as spam.
    """
    with Controller.from_port(port=9151) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)


proxy = {'http': 'socks5://127.0.0.1:9150',
         'https': 'socks5://127.0.0.1:9150'}

# load links that were collected previously
links = []
with open('links.txt', 'r') as lnks:
    links = lnks.read().splitlines()

# dict to save parsed info in 'address:info' format
# this program only collects info about the number of inhabitants
add_to_num_dict = dict()

for link in tqdm(links):
    change_proxy()  # changing address from which request will be sent
    source = requests.get(link, proxies=proxy).text  # loading page's html
    soup = BeautifulSoup(source, 'lxml')  # converting html text to BeautifulSoup object

    # if the page is unavaliable, move on to the next one
    if soup.find(class_='error_code'):
        continue

    # getting building's address
    address = soup.find(
        class_='folder-description').find(class_='text-white').text

    # if the info about the number of inhabitants is present, saving it to out dict
    # else, filling with NaN
    if soup.find(text='Численность жителей, чел.'):
        number = soup.find(text='Численность жителей, чел.').parent.parent.find(class_='').text
        add_to_num_dict.update({address: number})
    else:
        add_to_num_dict.update({address: np.nan})

# converting the dict to pandas DataFrame
df = pd.DataFrame(list(add_to_num_dict.items()),
                  columns=['Address', 'Inhabitants'])

df["Inhabitants"] = pd.to_numeric(df["Inhabitants"])

# saving DataFrame as csv file
df.to_csv('inhabitants.csv', index=False, sep=';', encoding='cp1251')

print('Done! Check "inhabitants.csv"')
