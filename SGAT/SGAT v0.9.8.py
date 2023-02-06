from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

import pandas as pd
from time import sleep
import os
import matplotlib.pyplot as plt
import numpy as np

import tkinter.messagebox as mb
from idlelib.tooltip import Hovertip
from tkinter import ttk
from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import CENTER
from tkinter import PhotoImage
from tkinter import END
from tkinter import Radiobutton
from tkinter import IntVar
from tkinter import LabelFrame
from tkinter import filedialog
from tkinter.ttk import Notebook, Style
import tkinter as tk    

import math
import time
from datetime import datetime
from tqdm import tqdm

import random

import nltk
from nltk.tokenize import word_tokenize 
import string

from wordcloud import WordCloud

from nltk.stem import WordNetLemmatizer
import pymorphy2

import re 

import requests
import json

from natasha import (Segmenter,MorphVocab,LOC,AddrExtractor,DatesExtractor)

def info():

    options = webdriver.ChromeOptions() 
    options.add_argument('--headless')
    ran = random.random()
    options.add_argument("--user-agent="+str(ran)+"")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--disable-3d-apis")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    chrome = pyt_Input.get()
    zap = zap_Input.get()
    im = im_Input.get()
    muz = muz_Input.get()

    global img
    try:
        img = open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[5]

    except FileNotFoundError:
        open("autofill_scraping.txt", "w+")
        img = ''
    except IndexError:
        img = ''

    s = Service(r''+chrome+'\\chromedriver') 
    driver = webdriver.Chrome(service=s, options=options)

    url = 'https://goskatalog.ru/portal/#/collections?q='+zap+'&museumIds='+muz+'&imageExists='+img+''

    driver.get(url)

    gg = 0
    while (gg==0):
        try:

            chis = driver.find_element(By.XPATH,'/html/body/article/ui-view/div/div[2]/div/div[2]').text

            if chis == 'Количество вычисляется...' or '':
                sleep(0.1)
            else:
                print(chis)
                gg = 1  

        except NoSuchElementException:
            gg=0
        except StaleElementReferenceException:
            gg=0

    mb.showinfo('Результат', chis)


def museums():

    options = webdriver.ChromeOptions() 
    options.add_argument('--headless')
    ran = random.random()
    options.add_argument("--user-agent="+str(ran)+"")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-3d-apis")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    chrome = pyt_Input.get()
    
    s = Service(r''+chrome+'\\chromedriver') 
    driver = webdriver.Chrome(service=s, options=options)

    url = 'https://goskatalog.ru/portal/#/museums'

    driver.get(url)

    elem_spisok = []
    

    perv = time.strftime("%X", time.localtime())
    
    bb=0
    while (bb == 0):

        try:

            chis1 = driver.find_element(By.XPATH,'/html/body/article/section/div/div/div[1]').text

            if chis1 == 'Количество вычисляется...' or '':
                sleep(0.1)
            else:
                driver.find_element(By.XPATH,'/html/body/article/section/div/div/div[1]/div/div/h3/a').click()

                rr=0
                while (rr == 0):
                    try:

                        chis2 = driver.find_element(By.XPATH,'/html/body/article/div/div[2]/div/div[2]').text

                        if chis2 == 'Количество вычисляется...' or '':
                            sleep(0.1)
                        else:
                            kol = driver.find_element(By.XPATH,'/html/body/article/div/div[2]/div/div[2]').text
                            kol = kol.split()
                            kol = int(kol[1])
                            print('Количество найденных музеев',kol)
                            
                            timer = range(kol)
                            for e in tqdm(timer):

                                e = int(timer.index(e))

                                hh = 0
                                while (hh == 0):
                                    try:
                                        chis2 = driver.find_element(By.XPATH,'/html/body/article/div/div[2]/div/div[2]').text
                                        if chis2 == 'Количество вычисляется...' or '':
                                            sleep(0.001)
                                        else:
                                            e = e + 1
                                            el = str(e)
                                            museum_id = driver.find_element(By.XPATH,'/html/body/article/section/div/div/div[1]/div/div/div/div['+el+']/div/div[1]/a').get_attribute('href')
                                            museum_id = ('='.join(museum_id.split('=')[-1:]))
                                            mus_name = driver.find_element(By.XPATH,'/html/body/article/section/div/div/div[1]/div/div/div/div['+el+']/div/div[2]').text
                                            elem = (str(museum_id)+' - '+str(mus_name)+'')
                                            elem_spisok.append(elem)
                                            with open(""+chrome+"\\museums.txt", "w+", encoding="utf-8") as file: file.writelines("%s\n" % line for line in elem_spisok)
                                            hh = 1

                                    except NoSuchElementException:
                                        html = driver.find_element(By.TAG_NAME,'html') 
                                        html.send_keys(Keys.END)
                                        sleep(0.001)
                                        hh = 0
                                    except StaleElementReferenceException:
                                        html = driver.find_element(By.TAG_NAME,'html')
                                        html.send_keys(Keys.END)
                                        sleep(0.001)
                                        hh = 0

                            rr = 1
                    except NoSuchElementException:
                        sleep(0.001)
                        rr = 0
                    except StaleElementReferenceException:
                        sleep(0.001)
                        rr = 0
                bb = 1


        except NoSuchElementException:
            sleep(0.001)
            bb = 0
        except StaleElementReferenceException:
            sleep(0.001)
            bb = 0
    vtoroe = time.strftime("%X", time.localtime())

    format = '%H:%M:%S'

    razn = datetime.strptime(vtoroe, format) - datetime.strptime(perv, format)
    print('Время выполнения - '+str(razn))


def spisok():

    global img
    try:
        img = open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[5]

    except FileNotFoundError:
        open("autofill_scraping.txt", "w+")
        img = ''
    except IndexError:
        img = ''

    options = webdriver.ChromeOptions() 
    options.add_argument('--headless')
    ran = random.random()
    options.add_argument("--user-agent="+str(ran)+"")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-3d-apis")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    chrome = pyt_Input.get()
    zap = zap_Input.get()
    im = im_Input.get()
    muz = muz_Input.get()
    
    s = Service(r''+chrome+'\\chromedriver') 
    driver = webdriver.Chrome(service=s, options=options)

    url = 'https://goskatalog.ru/portal/#/collections?q='+zap+'&museumIds='+muz+'&imageExists='+img+''

    driver.get(url)

    kol = int(zapch_Input.get())

    elem_spisok = []

    perv = time.strftime("%X", time.localtime())
    

    timer = range(kol)
    for e in tqdm(timer):
        e = int(timer.index(e))

        bb = 0
        while (bb == 0):

            try:
                chis2 = driver.find_element(By.XPATH,'/html/body/article/ui-view/div/div[2]/div/div[2]').text

                if chis2 == 'Количество вычисляется...' or '':
                    sleep(0.001)
                else:
                    e = e + 1
                    el = str(e)
                    elem = driver.find_element(By.XPATH,'/html/body/article/ui-view/section/div/div/div[1]/div/div['+el+']/div/div[1]/a').get_attribute('href')
                    elem_spisok.append(elem)
                    with open(""+chrome+"\\list.txt", "w+") as file:
                        file.writelines("%s\n" % line for line in elem_spisok)
                    bb = 1
            except NoSuchElementException:
                html = driver.find_element(By.TAG_NAME,'html') 
                html.send_keys(Keys.END)
                sleep(0.001)
                bb = 0
            except StaleElementReferenceException:
                html = driver.find_element(By.TAG_NAME,'html')
                html.send_keys(Keys.END)
                sleep(0.001)
                bb = 0
    vtoroe = time.strftime("%X", time.localtime())

    format = '%H:%M:%S'

    razn = datetime.strptime(vtoroe, format) - datetime.strptime(perv, format)
    print('Время выполнения - '+str(razn))

def nazhat_sbor():

    chrome = pyt_Input.get()
    kol = int(zapch_Input.get())
    with open(''+chrome+'\\list.txt') as myfile: count = sum(1 for line in myfile)
    if kol <= count:
        pars()
    else:
        mb.showerror("Ошибка", "Количество не совпадает со списком!")

def pars():

    global img
    try:
        img = open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[5]
    except IndexError:
        img = ''

    kol = int(zapch_Input.get())

    chrome = pyt_Input.get()
    zap = zap_Input.get()
    im = im_Input.get()

    global options

    options = webdriver.ChromeOptions() 
    options.add_argument('--headless')
    ran = random.random()
    options.add_argument("--user-agent="+str(ran)+"")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--disable-3d-apis")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    s = Service(r''+chrome+'\\chromedriver') 
    driver = webdriver.Chrome(service=s, options=options)

    url = 'https://goskatalog.ru/'
    driver.get(url)

    ID_spisok = [] # id
    author_spisok = [] #автор
    nazvanie_spisok = [] #название
    opisanie_spisok = [] #описание
    data_spisok = [] #дата создания 
    material_spisok = [] #материал 
    razmer_spisok = [] #размер 
    mesto_spisok = [] #место создания 
    gde_spisok = [] #место хранения 
    ssilka_spisok = [] #ссылка на объект 

    ssilka_img_spisok = [] #ссылка на изображение

    kp_spisok = []
    
    perv = time.strftime("%X", time.localtime())

    with open(""+chrome+"\\list.txt", "r", encoding="utf-8") as f:
        timer = [line.strip() for line in f if line.strip()]
    del timer[int(kol):]

    for i in tqdm(timer):

        i = int(timer.index(i))
        ur =open(""+chrome+"\\list.txt", "r", encoding="utf-8").read().split('\n')[i]
        driver.get(ur)

        aa = 0
        while (aa==0):

            ff = 0
            while (ff==0):

                try:
                    if driver.find_element(By.XPATH, '/html/body/article/ui-view/div/div[1]/section/div/h4').text != '':
                        driver.refresh()
                        ff = 1
                    else:
                        break

                except NoSuchElementException:
                    ff=1
                except StaleElementReferenceException:
                    ff=0

            try:

                nazvanie = driver.find_element(By.XPATH,'/html/body/article/ui-view/div/div[2]/section/div[1]/div/div/div[1]').text

                if nazvanie == '':
                    sleep(0.0001)
                else:

                    ID_number = ('='.join(ur.split('=')[-1:]))
                    ID_spisok.append(ID_number)

                    nazvanie = driver.find_element(By.XPATH,'/html/body/article/ui-view/div/div[2]').text

                    massiv =  nazvanie.split("\n")

                    author = massiv[0]
                    if author == '': author = '—'
                    author_spisok.append(author)

                    nazvanie = massiv[1]
                    if nazvanie == '': author = '—'
                    nazvanie_spisok.append(nazvanie)

                    opisanie = massiv[-1]
                    if opisanie == '': author = '—'
                    opisanie_spisok.append(opisanie)

                    data = massiv[4]
                    if data == '': author = '—'
                    data_spisok.append(data)

                    material = massiv[6]
                    if material == '': author = '—'
                    material = material.translate(str.maketrans({',': ' |'}))
                    material_spisok.append(material)

                    razmer = massiv[8]
                    if razmer == '': author = '—'
                    razmer_spisok.append(razmer)

                    kp = massiv[14]
                    if kp == '': author = '—'
                    kp_spisok.append(kp)

                    mesto = massiv[10]
                    if mesto == '': author = '—'
                    mesto_spisok.append(mesto)

                    gde = massiv[22]
                    if gde == '': author = '—'
                    gde_spisok.append(gde)

                    ssilka = ur
                    ssilka_spisok.append(ssilka)

                    try:
                        ssilka_img = driver.find_element(By.XPATH,'/html/body/article/ui-view/div/div[1]/div[1]/table/tbody/tr/td[1]/img').get_attribute('src')
                        ssilka_img = ('?'.join(ssilka_img.split('?')[:-1]))
                        ssilka_img_spisok.append(ssilka_img)
                    except:
                        ssilka_img = 'нет фото'
                        ssilka_img_spisok.append(ssilka_img)

                    aa = 1
                    
            except NoSuchElementException:
                sleep(0.001)
                aa=0
            except StaleElementReferenceException:
                sleep(0.001)
                aa=0

        data = dict(ID = ID_spisok, Автор=author_spisok,Название=nazvanie_spisok,Описание = opisanie_spisok, Период_создания=data_spisok,Технологии=material_spisok,Размер=razmer_spisok, Место_создания=mesto_spisok,Местонахождение=gde_spisok, Ссылка=ssilka_spisok, Ссылка_на_фото=ssilka_img_spisok, Номер_по_КП=kp_spisok)
        df = pd.DataFrame(data)
        df.to_csv(r''+chrome+'\\'+im+'.csv', encoding="utf-8", index=False)
                

    vtoroe = time.strftime("%X", time.localtime())

    format = '%H:%M:%S'

    razn = datetime.strptime(vtoroe, format) - datetime.strptime(perv, format)
    print('Время выполнения - '+str(razn))
    mb.showinfo("Уведомление", "Данные успешно собраны!")

def sbor_api():


    try:

        try:
            typology_name =open(r"typology.txt", "r", encoding="utf-8").read().split('\n')[0]
            if typology_name == '':
                typology_name == ''
        except:
            typology_name = ''

        if var.get() == 1: how_req = 'search'
        elif var.get() == 2: how_req = 'contain'

        chrome = pyt_Input3.get()
        req = zap_Input3.get()
        im = im_Input3.get()
        api = api_Input3.get()
        mus = muz_Input3.get()
        #mus = re.sub('"', '%5C%22', mus)


        if req=='':
            reque = 'https://opendata.mkrf.ru/v2/museum-exhibits/$?f={"data.museum.code":{"$'+how_req+'":"'+mus+'"},"data.typology.name":{"$eq":"'+typology_name+'"}'
            reque = re.sub(' ', '%20', reque)
            reque = re.sub('"', '%22', reque)
            reque = re.sub('{', '%7B', reque) 
            reque = re.sub('}', '%7D', reque)
        else:
            reque = 'https://opendata.mkrf.ru/v2/museum-exhibits/$?f={"data.name":{"$'+how_req+'":"'+req+'"},"data.museum.code":{"$eq":"'+mus+'"},"data.typology.name":{"$eq":"'+typology_name+'"}'
            reque = re.sub(' ', '%20', reque)
            reque = re.sub('"', '%22', reque)
            reque = re.sub('{', '%7B', reque) 
            reque = re.sub('}', '%7D', reque)



        response = requests.get(''+reque+'%7D&l=10'+'', headers={'X-API-KEY': ''+api+''})
        reque = reque.rstrip('&l=10')
        reque = (reque+'%7D')
        data = json.loads(response.text)
        kolkol = int(data['total'])
        print('Найдено результатов:',kolkol)


        id_massiv = []
        authors_massiv = []
        name_massiv = []
        description_massiv = []
        periodStr_massiv = []

        productionPlace_massiv = []
        museum_massiv = []
        museum_code_massiv = []
        museum_id_massiv = []

        typology_massiv = []
        technologies_massiv = []
        dimStr_massiv = []
        images_massiv = []

        kolkol1 = int(kolkol%1000)
        kolkol2 = int(round((kolkol-kolkol1)/1000))

        perv = time.strftime("%X", time.localtime())

        for i in range(kolkol2):
            response = requests.get(''+reque+'&s='+str(i*1000)+'&l=1000',headers={'X-API-KEY': ''+api+''})
            data = json.loads(response.text)
            data_1 =(data['data'])
            kol=1000
            timer = range(kol)
            for i in tqdm(timer):
                i = int(timer.index(i))
                data_2 = (data_1[i]['data'])

                # ID
                try:
                    id_m = (data_2['id'])
                    id_massiv.append(id_m)
                except KeyError:
                    id_m = '—'
                    id_massiv.append(id_m)

                # AUTHORS
                try:
                    authors_m = data_2['authors']
                    authors_m = " ".join(authors_m)
                    if authors_m == '':
                        authors_m = '—'
                    authors_massiv.append(str(authors_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''}))))
                except KeyError:
                    authors_m = '—'
                    authors_massiv.append(authors_m)

                # NAME    
                try:
                    name_m = data_2['name']
                    if name_m == '':
                        name_m = '—'
                    name_massiv.append(name_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    name_m = '—'
                    name_massiv.append(name_m)

                # DESCRIPTION 
                try:
                    description_m = data_2['description']
                    if description_m == '':
                        description_m = '—'
                    description_massiv.append(description_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    description_m = '—'
                    description_massiv.append(description_m)

                # periodStr_massiv
                try:
                    periodStr_m = data_2['periodStr']
                    if periodStr_m == '':
                        periodStr_m = '—'
                    periodStr_massiv.append(periodStr_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    periodStr_m = '—'
                    periodStr_massiv.append(periodStr_m)

                # productionPlace
                try:
                    productionPlace_m = data_2['productionPlace']
                    if productionPlace_m == '':
                        productionPlace_m = '—'
                    productionPlace_massiv.append(productionPlace_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    productionPlace_m = '—'
                    productionPlace_massiv.append(productionPlace_m)

                # museum_massiv
                try:
                    data_3 = data_2['museum']
                    museum_m = data_3['name']
                    if museum_m == '':
                        museum_m = '—'
                    museum_massiv.append(museum_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    museum_m = '—'
                    museum_massiv.append(museum_m)

                # museum_id_massiv
                try:
                    data_3 = data_2['museum']
                    museum_id_m = data_3['id']
                    if museum_id_m == '':
                        museum_id_m = '—'
                    museum_id_massiv.append(museum_id_m)
                except KeyError:
                    museum_id_m = '—'
                    museum_id_massiv.append(museum_id_m)

                # museum_code_massiv
                try:
                    data_3 = data_2['museum']
                    museum_code_m = data_3['code']
                    if museum_code_m == '':
                        museum_code_m = '—'
                    museum_code_massiv.append(museum_code_m)
                except KeyError:
                    museum_code_m = '—'
                    museum_code_massiv.append(museum_code_m)

                # typology_massiv
                try:
                    data_3 = data_2['typology']
                    typology_m = data_3['name']
                    if typology_m == '':
                        typology_m = '—'
                    typology_massiv.append(typology_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    typology_m = '—'
                    typology_massiv.append(typology_m)

                # technologies_massiv
                try:
                    technologies_m = data_2['technologies']
                    technologies_m = re.sub("'", '', str(technologies_m))
                    technologies_m = technologies_m[1:]
                    technologies_m = technologies_m[:-1]
                    if technologies_m == '':
                        technologies_m = '—'
                    technologies_massiv.append(technologies_m)
                except KeyError:
                    technologies_m = '—'
                    technologies_massiv.append(technologies_m)

                # dimStr_massiv
                try:
                    dimStr_m = data_2['dimStr']
                    if dimStr_m == '':
                        dimStr_m = '—'
                    dimStr_massiv.append(dimStr_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    dimStr_m = '—'
                    dimStr_massiv.append(dimStr_m)

                # images_massiv
                try:
                    images_m = data_2['images']
                    images_m = re.sub("{'", '', str(images_m))
                    images_m = re.sub("'}", '', str(images_m))
                    images_m = images_m[1:]
                    images_m = images_m[:-1]
                    images_m = images_m.translate(str.maketrans({"'": ''}))
                    images_m = re.sub('url: ', '', images_m)
                    if images_m == '':
                        images_m = '—'
                    images_massiv.append(images_m)
                except KeyError:
                    images_m = '—'
                    images_massiv.append(images_m)

                i += 1

        for i in range(1):
            response = requests.get(''+reque+'&s='+str(kolkol2*1000)+'&l='+str(kolkol1)+'',headers={'X-API-KEY': ''+api+''})
            data = json.loads(response.text)
            data_1 =(data['data'])


            timer = range(kolkol1)
            for i in tqdm(timer):
                i = int(timer.index(i))
                data_2 = (data_1[i]['data'])


                # ID
                try:
                    id_m = (data_2['id'])
                    id_massiv.append(id_m)
                except KeyError:
                    id_m = '—'
                    id_massiv.append(id_m)

                # AUTHORS
                try:
                    authors_m = data_2['authors']
                    authors_m = " ".join(authors_m)
                    if authors_m == '':
                        authors_m = '—'
                    authors_massiv.append(authors_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    authors_m = '—'
                    authors_massiv.append(authors_m)

                # NAME    
                try:
                    name_m = data_2['name']
                    if name_m == '':
                        name_m = '—'
                    name_massiv.append(name_m.replace("\n", " "))
                except KeyError:
                    name_m = '—'
                    name_massiv.append(name_m)

                # DESCRIPTION 
                try:
                    description_m = data_2['description']
                    if description_m == '':
                        description_m = '—'
                    description_massiv.append(description_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    description_m = '—'
                    description_massiv.append(description_m)

                # periodStr_massiv
                try:
                    periodStr_m = data_2['periodStr']
                    if periodStr_m == '':
                        periodStr_m = '—'
                    periodStr_massiv.append(periodStr_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    periodStr_m = '—'
                    periodStr_massiv.append(periodStr_m)

                # productionPlace
                try:
                    productionPlace_m = data_2['productionPlace']
                    if productionPlace_m == '':
                        productionPlace_m = '—'
                    productionPlace_massiv.append(productionPlace_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    productionPlace_m = '—'
                    productionPlace_massiv.append(productionPlace_m)

                # museum_massiv
                try:
                    data_3 = data_2['museum']
                    museum_m = data_3['name']
                    if museum_m == '':
                        museum_m = '—'
                    museum_massiv.append(museum_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    museum_m = '—'
                    museum_massiv.append(museum_m)

                # museum_code_massiv
                try:
                    data_3 = data_2['museum']
                    museum_code_m = data_3['code']
                    if museum_code_m == '':
                        museum_code_m = '—'
                    museum_code_massiv.append(museum_code_m)
                except KeyError:
                    museum_code_m = '—'
                    museum_code_massiv.append(museum_code_m)

                # museum_id_massiv
                try:
                    data_3 = data_2['museum']
                    museum_id_m = data_3['id']
                    if museum_id_m == '':
                        museum_id_m = '—'
                    museum_id_massiv.append(museum_id_m)
                except KeyError:
                    museum_id_m = '—'
                    museum_id_massiv.append(museum_id_m)

                # typology_massiv
                try:
                    data_3 = data_2['typology']
                    typology_m = data_3['name']
                    if typology_m == '':
                        typology_m = '—'
                    typology_massiv.append(typology_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    typology_m = '—'
                    typology_massiv.append(typology_m)

                # technologies_massiv
                try:
                    technologies_m = data_2['technologies']
                    technologies_m = re.sub("'", '', str(technologies_m))
                    technologies_m = technologies_m[1:]
                    technologies_m = technologies_m[:-1]
                    if technologies_m == '':
                        technologies_m = '—'
                    technologies_massiv.append(technologies_m)
                except KeyError:
                    technologies_m = '—'
                    technologies_massiv.append(technologies_m)

                # dimStr_massiv
                try:
                    dimStr_m = data_2['dimStr']
                    if dimStr_m == '':
                        dimStr_m = '—'
                    dimStr_massiv.append(dimStr_m.translate(str.maketrans({'\n': '', '\r': '', '\t': ''})))
                except KeyError:
                    dimStr_m = '—'
                    dimStr_massiv.append(dimStr_m)
                    
                # images_massiv
                try:
                    images_m = data_2['images']
                    images_m = re.sub("{'", '', str(images_m))
                    images_m = re.sub("'}", '', str(images_m))
                    images_m = images_m[1:]
                    images_m = images_m[:-1]
                    images_m = images_m.translate(str.maketrans({"'": ''}))
                    images_m = re.sub('url: ', '', images_m)
                    if images_m == '':
                        images_m = '—'
                    images_massiv.append(images_m)
                except KeyError:
                    images_m = '—'
                    images_massiv.append(images_m)

                i += 1

        data = dict(ID = id_massiv, Автор=authors_massiv,Название=name_massiv, Описание=description_massiv, Период_создания=periodStr_massiv, Место_создания=productionPlace_massiv, Музей=museum_massiv, КОПУК_Музея=museum_code_massiv, ID_Музея=museum_id_massiv, Типология=typology_massiv, Технологии=technologies_massiv, Размер=dimStr_massiv, Изображения=images_massiv)
        df = pd.DataFrame(data)
        df.to_csv(r''+chrome+'\\'+im+'.csv', encoding="utf-8", index=False)


        vtoroe = time.strftime("%X", time.localtime())
        format = '%H:%M:%S'
        razn = datetime.strptime(vtoroe, format) - datetime.strptime(perv, format)
        print('Время выполнения - '+str(razn))

    except:

        data = dict(ID = id_massiv, Автор=authors_massiv,Название=name_massiv, Описание=description_massiv, Период_создания=periodStr_massiv, Место_создания=productionPlace_massiv, Музей=museum_massiv, КОПУК_Музея=museum_code_massiv, ID_Музея=museum_id_massiv, Типология=typology_massiv, Технологии=technologies_massiv, Размер=dimStr_massiv, Изображения=images_massiv)
        df = pd.DataFrame(data)
        df.to_csv(r''+chrome+'\\'+im+'.csv', encoding="utf-8", index=False)

        vtoroe = time.strftime("%X", time.localtime())
        format = '%H:%M:%S'
        razn = datetime.strptime(vtoroe, format) - datetime.strptime(perv, format)
        print('Время выполнения - '+str(razn))

def proc_data_choice():

    if var4f.get() == 1: proc_data_1()
    elif var4f.get() == 2: proc_data_2()
    elif var4f.get() == 3: proc_data_5()
    elif var4f.get() == 4: proc_data_3()
    elif var4f.get() == 5: proc_data_4()

def proc_data_1():

    im = csv_ob3.get()
    pyt = pyt_ob3.get()


    try:

        ### Проверка ###
        df = pd.read_csv(""+pyt+"\\"+im+".csv", encoding="utf-8")
        df["Место_создания(обр.)"].tolist()

        mb.showwarning("Внимание!", "Обработка уже выполнена")
        ### Проверка ###

    except:
        segmenter = Segmenter()
        morph_vocab = MorphVocab()
        addr_extractor = AddrExtractor(morph_vocab)

        vv = []

        df = pd.read_csv(""+pyt+"\\"+im+".csv", encoding="utf-8")
        text = df['Место_создания'].tolist()

        kol = len(text)
        timer = range(kol)

        for i in tqdm(timer):
          text_el = text[i]
          if text_el == '':
            text_el = '—'
          matches = addr_extractor(text_el)
          facts = [i.fact.as_json for i in matches]

          if facts != []:
            tmp = list(facts[0].values())
            vv.append(tmp[0])
          else:
            vv.append('—')
            i += 1


        df.insert(6, "Место_создания(обр.)", vv)

        df.to_csv(""+pyt+"\\"+im+".csv", encoding="utf-8", index=False)

def proc_data_2():
    
    im = csv_ob3.get()
    pyt = pyt_ob3.get()

    try:

        ### Проверка ###
        df = pd.read_csv(""+pyt+"\\"+im+".csv", encoding="utf-8")
        df["Период_создания(обр.)"].tolist()
        ### Проверка ###

    except:

        segmenter = Segmenter()
        morph_vocab = MorphVocab()
        addr_extractor = DatesExtractor(morph_vocab)

        vv = []

        df = pd.read_csv(""+pyt+"\\"+im+".csv", encoding="utf-8")
        text = df['Период_создания'].tolist()

        kol = len(text)
        timer = range(kol)

        for i in tqdm(timer):
          text_el = text[i]
          if text_el == '':
            text_el = '—'
          matches = addr_extractor(text_el)
          facts = [i.fact.as_json for i in matches]

          if facts != []:
            tmp = list(facts[0].values())
            vv.append(tmp[0])
          else:
            vv.append(text_el)
            i += 1


        df.insert(5, "Период_создания(обр.)", vv)

        df.to_csv(""+pyt+"\\"+im+".csv", encoding="utf-8", index=False)

        stolb = []
        try:
          with open("dict_date.txt", encoding="utf-8") as file: stolb = [row.strip() for row in file]
        except FileNotFoundError:
          stolb = []



        df = pd.read_csv(""+pyt+"\\"+im+".csv", encoding="utf-8")

        new_ = []

        for i in range(len(df)):
          bb = df["Период_создания(обр.)"][i]
          bb = re.sub('"', '', str(bb))
          bb = bb.lstrip()
          #print(bb)
          for ii in range(len(stolb)):
            p = stolb[ii].split(',')
            if bb in p:
              new_.append(p[0])

        dt = new_
        new_c = []


        nw = []

        for i in range(len(dt)):
          bb = dt[i]
          bb = bb.split('-')
          if len(bb) == 2:
            v = []
            for n in range(int(bb[0]),int(bb[1])+1): 
              v.append(n)
            new_c.append(v)
          else:
            new_c.append(bb)

        year_1801 = 0
        year_1802 = 0
        year_1803 = 0
        year_1804 = 0
        year_1805 = 0
        year_1806 = 0
        year_1807 = 0
        year_1808 = 0
        year_1809 = 0
        year_1810 = 0
        year_1811 = 0
        year_1812 = 0
        year_1813 = 0
        year_1814 = 0
        year_1815 = 0
        year_1816 = 0
        year_1817 = 0
        year_1818 = 0
        year_1819 = 0
        year_1820 = 0
        year_1821 = 0
        year_1822 = 0
        year_1823 = 0
        year_1824 = 0
        year_1825 = 0
        year_1826 = 0
        year_1827 = 0
        year_1828 = 0
        year_1829 = 0
        year_1830 = 0
        year_1831 = 0
        year_1832 = 0
        year_1833 = 0
        year_1834 = 0
        year_1835 = 0
        year_1836 = 0
        year_1837 = 0
        year_1838 = 0
        year_1839 = 0
        year_1840 = 0
        year_1841 = 0
        year_1842 = 0
        year_1843 = 0
        year_1844 = 0
        year_1845 = 0
        year_1846 = 0
        year_1847 = 0
        year_1848 = 0
        year_1849 = 0
        year_1850 = 0
        year_1851 = 0
        year_1852 = 0
        year_1853 = 0
        year_1854 = 0
        year_1855 = 0
        year_1856 = 0
        year_1857 = 0
        year_1858 = 0
        year_1859 = 0
        year_1860 = 0
        year_1861 = 0
        year_1862 = 0
        year_1863 = 0
        year_1864 = 0
        year_1865 = 0
        year_1866 = 0
        year_1867 = 0
        year_1868 = 0
        year_1869 = 0
        year_1870 = 0
        year_1871 = 0
        year_1872 = 0
        year_1873 = 0
        year_1874 = 0
        year_1875 = 0
        year_1876 = 0
        year_1877 = 0
        year_1878 = 0
        year_1879 = 0
        year_1880 = 0
        year_1881 = 0
        year_1882 = 0
        year_1883 = 0
        year_1884 = 0
        year_1885 = 0
        year_1886 = 0
        year_1887 = 0
        year_1888 = 0
        year_1889 = 0
        year_1890 = 0
        year_1891 = 0
        year_1892 = 0
        year_1893 = 0
        year_1894 = 0
        year_1895 = 0
        year_1896 = 0
        year_1897 = 0
        year_1898 = 0
        year_1899 = 0
        year_1900 = 0
        year_1901 = 0
        year_1902 = 0
        year_1903 = 0
        year_1904 = 0
        year_1905 = 0
        year_1906 = 0
        year_1907 = 0
        year_1908 = 0
        year_1909 = 0
        year_1910 = 0
        year_1911 = 0
        year_1912 = 0
        year_1913 = 0
        year_1914 = 0
        year_1915 = 0
        year_1916 = 0
        year_1917 = 0
        year_1918 = 0
        year_1919 = 0
        year_1920 = 0
        year_1921 = 0
        year_1922 = 0
        year_1923 = 0
        year_1924 = 0
        year_1925 = 0
        year_1926 = 0
        year_1927 = 0
        year_1928 = 0
        year_1929 = 0
        year_1930 = 0
        year_1931 = 0
        year_1932 = 0
        year_1933 = 0
        year_1934 = 0
        year_1935 = 0
        year_1936 = 0
        year_1937 = 0
        year_1938 = 0
        year_1939 = 0
        year_1940 = 0
        year_1941 = 0
        year_1942 = 0
        year_1943 = 0
        year_1944 = 0
        year_1945 = 0
        year_1946 = 0
        year_1947 = 0
        year_1948 = 0
        year_1949 = 0
        year_1950 = 0
        year_1951 = 0
        year_1952 = 0
        year_1953 = 0
        year_1954 = 0
        year_1955 = 0
        year_1956 = 0
        year_1957 = 0
        year_1958 = 0
        year_1959 = 0
        year_1960 = 0
        year_1961 = 0
        year_1962 = 0
        year_1963 = 0
        year_1964 = 0
        year_1965 = 0
        year_1966 = 0
        year_1967 = 0
        year_1968 = 0
        year_1969 = 0
        year_1970 = 0
        year_1971 = 0
        year_1972 = 0
        year_1973 = 0
        year_1974 = 0
        year_1975 = 0
        year_1976 = 0
        year_1977 = 0
        year_1978 = 0
        year_1979 = 0
        year_1980 = 0
        year_1981 = 0
        year_1982 = 0
        year_1983 = 0
        year_1984 = 0
        year_1985 = 0
        year_1986 = 0
        year_1987 = 0
        year_1988 = 0
        year_1989 = 0
        year_1990 = 0
        year_1991 = 0
        year_1992 = 0
        year_1993 = 0
        year_1994 = 0
        year_1995 = 0
        year_1996 = 0
        year_1997 = 0
        year_1998 = 0
        year_1999 = 0
        year_2000 = 0
        year_2001 = 0
        year_2002 = 0
        year_2003 = 0
        year_2004 = 0
        year_2005 = 0
        year_2006 = 0
        year_2007 = 0
        year_2008 = 0
        year_2009 = 0
        year_2010 = 0
        year_2011 = 0
        year_2012 = 0
        year_2013 = 0
        year_2014 = 0
        year_2015 = 0
        year_2016 = 0
        year_2017 = 0
        year_2018 = 0
        year_2019 = 0
        year_2020 = 0
        year_2021 = 0
        year_2022 = 0


        bbbb = new_c

        for iii in range(len(bbbb)):
          bbb = bbbb[iii]
          for ii in range(len(bbb)):
            v = int(bbb[ii])
            if v == 1801: year_1801+= round((1/(len(bbb))),2)
            elif v == 1802: year_1802+= round((1/(len(bbb))),2)
            elif v == 1803: year_1803+= round((1/(len(bbb))),2)
            elif v == 1804: year_1804+= round((1/(len(bbb))),2)
            elif v == 1805: year_1805+= round((1/(len(bbb))),2)
            elif v == 1806: year_1806+= round((1/(len(bbb))),2)
            elif v == 1807: year_1807+= round((1/(len(bbb))),2)
            elif v == 1808: year_1808+= round((1/(len(bbb))),2)
            elif v == 1809: year_1809+= round((1/(len(bbb))),2)
            elif v == 1810: year_1810+= round((1/(len(bbb))),2)
            elif v == 1811: year_1811+= round((1/(len(bbb))),2)
            elif v == 1812: year_1812+= round((1/(len(bbb))),2)
            elif v == 1813: year_1813+= round((1/(len(bbb))),2)
            elif v == 1814: year_1814+= round((1/(len(bbb))),2)
            elif v == 1815: year_1815+= round((1/(len(bbb))),2)
            elif v == 1816: year_1816+= round((1/(len(bbb))),2)
            elif v == 1817: year_1817+= round((1/(len(bbb))),2)
            elif v == 1818: year_1818+= round((1/(len(bbb))),2)
            elif v == 1819: year_1819+= round((1/(len(bbb))),2)
            elif v == 1820: year_1820+= round((1/(len(bbb))),2)
            elif v == 1821: year_1821+= round((1/(len(bbb))),2)
            elif v == 1822: year_1822+= round((1/(len(bbb))),2)
            elif v == 1823: year_1823+= round((1/(len(bbb))),2)
            elif v == 1824: year_1824+= round((1/(len(bbb))),2)
            elif v == 1825: year_1825+= round((1/(len(bbb))),2)
            elif v == 1826: year_1826+= round((1/(len(bbb))),2)
            elif v == 1827: year_1827+= round((1/(len(bbb))),2)
            elif v == 1828: year_1828+= round((1/(len(bbb))),2)
            elif v == 1829: year_1829+= round((1/(len(bbb))),2)
            elif v == 1830: year_1830+= round((1/(len(bbb))),2)
            elif v == 1831: year_1831+= round((1/(len(bbb))),2)
            elif v == 1832: year_1832+= round((1/(len(bbb))),2)
            elif v == 1833: year_1833+= round((1/(len(bbb))),2)
            elif v == 1834: year_1834+= round((1/(len(bbb))),2)
            elif v == 1835: year_1835+= round((1/(len(bbb))),2)
            elif v == 1836: year_1836+= round((1/(len(bbb))),2)
            elif v == 1837: year_1837+= round((1/(len(bbb))),2)
            elif v == 1838: year_1838+= round((1/(len(bbb))),2)
            elif v == 1839: year_1839+= round((1/(len(bbb))),2)
            elif v == 1840: year_1840+= round((1/(len(bbb))),2)
            elif v == 1841: year_1841+= round((1/(len(bbb))),2)
            elif v == 1842: year_1842+= round((1/(len(bbb))),2)
            elif v == 1843: year_1843+= round((1/(len(bbb))),2)
            elif v == 1844: year_1844+= round((1/(len(bbb))),2)
            elif v == 1845: year_1845+= round((1/(len(bbb))),2)
            elif v == 1846: year_1846+= round((1/(len(bbb))),2)
            elif v == 1847: year_1847+= round((1/(len(bbb))),2)
            elif v == 1848: year_1848+= round((1/(len(bbb))),2)
            elif v == 1849: year_1849+= round((1/(len(bbb))),2)
            elif v == 1850: year_1850+= round((1/(len(bbb))),2)
            elif v == 1851: year_1851+= round((1/(len(bbb))),2)
            elif v == 1852: year_1852+= round((1/(len(bbb))),2)
            elif v == 1853: year_1853+= round((1/(len(bbb))),2)
            elif v == 1854: year_1854+= round((1/(len(bbb))),2)
            elif v == 1855: year_1855+= round((1/(len(bbb))),2)
            elif v == 1856: year_1856+= round((1/(len(bbb))),2)
            elif v == 1857: year_1857+= round((1/(len(bbb))),2)
            elif v == 1858: year_1858+= round((1/(len(bbb))),2)
            elif v == 1859: year_1859+= round((1/(len(bbb))),2)
            elif v == 1860: year_1860+= round((1/(len(bbb))),2)
            elif v == 1861: year_1861+= round((1/(len(bbb))),2)
            elif v == 1862: year_1862+= round((1/(len(bbb))),2)
            elif v == 1863: year_1863+= round((1/(len(bbb))),2)
            elif v == 1864: year_1864+= round((1/(len(bbb))),2)
            elif v == 1865: year_1865+= round((1/(len(bbb))),2)
            elif v == 1866: year_1866+= round((1/(len(bbb))),2)
            elif v == 1867: year_1867+= round((1/(len(bbb))),2)
            elif v == 1868: year_1868+= round((1/(len(bbb))),2)
            elif v == 1869: year_1869+= round((1/(len(bbb))),2)
            elif v == 1870: year_1870+= round((1/(len(bbb))),2)
            elif v == 1871: year_1871+= round((1/(len(bbb))),2)
            elif v == 1872: year_1872+= round((1/(len(bbb))),2)
            elif v == 1873: year_1873+= round((1/(len(bbb))),2)
            elif v == 1874: year_1874+= round((1/(len(bbb))),2)
            elif v == 1875: year_1875+= round((1/(len(bbb))),2)
            elif v == 1876: year_1876+= round((1/(len(bbb))),2)
            elif v == 1877: year_1877+= round((1/(len(bbb))),2)
            elif v == 1878: year_1878+= round((1/(len(bbb))),2)
            elif v == 1879: year_1879+= round((1/(len(bbb))),2)
            elif v == 1880: year_1880+= round((1/(len(bbb))),2)
            elif v == 1881: year_1881+= round((1/(len(bbb))),2)
            elif v == 1882: year_1882+= round((1/(len(bbb))),2)
            elif v == 1883: year_1883+= round((1/(len(bbb))),2)
            elif v == 1884: year_1884+= round((1/(len(bbb))),2)
            elif v == 1885: year_1885+= round((1/(len(bbb))),2)
            elif v == 1886: year_1886+= round((1/(len(bbb))),2)
            elif v == 1887: year_1887+= round((1/(len(bbb))),2)
            elif v == 1888: year_1888+= round((1/(len(bbb))),2)
            elif v == 1889: year_1889+= round((1/(len(bbb))),2)
            elif v == 1890: year_1890+= round((1/(len(bbb))),2)
            elif v == 1891: year_1891+= round((1/(len(bbb))),2)
            elif v == 1892: year_1892+= round((1/(len(bbb))),2)
            elif v == 1893: year_1893+= round((1/(len(bbb))),2)
            elif v == 1894: year_1894+= round((1/(len(bbb))),2)
            elif v == 1895: year_1895+= round((1/(len(bbb))),2)
            elif v == 1896: year_1896+= round((1/(len(bbb))),2)
            elif v == 1897: year_1897+= round((1/(len(bbb))),2)
            elif v == 1898: year_1898+= round((1/(len(bbb))),2)
            elif v == 1899: year_1899+= round((1/(len(bbb))),2)
            elif v == 1900: year_1900+= round((1/(len(bbb))),2)
            elif v == 1901: year_1901+= round((1/(len(bbb))),2)
            elif v == 1902: year_1902+= round((1/(len(bbb))),2)
            elif v == 1903: year_1903+= round((1/(len(bbb))),2)
            elif v == 1904: year_1904+= round((1/(len(bbb))),2)
            elif v == 1905: year_1905+= round((1/(len(bbb))),2)
            elif v == 1906: year_1906+= round((1/(len(bbb))),2)
            elif v == 1907: year_1907+= round((1/(len(bbb))),2)
            elif v == 1908: year_1908+= round((1/(len(bbb))),2)
            elif v == 1909: year_1909+= round((1/(len(bbb))),2)
            elif v == 1910: year_1910+= round((1/(len(bbb))),2)
            elif v == 1911: year_1911+= round((1/(len(bbb))),2)
            elif v == 1912: year_1912+= round((1/(len(bbb))),2)
            elif v == 1913: year_1913+= round((1/(len(bbb))),2)
            elif v == 1914: year_1914+= round((1/(len(bbb))),2)
            elif v == 1915: year_1915+= round((1/(len(bbb))),2)
            elif v == 1916: year_1916+= round((1/(len(bbb))),2)
            elif v == 1917: year_1917+= round((1/(len(bbb))),2)
            elif v == 1918: year_1918+= round((1/(len(bbb))),2)
            elif v == 1919: year_1919+= round((1/(len(bbb))),2)
            elif v == 1920: year_1920+= round((1/(len(bbb))),2)
            elif v == 1921: year_1921+= round((1/(len(bbb))),2)
            elif v == 1922: year_1922+= round((1/(len(bbb))),2)
            elif v == 1923: year_1923+= round((1/(len(bbb))),2)
            elif v == 1924: year_1924+= round((1/(len(bbb))),2)
            elif v == 1925: year_1925+= round((1/(len(bbb))),2)
            elif v == 1926: year_1926+= round((1/(len(bbb))),2)
            elif v == 1927: year_1927+= round((1/(len(bbb))),2)
            elif v == 1928: year_1928+= round((1/(len(bbb))),2)
            elif v == 1929: year_1929+= round((1/(len(bbb))),2)
            elif v == 1930: year_1930+= round((1/(len(bbb))),2)
            elif v == 1931: year_1931+= round((1/(len(bbb))),2)
            elif v == 1932: year_1932+= round((1/(len(bbb))),2)
            elif v == 1933: year_1933+= round((1/(len(bbb))),2)
            elif v == 1934: year_1934+= round((1/(len(bbb))),2)
            elif v == 1935: year_1935+= round((1/(len(bbb))),2)
            elif v == 1936: year_1936+= round((1/(len(bbb))),2)
            elif v == 1937: year_1937+= round((1/(len(bbb))),2)
            elif v == 1938: year_1938+= round((1/(len(bbb))),2)
            elif v == 1939: year_1939+= round((1/(len(bbb))),2)
            elif v == 1940: year_1940+= round((1/(len(bbb))),2)
            elif v == 1941: year_1941+= round((1/(len(bbb))),2)
            elif v == 1942: year_1942+= round((1/(len(bbb))),2)
            elif v == 1943: year_1943+= round((1/(len(bbb))),2)
            elif v == 1944: year_1944+= round((1/(len(bbb))),2)
            elif v == 1945: year_1945+= round((1/(len(bbb))),2)
            elif v == 1946: year_1946+= round((1/(len(bbb))),2)
            elif v == 1947: year_1947+= round((1/(len(bbb))),2)
            elif v == 1948: year_1948+= round((1/(len(bbb))),2)
            elif v == 1949: year_1949+= round((1/(len(bbb))),2)
            elif v == 1950: year_1950+= round((1/(len(bbb))),2)
            elif v == 1951: year_1951+= round((1/(len(bbb))),2)
            elif v == 1952: year_1952+= round((1/(len(bbb))),2)
            elif v == 1953: year_1953+= round((1/(len(bbb))),2)
            elif v == 1954: year_1954+= round((1/(len(bbb))),2)
            elif v == 1955: year_1955+= round((1/(len(bbb))),2)
            elif v == 1956: year_1956+= round((1/(len(bbb))),2)
            elif v == 1957: year_1957+= round((1/(len(bbb))),2)
            elif v == 1958: year_1958+= round((1/(len(bbb))),2)
            elif v == 1959: year_1959+= round((1/(len(bbb))),2)
            elif v == 1960: year_1960+= round((1/(len(bbb))),2)
            elif v == 1961: year_1961+= round((1/(len(bbb))),2)
            elif v == 1962: year_1962+= round((1/(len(bbb))),2)
            elif v == 1963: year_1963+= round((1/(len(bbb))),2)
            elif v == 1964: year_1964+= round((1/(len(bbb))),2)
            elif v == 1965: year_1965+= round((1/(len(bbb))),2)
            elif v == 1966: year_1966+= round((1/(len(bbb))),2)
            elif v == 1967: year_1967+= round((1/(len(bbb))),2)
            elif v == 1968: year_1968+= round((1/(len(bbb))),2)
            elif v == 1969: year_1969+= round((1/(len(bbb))),2)
            elif v == 1970: year_1970+= round((1/(len(bbb))),2)
            elif v == 1971: year_1971+= round((1/(len(bbb))),2)
            elif v == 1972: year_1972+= round((1/(len(bbb))),2)
            elif v == 1973: year_1973+= round((1/(len(bbb))),2)
            elif v == 1974: year_1974+= round((1/(len(bbb))),2)
            elif v == 1975: year_1975+= round((1/(len(bbb))),2)
            elif v == 1976: year_1976+= round((1/(len(bbb))),2)
            elif v == 1977: year_1977+= round((1/(len(bbb))),2)
            elif v == 1978: year_1978+= round((1/(len(bbb))),2)
            elif v == 1979: year_1979+= round((1/(len(bbb))),2)
            elif v == 1980: year_1980+= round((1/(len(bbb))),2)
            elif v == 1981: year_1981+= round((1/(len(bbb))),2)
            elif v == 1982: year_1982+= round((1/(len(bbb))),2)
            elif v == 1983: year_1983+= round((1/(len(bbb))),2)
            elif v == 1984: year_1984+= round((1/(len(bbb))),2)
            elif v == 1985: year_1985+= round((1/(len(bbb))),2)
            elif v == 1986: year_1986+= round((1/(len(bbb))),2)
            elif v == 1987: year_1987+= round((1/(len(bbb))),2)
            elif v == 1988: year_1988+= round((1/(len(bbb))),2)
            elif v == 1989: year_1989+= round((1/(len(bbb))),2)
            elif v == 1990: year_1990+= round((1/(len(bbb))),2)
            elif v == 1991: year_1991+= round((1/(len(bbb))),2)
            elif v == 1992: year_1992+= round((1/(len(bbb))),2)
            elif v == 1993: year_1993+= round((1/(len(bbb))),2)
            elif v == 1994: year_1994+= round((1/(len(bbb))),2)
            elif v == 1995: year_1995+= round((1/(len(bbb))),2)
            elif v == 1996: year_1996+= round((1/(len(bbb))),2)
            elif v == 1997: year_1997+= round((1/(len(bbb))),2)
            elif v == 1998: year_1998+= round((1/(len(bbb))),2)
            elif v == 1999: year_1999+= round((1/(len(bbb))),2)
            elif v == 2000: year_2000+= round((1/(len(bbb))),2)
            elif v == 2001: year_2001+= round((1/(len(bbb))),2)
            elif v == 2002: year_2002+= round((1/(len(bbb))),2)
            elif v == 2003: year_2003+= round((1/(len(bbb))),2)
            elif v == 2004: year_2004+= round((1/(len(bbb))),2)
            elif v == 2005: year_2005+= round((1/(len(bbb))),2)
            elif v == 2006: year_2006+= round((1/(len(bbb))),2)
            elif v == 2007: year_2007+= round((1/(len(bbb))),2)
            elif v == 2008: year_2008+= round((1/(len(bbb))),2)
            elif v == 2009: year_2009+= round((1/(len(bbb))),2)
            elif v == 2010: year_2010+= round((1/(len(bbb))),2)
            elif v == 2011: year_2011+= round((1/(len(bbb))),2)
            elif v == 2012: year_2012+= round((1/(len(bbb))),2)
            elif v == 2013: year_2013+= round((1/(len(bbb))),2)
            elif v == 2014: year_2014+= round((1/(len(bbb))),2)
            elif v == 2015: year_2015+= round((1/(len(bbb))),2)
            elif v == 2016: year_2016+= round((1/(len(bbb))),2)
            elif v == 2017: year_2017+= round((1/(len(bbb))),2)
            elif v == 2018: year_2018+= round((1/(len(bbb))),2)
            elif v == 2019: year_2019+= round((1/(len(bbb))),2)
            elif v == 2020: year_2020+= round((1/(len(bbb))),2)
            elif v == 2021: year_2021+= round((1/(len(bbb))),2)
            elif v == 2022: year_2022+= round((1/(len(bbb))),2)


        years_dt = year_1801, year_1802, year_1803, year_1804, year_1805, year_1806, year_1807, year_1808, year_1809, year_1810, year_1811, year_1812, year_1813, year_1814, year_1815, year_1816, year_1817, year_1818, year_1819, year_1820, year_1821, year_1822, year_1823, year_1824, year_1825, year_1826, year_1827, year_1828, year_1829, year_1830, year_1831, year_1832, year_1833, year_1834, year_1835, year_1836, year_1837, year_1838, year_1839, year_1840, year_1841, year_1842, year_1843, year_1844, year_1845, year_1846, year_1847, year_1848, year_1849, year_1850, year_1851, year_1852, year_1853, year_1854, year_1855, year_1856, year_1857, year_1858, year_1859, year_1860, year_1861, year_1862, year_1863, year_1864, year_1865, year_1866, year_1867, year_1868, year_1869, year_1870, year_1871, year_1872, year_1873, year_1874, year_1875, year_1876, year_1877, year_1878, year_1879, year_1880, year_1881, year_1882, year_1883, year_1884, year_1885, year_1886, year_1887, year_1888, year_1889, year_1890, year_1891, year_1892, year_1893, year_1894, year_1895, year_1896, year_1897, year_1898, year_1899, year_1900, year_1901, year_1902, year_1903, year_1904, year_1905, year_1906, year_1907, year_1908, year_1909, year_1910, year_1911, year_1912, year_1913, year_1914, year_1915, year_1916, year_1917, year_1918, year_1919, year_1920, year_1921, year_1922, year_1923, year_1924, year_1925, year_1926, year_1927, year_1928, year_1929, year_1930, year_1931, year_1932, year_1933, year_1934, year_1935, year_1936, year_1937, year_1938, year_1939, year_1940, year_1941, year_1942, year_1943, year_1944, year_1945, year_1946, year_1947, year_1948, year_1949, year_1950, year_1951, year_1952, year_1953, year_1954, year_1955, year_1956, year_1957, year_1958, year_1959, year_1960, year_1961, year_1962, year_1963, year_1964, year_1965, year_1966, year_1967, year_1968, year_1969, year_1970, year_1971, year_1972, year_1973, year_1974, year_1975, year_1976, year_1977, year_1978, year_1979, year_1980, year_1981, year_1982, year_1983, year_1984, year_1985, year_1986, year_1987, year_1988, year_1989, year_1990, year_1991, year_1992, year_1993, year_1994, year_1995, year_1996, year_1997, year_1998, year_1999, year_2000, year_2001, year_2002, year_2003, year_2004, year_2005, year_2006, year_2007, year_2008, year_2009, year_2010, year_2011, year_2012, year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022
        years_dt = list(years_dt)
        with open(''+pyt+'\\date(1801-2022).txt', 'w', encoding="utf-8") as filehandle: 
          for listitem in years_dt: 
              filehandle.write('%s\n' % listitem)

def proc_data_3():

    im = csv_ob3.get()
    pyt = pyt_ob3.get()

    try:

        ### Проверка ###
        file_ = open(''+pyt+"\\col_name.txt", "r", encoding="utf-8")

        mb.showwarning("Внимание!", "Обработка уже выполнена")

        file_.close()
        ### Проверка ###

    except:
        
        df = pd.read_csv(""+pyt+"\\"+im+".csv")
        column = df['Название'].tolist()


        new_column = str(column)
        new_column = new_column.translate(str.maketrans({'[': '', ']': '', "'": '', '—': ''}))


        all_columns = new_column
        all_columns = all_columns.lower()

        spec_chars = string.punctuation + '\n\xa0«»\t—…1234567890' 
        all_columns = "".join([ch for ch in all_columns if ch not in spec_chars])

        nltk.download('punkt')
        tokenized_text = word_tokenize(all_columns)
        tokenized_text = nltk.Text(tokenized_text)

        tokenized_text = " ".join(tokenized_text)
        tokenized_text = tokenized_text.split()


        new_new = []
        morph = pymorphy2.MorphAnalyzer()
        for word in tokenized_text:
            p = morph.normal_forms(word)[0]
            new_new.append(p)

        with open(''+pyt+'\\col_name.txt', 'w', encoding="utf-8") as filehandle: 
            for listitem in new_new: 
                filehandle.write('%s\n' % listitem)

        print('Обработано слов: '+str(len(tokenized_text)))

def proc_data_4():

    im = csv_ob3.get()
    pyt = pyt_ob3.get()

    try:

        ### Проверка ###
        file_ = open(''+pyt+"\\col_description.txt", "r", encoding="utf-8")

        mb.showwarning("Внимание!", "Обработка уже выполнена")

        file_.close()
        ### Проверка ###

    except:
        
        df = pd.read_csv(""+pyt+"\\"+im+".csv")
        column = df['Описание'].tolist()


        new_column = str(column)
        new_column = new_column.translate(str.maketrans({'[': '', ']': '', "'": '', '—': ''}))


        all_columns = new_column
        all_columns = all_columns.lower()

        spec_chars = string.punctuation + '\n\xa0«»\t—…1234567890' 
        all_columns = "".join([ch for ch in all_columns if ch not in spec_chars])

        nltk.download('punkt')
        tokenized_text = word_tokenize(all_columns)
        tokenized_text = nltk.Text(tokenized_text)

        tokenized_text = " ".join(tokenized_text)
        tokenized_text = tokenized_text.split()


        new_new = []
        morph = pymorphy2.MorphAnalyzer()
        for word in tokenized_text:
            p = morph.normal_forms(word)[0]
            new_new.append(p)

        with open(''+pyt+'\\col_description.txt', 'w', encoding="utf-8") as filehandle: 
            for listitem in new_new: 
                filehandle.write('%s\n' % listitem)

        print('Обработано слов: '+str(len(tokenized_text)))


def delete_new_col():
    im = csv_ob3.get()
    pyt = pyt_ob3.get()
    if var4f.get() == 1:
        try:
            df = pd.read_csv(""+pyt+"\\"+im+".csv", encoding="utf-8")
            df = df.drop(columns=['Место_создания(обр.)'])
            df.to_csv(""+pyt+"\\"+im+".csv", encoding="utf-8", index=False)
        except:
            mb.showwarning("Внимание!", "Нет обработанного столбца")
    elif var4f.get() == 2: 
        try:
            df = pd.read_csv(""+pyt+"\\"+im+".csv", encoding="utf-8")
            df = df.drop(columns=['Период_создания(обр.)'])
            df.to_csv(""+pyt+"\\"+im+".csv", encoding="utf-8", index=False)
            os.remove(''+pyt+"\\date(1801-2022).txt")
        except:
            mb.showwarning("Внимание!", "Нет обработанного столбца")
    elif var4f.get() == 4: 
        try:
            os.remove(''+pyt+"\\col_name.txt")
        except:
            mb.showwarning("Внимание!", "Нет обработанного столбца")
    elif var4f.get() == 5: 
        try:
            os.remove(''+pyt+"\\col_description.txt")
        except:
            mb.showwarning("Внимание!", "Нет обработанного столбца")
        
def analysis_choice():

    if var2.get() == 1: analysis1()
    elif var2.get() == 2: analysis2()
    elif var2.get() == 3: analysis3()
    elif var2.get() == 4: analysis4()


def analysis1():

    color = '1f77b4'

    chrome = pyt_Input2.get()
    im = im_Input2.get()
    qua = int(qua_Input.get())
    size1 = size1_Input.get()
    size2 = size2_Input.get()
    head = head_Input.get()
    pyt = pyt_Input2.get()

    all_col = []

    vvod = var2f.get()

    if vvod == 1: vvod = 'Название'
    elif vvod == 2: vvod = 'Описание'
    elif vvod == 3: vvod = 'Технологии'
    elif vvod == 4: vvod = 'Типология'
    elif vvod == 5: vvod = 'ID_Музея'
    elif vvod == 6: vvod = 'Место_создания'
    elif vvod == 7: vvod = 'Место_создания(обр.)'


    df = pd.read_csv(""+pyt+"\\"+im+".csv")
    a = df[vvod].tolist()

    le = len(a)

    a = [i for i in a if i != '—']
    new_a = []
    for element in a:
        element = str(element)
        element = re.sub(r'\([^()]*\)', '', element)
        if vvod == 'Технологии':
            new_a += element.split(',')
        else:
            new_a += element.split('`|`')
    all_col = [x.strip() for x in new_a]


    array_d = {}.fromkeys(all_col, 0)
    for a in all_col:
        array_d[a] += 1

    array_d = {k: array_d[k] for k in sorted(array_d, key=array_d.get, reverse=True)}

    def addlabels(x,y):
      for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

    xxx = list(array_d.keys())[0:qua]
    yyy = list(array_d.values())[0:qua]

    fig = plt.figure()
    fig.set_figheight(int(size1))
    fig.set_figwidth(int(size2))
    plt.bar(xxx, yyy, color=("#"+color))
    addlabels(xxx, yyy)
    plt.title(head+' ('+str(le)+')')
    plt.ylabel('Количество')
    plt.xticks(rotation=90)
    fig.savefig(""+chrome+"\\"+head+".png", bbox_inches="tight")

def analysis2():

    color = 'Set1/000000'

    chrome = pyt_Input2.get()
    im = im_Input2.get()
    qua = int(qua_Input.get())
    size1 = size1_Input.get()
    size2 = size2_Input.get()
    head = head_Input.get()
    pyt = pyt_Input2.get()


    all_col = []

    vvod = var2f.get()

    if vvod == 1: vvod = 'col_name'
    elif vvod == 2: vvod = 'col_description'

    with open(''+pyt+"\\"+vvod+'.txt', 'r', encoding="utf-8") as filehandle: 
        new_new = [current_place.rstrip() for current_place in filehandle.readlines()]

    new_new = list(filter(None, new_new))

    stop_words = []
    try:
        with open(""+pyt+"\\stopwords.txt", encoding="utf-8") as file: stop_words = [row.strip() for row in file]
    except FileNotFoundError:
        stop_words = []

    new_new = [word for word in new_new if word not in stop_words]


    array_dd = {}.fromkeys(new_new, 0)
    for a in new_new:
            array_dd[a] += 1
    array_dd = {k: array_dd[k] for k in sorted(array_dd, key=array_dd.get, reverse=True)}


    w = int(size2)
    h = int(size1)

    xxx = list(array_dd.keys())[0:qua]
    yyy = list(array_dd.values())[0:qua]

    new = " ".join(xxx)

    color = color.split('/')
    color[1] = '#'+color[1]

    cloud = WordCloud(width=100*w, height=100*h, background_color=color[1], colormap=color[0], max_words=qua,contour_width=0).generate(new)
    plt.figure(figsize=(w,h))
    plt.imshow(cloud)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(""+chrome+"\\"+head+".png", bbox_inches='tight')


def analysis3():

    color = 'FF9D73/FFC673/FFE173/E6FB71/92ED6B/60D4AE/6899D3'

    chrome = pyt_Input2.get()
    im = im_Input2.get()
    size1 = size1_Input.get()
    size2 = size2_Input.get()
    head = head_Input.get()
    pyt = pyt_Input2.get()

    df = pd.read_csv(""+pyt+"\\"+im+".csv")

    column_1 = df['Автор'].tolist()
    column_2 = df['Название'].tolist()
    column_3 = df['Описание'].tolist()
    column_4 = df['Период_создания'].tolist()
    column_5 = df['Технологии'].tolist()
    column_6 = df['Размер'].tolist()
    column_7 = df['Место_создания'].tolist()

    kol_0 = len(column_1)

    new_column_1 = column_1
    nc1_len = len(new_column_1)
    new_column_1 = [i for i in new_column_1 if i == '—']

    new_column_2 = column_2
    nc2_len = len(new_column_2)
    new_column_2 = [i for i in new_column_2 if i == '—']

    new_column_3 = column_3
    nc3_len = len(new_column_3)
    new_column_3 = [i for i in new_column_3 if i == '—']

    new_column_4 = column_4
    nc4_len = len(new_column_4)
    new_column_4 = [i for i in new_column_4 if i == '—' or i == ' ']

    new_column_5 = column_5
    nc5_len = len(new_column_5)
    new_column_5 = [i for i in new_column_5 if i == '—']

    new_column_6 = column_6
    nc6_len = len(new_column_6)
    new_column_6 = [i for i in new_column_6 if i == '—']

    new_column_7 = column_7
    nc7_len = len(column_7)
    new_column_7 = [i for i in new_column_7 if i == '—']



    names = ['Автор','Название','Описание','Период_создания','Технологии','Размер','Место_создания']
    kol = [len(new_column_1), len(new_column_2), len(new_column_3), len(new_column_4), len(new_column_5), len(new_column_6), len(new_column_7)]

    n_k1 = [names[0], kol[0]]
    n_k2 = [names[1], kol[1]]
    n_k3 = [names[2], kol[2]]
    n_k4 = [names[3], kol[3]]
    n_k5 = [names[4], kol[4]]
    n_k6 = [names[5], kol[5]]
    n_k7 = [names[6], kol[6]]

    k_nk = [n_k1[0], n_k2[0], n_k3[0], n_k4[0], n_k5[0], n_k6[0], n_k7[0] ]
    ar_nk = [int(n_k1[1]), int(n_k2[1]), int(n_k3[1]), int(n_k4[1]), int(n_k5[1]), int(n_k6[1]), int(n_k7[1])]

    ddd = dict(zip(k_nk, ar_nk))
    ddd = {k: ddd[k] for k in sorted(ddd, key=ddd.get, reverse=True)}

    dd = list(map(list, ddd.items()))

    new_names = [dd[0][0], dd[1][0], dd[2][0], dd[3][0], dd[4][0], dd[5][0], dd[6][0]]
    new_kol = [dd[0][1], dd[1][1], dd[2][1], dd[3][1], dd[4][1], dd[5][1], dd[6][1]]
    kol_2 = [kol_0-new_kol[0], kol_0-new_kol[1], kol_0-new_kol[2], kol_0-new_kol[3], kol_0-new_kol[4], kol_0-new_kol[5], kol_0-new_kol[6]]


    s = []

    for i in range(7):
        height = round(new_kol[i] / kol_0 * 100, 2)
        label_text = str(height)+'%'
        s.append(label_text)

    new_nm = []

    for n in range(7):
      new_nm.append(new_names[n] + ' (' + str(s[n])+' / '+str(new_kol[n])+ ')')

    df = pd.DataFrame.from_dict({'Name': new_nm,'fill': new_kol,'empty': kol_2,'Total': kol_0})

    fig = plt.figure()
    fig.set_figheight(int(size1))
    fig.set_figwidth(int(size2))

    df['fill fill'] = df['fill'] / df['Total'] * 100
    df['empty empty'] = df['empty'] / df['Total'] * 100

    plt.bar(x=df['Name'], height=df['fill fill'], label='Пропуски')
    plt.bar(x=df['Name'], height=df['empty empty'], bottom=df['fill fill'], label='Заполнено')


    plt.title(head+' ('+str(kol_0)+')')
    plt.ylabel('Количество (%)')
    plt.xticks(rotation=90)
    plt.legend()
    fig.savefig(""+chrome+"\\"+head+".png", bbox_inches="tight")

def analysis4():

    color = '1f77b4'

    chrome = pyt_Input2.get()
    im = im_Input2.get()
    qua = qua_Input.get()
    size1 = size1_Input.get()
    size2 = size2_Input.get()
    head = head_Input.get()
    pyt = pyt_Input2.get()

    df = pd.read_csv(""+pyt+"\\"+im+".csv")

    kol = 0

    y = []
    try:
        with open(''+pyt+"\\date(1801-2022).txt", encoding="utf-8") as file: y = [row.strip() for row in file]
    except FileNotFoundError:
        y = []

    for i in range(len(y)):
      y[i] = float(y[i])

    for k in range(len(y)):
      kol += y[k]
    kol = round(kol)

    x = [1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    fig = plt.figure()

    #ticks = x
    #plt.xticks([ticks[i] for i in range(len(ticks)) if i % 10 == 0])

    plt.title(str(head)+' ('+str(round(kol/len(df)*100,2))+'%)')
    plt.plot(x, y, color=("#1f77b4"))
    plt.ylabel('Количество')
    fig.set_figheight(int(size1))
    fig.set_figwidth(int(size2))
    ax = plt.gca()

    ax.set_facecolor('#FFFFFF')
    ax.grid(color = '#000000',    #  цвет линий
            linewidth = 1,    #  толщина
            linestyle = '--',alpha=0.5) 

    fig.savefig(""+chrome+"\\"+head+".png", dpi=100)



def avtozap():
    minus()
    avtoz1 =open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[0]
    avtoz2 =open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[1]
    avtoz3 =open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[2]
    avtoz4 =open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[3]
    avtoz5 =open(r"autofill_scraping.txt", "r", encoding="utf-8").read().split('\n')[4]
    zap_Input.insert(0, avtoz1)
    muz_Input.insert(0, avtoz2)
    zapch_Input.insert(0, avtoz3)
    pyt_Input.insert(0, avtoz4)
    im_Input.insert(0, avtoz5)

def minus():
    zap_Input.delete(0, END)
    muz_Input.delete(0, END)
    zapch_Input.delete(0, END)
    pyt_Input.delete(0, END)
    im_Input.delete(0, END)

def avtozap2():
    minus2()
    avtoz1 =open(r"autofill_visualization.txt", "r", encoding="utf-8").read().split('\n')[0]
    avtoz2 =open(r"autofill_visualization.txt", "r", encoding="utf-8").read().split('\n')[1]
    avtoz3 =open(r"autofill_visualization.txt", "r", encoding="utf-8").read().split('\n')[2]
    avtoz4 =open(r"autofill_visualization.txt", "r", encoding="utf-8").read().split('\n')[3]
    avtoz5 =open(r"autofill_visualization.txt", "r", encoding="utf-8").read().split('\n')[4]
    avtoz6 =open(r"autofill_visualization.txt", "r", encoding="utf-8").read().split('\n')[5]
    head_Input.insert(0, avtoz1)
    qua_Input.insert(0, avtoz2)
    size1_Input.insert(0, avtoz3)
    size2_Input.insert(0, avtoz4)
    pyt_Input2.insert(0, avtoz5)
    im_Input2.insert(0, avtoz6)


def minus2():
    head_Input.delete(0, END)
    qua_Input.delete(0, END)
    size1_Input.delete(0, END)
    size2_Input.delete(0, END)
    pyt_Input2.delete(0, END)
    im_Input2.delete(0, END)

def avtozap3():
    minus3()
    avtoz1 =open(r"autofill_scraping_api.txt", "r", encoding="utf-8").read().split('\n')[0]
    avtoz2 =open(r"autofill_scraping_api.txt", "r", encoding="utf-8").read().split('\n')[1]
    avtoz3 =open(r"autofill_scraping_api.txt", "r", encoding="utf-8").read().split('\n')[2]
    avtoz4 =open(r"autofill_scraping_api.txt", "r", encoding="utf-8").read().split('\n')[3]
    avtoz5 =open(r"autofill_scraping_api.txt", "r", encoding="utf-8").read().split('\n')[4]
    zap_Input3.insert(0, avtoz1)
    muz_Input3.insert(0, avtoz2)
    api_Input3.insert(0, avtoz3)
    pyt_Input3.insert(0, avtoz4)
    im_Input3.insert(0, avtoz5)

def minus3():
    zap_Input3.delete(0, END)
    muz_Input3.delete(0, END)
    api_Input3.delete(0, END)
    pyt_Input3.delete(0, END)
    im_Input3.delete(0, END)


def avtozap4():
    minus4()
    avtoz1 =open(r"autofill_processing.txt", "r", encoding="utf-8").read().split('\n')[0]
    avtoz2 =open(r"autofill_processing.txt", "r", encoding="utf-8").read().split('\n')[1]
    pyt_ob3.insert(0, avtoz1)
    csv_ob3.insert(0, avtoz2)

def minus4():
    pyt_ob3.delete(0, END)
    csv_ob3.delete(0, END)


root = tk.Tk()
root.title('SGAT v0.9.8')
root.geometry("650x400")
root.resizable(width=False, height=False)
root.iconbitmap('icon.ico')

note =Notebook(root)

frame1= Frame(note, background="grey")
frame2 = Frame(note, background="grey")
frame3 = Frame(note, background="grey")
frame4 = Frame(note, background="grey")

note.add(frame1, text= '    Скрэйпинг (opendata.mkrf.ru)    ')
note.add(frame2, text= '    Скрэйпинг (goskatalog.ru)    ')
note.add(frame4, text= '    Обработка    ')
note.add(frame3, text= '    Визуализация    ')

frame_for_hight = Frame(background="gray")
f1 = frame_for_hight.place(in_=frame2, anchor="c", relx=.08, rely=.08)

frame_for_center = Frame(background="gray")
f2 = frame_for_center.place(in_=frame2, anchor="c", relx=.50, rely=.26)

frame_for_center2 = Frame(background="gray")
f3 = frame_for_center2.place(in_=frame2, anchor="c", relx=.50, rely=.42)

frame_for_center3 = Frame(background="gray")
f4 = frame_for_center3.place(in_=frame2, anchor="c", relx=.50, rely=.70)

frame_for_down = Frame(background="gray")
f5 = frame_for_down.place(in_=frame2, anchor="c", relx=.92, rely=.92)

frame_for_by = Frame(background="gray")
f7 = frame_for_by.place(in_=frame2, anchor="c", relx=.5, rely=.92)


icon_i = PhotoImage(file="i.png")
photoimage_i = icon_i.subsample(2, 2)
btninfo = Button(frame_for_hight, command=info,image=photoimage_i, text='i', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btninfo.grid(row=0, column=0, ipadx=0, ipady=0, padx=6, pady=0) 
Hovertip(btninfo,' Получение информации о количестве \n объектов по запросу ')

icon_m = PhotoImage(file="m.png")
photoimage_m = icon_m.subsample(2, 2)
btnmus = Button(frame_for_hight, command=museums,image=photoimage_m,text='m', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnmus.grid(row=0, column=1, ipadx=0, ipady=0, padx=6, pady=0) 
Hovertip(btnmus,' Формирование txt-файла с "id" \n и "названием" всех музеев ')


title_zap = Label(frame_for_center, text='Ваш запрос', bg='gray',fg='white', font=("Century Gothic", 10))
title_zap.grid(row=1, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 
zap_Input = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
zap_Input.grid(row=2, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2)

title_muz = Label(frame_for_center, text='ID музея', bg='gray',fg='white', font=("Century Gothic", 10))
title_muz.grid(row=1, column=2, ipadx=1, ipady=0, padx=15, pady=0) 
muz_Input = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=11)
muz_Input.grid(row=2, column=2, ipadx=1, ipady=0, padx=15, pady=0) 

title_zapch = Label(frame_for_center, text='Количество', bg='gray',fg='white', font=("Century Gothic", 10))
title_zapch.grid(row=1, column=3, ipadx=0, ipady=0, padx=15, pady=0) 
zapch_Input = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=11)
zapch_Input.grid(row=2, column=3, ipadx=0, ipady=0, padx=15, pady=0) 


title_pyt = Label(frame_for_center2, text='Путь к папке', bg='gray',fg='white', font=("Century Gothic", 10))
title_pyt.grid(row=3, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 
pyt_Input = Entry(frame_for_center2, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
pyt_Input.grid(row=4, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 

title_im = Label(frame_for_center2, text='Имя CSV', bg='gray',fg='white', font=("Century Gothic", 10))
title_im.grid(row=3, column=2, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 
im_Input = Entry(frame_for_center2, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
im_Input.grid(row=4, column=2, ipadx=3, ipady=0, padx=15, pady=0, columnspan=2) 


btngo = Button(frame_for_center3, command=spisok, text='Создать список элементов', bg='white', height=1, width=27, font=("Century Gothic", 10, "bold"))
btngo.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=8)

btngo = Button(frame_for_center3, command=nazhat_sbor, text='Начать сбор данных', bg='white', height=1, width=27, font=("Century Gothic", 10, "bold"))
btngo.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=8)


icon_plus = PhotoImage(file="+.png")
photoimage_plus = icon_plus.subsample(2, 2)
btnp = Button(frame_for_down, command=avtozap, image=photoimage_plus, text='+', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnp.grid(row=0, column=0, ipadx=0, ipady=0, padx=6, pady=0) 

icon_minus = PhotoImage(file="-.png")
photoimage_minus = icon_minus.subsample(2, 2)
btnm = Button(frame_for_down, command=minus, image=photoimage_minus, text='-', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnm.grid(row=0, column=1, ipadx=0, ipady=0, padx=6, pady=0)


def on_enter(e): title_version['fg'] = 'white'
def on_leave(e): title_version['fg'] = 'gray'
title_version = Label(frame_for_by, text='powered by Konstantin Kozhin', bg='gray',fg='gray', font=("Century Gothic", 9),justify=CENTER)
title_version.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
title_version.bind("<Enter>", on_enter)
title_version.bind("<Leave>", on_leave)



frame_for_hight = LabelFrame(background="gray", text='Параметр запроса', bg='gray', fg='white', font=("Century Gothic", 10), labelanchor="n")
f1 = frame_for_hight.place(in_=frame1, anchor="c", relx=.50, rely=.13)

frame_for_center = Frame(background="gray")
f2 = frame_for_center.place(in_=frame1, anchor="c", relx=.50, rely=.32)

frame_for_center2 = Frame(background="gray")
f3 = frame_for_center2.place(in_=frame1, anchor="c", relx=.50, rely=.48)

frame_for_center3 = Frame(background="gray")
f4 = frame_for_center3.place(in_=frame1, anchor="c", relx=.50, rely=.70)

frame_for_down = Frame(background="gray")
f5 = frame_for_down.place(in_=frame1, anchor="c", relx=.92, rely=.92)

frame_for_by = Frame(background="gray")
f7 = frame_for_by.place(in_=frame1, anchor="c", relx=.5, rely=.92)


var = IntVar()
var.set(1)

req_1 = Radiobutton(frame_for_hight, value=1, text='Лемма', variable=var, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 10),selectcolor='gray')
req_1.grid(row=0, column=0, ipadx=0, ipady=0, padx=6, pady=0) 

req_2 = Radiobutton(frame_for_hight, value=2, text='Словоформа', variable=var, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 10),selectcolor='gray')
req_2.grid(row=0, column=1, ipadx=0, ipady=0, padx=6, pady=0) 


title_zap3 = Label(frame_for_center, text='Ваш запрос', bg='gray',fg='white', font=("Century Gothic", 10))   
title_zap3.grid(row=1, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 
zap_Input3 = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
zap_Input3.grid(row=2, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2)

title_muz3 = Label(frame_for_center, text='КОПУК музея', bg='gray',fg='white', font=("Century Gothic", 10))
title_muz3.grid(row=1, column=2, ipadx=1, ipady=0, padx=15, pady=0) 
muz_Input3 = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=11)
muz_Input3.grid(row=2, column=2, ipadx=1, ipady=0, padx=15, pady=0) 

title_api3 = Label(frame_for_center, text='API-ключ', bg='gray',fg='white', font=("Century Gothic", 10))
title_api3.grid(row=1, column=3, ipadx=2, ipady=0, padx=15, pady=0)
api_Input3 = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=11)
api_Input3.grid(row=2, column=3, ipadx=0, ipady=0, padx=15, pady=0) 


title_pyt3 = Label(frame_for_center2, text='Путь к папке', bg='gray',fg='white', font=("Century Gothic", 10))
title_pyt3.grid(row=3, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 
pyt_Input3 = Entry(frame_for_center2, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
pyt_Input3.grid(row=4, column=0, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 

title_im3 = Label(frame_for_center2, text='Имя CSV', bg='gray',fg='white', font=("Century Gothic", 10))
title_im3.grid(row=3, column=2, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2) 
im_Input3 = Entry(frame_for_center2, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
im_Input3.grid(row=4, column=2, ipadx=3, ipady=0, padx=15, pady=0, columnspan=2)


btngo = Button(frame_for_center3, command=sbor_api, text='Начать сбор данных', bg='white', height=1, width=27, font=("Century Gothic", 10, "bold"))
btngo.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=8)

icon_plus_ = PhotoImage(file="+.png")
photoimage_plus_ = icon_plus_.subsample(2, 2)
btnp_ = Button(frame_for_down, command=avtozap3, image=photoimage_plus, text='+', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnp_.grid(row=0, column=0, ipadx=0, ipady=0, padx=6, pady=0) 

icon_minus_ = PhotoImage(file="-.png")
photoimage_minus_ = icon_minus_.subsample(2, 2)
btnm_ = Button(frame_for_down, command=minus3, image=photoimage_minus, text='-', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnm_.grid(row=0, column=1, ipadx=0, ipady=0, padx=6, pady=0)


def on_enter(e): title_version1['fg'] = 'white'
def on_leave(e): title_version1['fg'] = 'gray'
title_version1 = Label(frame_for_by, text='powered by Konstantin Kozhin', bg='gray',fg='gray', font=("Century Gothic", 9),justify=CENTER)
title_version1.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
title_version1.bind("<Enter>", on_enter)
title_version1.bind("<Leave>", on_leave)


### Анализ ###

frame_for_hight = LabelFrame(background="gray", text='Способ визуализации', bg='gray', fg='white', font=("Century Gothic", 10), labelanchor="n")
f1 = frame_for_hight.place(in_=frame3, anchor="c", relx=.50, rely=.1)

frame_for_center = LabelFrame(background="gray", text='Данные для визуализации', bg='gray', fg='white', font=("Century Gothic", 10), labelanchor="n")
f2 = frame_for_center.place(in_=frame3, anchor="c", relx=.50, rely=.26)

frame_for_center2 = Frame(background="gray")
f3 = frame_for_center2.place(in_=frame3, anchor="c", relx=.50, rely=.40)

frame_for_center3 = Frame(background="gray")
f4 = frame_for_center3.place(in_=frame3, anchor="c", relx=.50, rely=.53)

frame_for_center4 = Frame(background="gray")
f4 = frame_for_center4.place(in_=frame3, anchor="c", relx=.50, rely=.66)

frame_for_center5 = Frame(background="gray")
f4 = frame_for_center5.place(in_=frame3, anchor="c", relx=.50, rely=.82)

frame_for_down = Frame(background="gray")
f5 = frame_for_down.place(in_=frame3, anchor="c", relx=.92, rely=.92)

frame_for_by = Frame(background="gray")
f5 = frame_for_by.place(in_=frame3, anchor="c", relx=.5, rely=.92)

var2 = IntVar()
var2.set(1)

def vision_an1():
    var2f.set(3)
    qua_Input['state']='normal'

    an_1f.grid_remove()
    an_2f.grid_remove()
    an_3f.grid(row=1, column=2, ipadx=0, ipady=0, padx=3, pady=0)
    an_4f.grid(row=1, column=3, ipadx=0, ipady=0, padx=3, pady=0)
    an_7f.grid(row=1, column=6, ipadx=0, ipady=0, padx=3, pady=0)
    title_4analis.grid_remove()
    title_3analis.grid_remove()
def vision_an2():
    var2f.set(1)
    qua_Input['state']='normal'

    an_3f.grid_remove()
    an_4f.grid_remove()
    an_1f.grid(row=1, column=0, ipadx=0, ipady=0, padx=3, pady=0)
    an_2f.grid(row=1, column=1, ipadx=0, ipady=0, padx=3, pady=0)
    an_7f.grid_remove()
    title_4analis.grid_remove()
    title_3analis.grid_remove()
def vision_an3():
    qua_Input.delete(0, END)
    qua_Input['state']='readonly'

    an_1f.grid_remove()
    an_2f.grid_remove()
    an_3f.grid_remove()
    an_4f.grid_remove()
    an_7f.grid_remove()
    title_3analis.grid(row=1, column=10, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2)
    title_4analis.grid_remove()
def vision_an4():
    qua_Input.delete(0, END)
    qua_Input['state']='readonly'

    an_1f.grid_remove()
    an_2f.grid_remove()
    an_3f.grid_remove()
    an_4f.grid_remove()
    an_7f.grid_remove()
    title_4analis.grid(row=1, column=10, ipadx=0, ipady=0, padx=15, pady=0, columnspan=2)
    title_3analis.grid_remove()

an1 = PhotoImage(file="1.png").subsample(2, 2)
an_1 = Radiobutton(frame_for_hight, image=an1, command=vision_an1, value=1, text='1', variable=var2, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 10),selectcolor='gray')
an_1.grid(row=0, column=0, ipadx=0, ipady=0, padx=6, pady=0) 

an2 = PhotoImage(file="2.png").subsample(2, 2)
an_2 = Radiobutton(frame_for_hight, image=an2, command=vision_an2, value=2, text='2', variable=var2, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 10),selectcolor='gray')
an_2.grid(row=0, column=1, ipadx=0, ipady=0, padx=6, pady=0) 

an3 = PhotoImage(file="3.png").subsample(2, 2)
an_3 = Radiobutton(frame_for_hight, image=an3, command=vision_an3, value=3, text='3', variable=var2, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 10),selectcolor='gray')
an_3.grid(row=0, column=2, ipadx=0, ipady=0, padx=6, pady=0) 

an4 = PhotoImage(file="4.png").subsample(2, 2)
an_4 = Radiobutton(frame_for_hight, image=an4, command=vision_an4, value=4, text='4', variable=var2, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 10),selectcolor='gray')
an_4.grid(row=0, column=3, ipadx=0, ipady=0, padx=6, pady=0)

#an5 = PhotoImage(file="5.png").subsample(2, 2)
#an_5 = Radiobutton(frame_for_hight, image=an5, value=5, text='5', variable=var2, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 10),selectcolor='gray')
#an_5.grid(row=0, column=4, ipadx=0, ipady=0, padx=6, pady=0) 
#an_5['state']='disabled'

var2f = IntVar()
var2f.set(3)

an_1f = Radiobutton(frame_for_center, value=1, text='Название', variable=var2f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')

an_2f = Radiobutton(frame_for_center, value=2, text='Описание', variable=var2f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')

an_3f = Radiobutton(frame_for_center, value=3, text='Технологии', variable=var2f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
an_3f.grid(row=1, column=0, ipadx=0, ipady=0, padx=3, pady=0)

an_4f = Radiobutton(frame_for_center, value=4, text='Типология', variable=var2f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
an_4f.grid(row=1, column=1, ipadx=0, ipady=0, padx=3, pady=0)

an_7f = Radiobutton(frame_for_center, value=7, text='Место_создания(обр.)', variable=var2f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
an_7f.grid(row=1, column=2, ipadx=0, ipady=0, padx=3, pady=0)

title_3analis = Label(frame_for_center, text='"Визуализация пропусков в метаданных"', bg='gray',fg='white', font=("Century Gothic", 10))   

title_4analis = Label(frame_for_center, text='"Визуализация объектов по времени"', bg='gray',fg='white', font=("Century Gothic", 10))
    



title_head = Label(frame_for_center2, text='Имя графика', bg='gray',fg='white', font=("Century Gothic", 10))
title_head.grid(row=1, column=0, ipadx=0, ipady=0, padx=15, pady=0)
head_Input = Entry(frame_for_center2, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
head_Input.grid(row=2, column=0, ipadx=0, ipady=0, padx=15, pady=0)

title_qua = Label(frame_for_center2, text='Количество', bg='gray',fg='white', font=("Century Gothic", 10))   
title_qua.grid(row=1, column=1, ipadx=0, ipady=0, padx=15, pady=0)
qua_Input = Entry(frame_for_center2, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
qua_Input.grid(row=2, column=1, ipadx=0, ipady=0, padx=15, pady=0)


title_size1 = Label(frame_for_center3, text='Высота', bg='gray',fg='white', font=("Century Gothic", 10))
title_size1.grid(row=1, column=0, ipadx=0, ipady=0, padx=15, pady=0)
size1_Input = Entry(frame_for_center3, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
size1_Input.grid(row=2, column=0, ipadx=0, ipady=0, padx=15, pady=0)

title_size2 = Label(frame_for_center3, text='Ширина', bg='gray',fg='white', font=("Century Gothic", 10))
title_size2.grid(row=1, column=1, ipadx=0, ipady=0, padx=15, pady=0)
size2_Input = Entry(frame_for_center3, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
size2_Input.grid(row=2, column=1, ipadx=0, ipady=0, padx=15, pady=0)


title_pyt2 = Label(frame_for_center4, text='Путь к папке', bg='gray',fg='white', font=("Century Gothic", 10))
title_pyt2.grid(row=1, column=0, ipadx=0, ipady=0, padx=15, pady=0)
pyt_Input2 = Entry(frame_for_center4, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
pyt_Input2.grid(row=2, column=0, ipadx=0, ipady=0, padx=15, pady=0)

title_im2 = Label(frame_for_center4, text='Имя CSV', bg='gray',fg='white', font=("Century Gothic", 10))
title_im2.grid(row=1, column=1, ipadx=0, ipady=0, padx=15, pady=0)
im_Input2 = Entry(frame_for_center4, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
im_Input2.grid(row=2, column=1, ipadx=0, ipady=0, padx=15, pady=0)




btngoa = Button(frame_for_center5, command=analysis_choice, text='Визуализировать', bg='white', height=1, width=27, font=("Century Gothic", 10, "bold"))
btngoa.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)


icon_plus2 = PhotoImage(file="+.png")
photoimage_plus2 = icon_plus.subsample(2, 2)
btnp2 = Button(frame_for_down, command=avtozap2, image=photoimage_plus, text='+', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnp2.grid(row=0, column=0, ipadx=0, ipady=0, padx=6, pady=0)

icon_minus2 = PhotoImage(file="-.png")
photoimage_minus2 = icon_minus.subsample(2, 2)
btnm2 = Button(frame_for_down, command=minus2, image=photoimage_minus, text='-', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnm2.grid(row=0, column=1, ipadx=0, ipady=0, padx=6, pady=0)


def on_enter(e): title_version2['fg'] = 'white'
def on_leave(e): title_version2['fg'] = 'gray'
title_version2 = Label(frame_for_by, text='powered by Konstantin Kozhin', bg='gray',fg='gray', font=("Century Gothic", 9),justify=CENTER)
title_version2.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
title_version2.bind("<Enter>", on_enter)
title_version2.bind("<Leave>", on_leave)


### Обработка ###

frame_for_hight = LabelFrame(background="gray", text='Данные для обработки', bg='gray', fg='white', font=("Century Gothic", 10), labelanchor="n")
f1 = frame_for_hight.place(in_=frame4, anchor="c", relx=.50, rely=.25)

frame_for_center = Frame(background="gray")
f2 = frame_for_center.place(in_=frame4, anchor="c", relx=.50, rely=.42)

frame_for_center2 = Frame(background="gray")
f3 = frame_for_center2.place(in_=frame4, anchor="c", relx=.50, rely=.67)


frame_for_down = Frame(background="gray")
f4 = frame_for_down.place(in_=frame4, anchor="c", relx=.92, rely=.92)

frame_for_by = Frame(background="gray")
f5 = frame_for_by.place(in_=frame4, anchor="c", relx=.5, rely=.92)




var4f = IntVar()
var4f.set(1)

ob_1f = Radiobutton(frame_for_hight, value=1, text='Место_создания', variable=var4f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
ob_1f.grid(row=1, column=0, ipadx=0, ipady=0, padx=3, pady=0)

ob_2f = Radiobutton(frame_for_hight, value=2, text='Период_создания', variable=var4f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
ob_2f.grid(row=1, column=1, ipadx=0, ipady=0, padx=3, pady=0)

#ob_3f = Radiobutton(frame_for_hight, value=3, text='Технологии', variable=var4f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
#ob_3f.grid(row=1, column=2, ipadx=0, ipady=0, padx=3, pady=0)

ob_4f = Radiobutton(frame_for_hight, value=4, text='Название', variable=var4f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
ob_4f.grid(row=1, column=3, ipadx=0, ipady=0, padx=3, pady=0)

ob_5f = Radiobutton(frame_for_hight, value=5, text='Описание', variable=var4f, bg='gray',activebackground='gray',fg='white', font=("Century Gothic", 8),selectcolor='gray')
ob_5f.grid(row=1, column=4, ipadx=0, ipady=0, padx=3, pady=0)


title_pyt_ob3 = Label(frame_for_center, text='Путь к папке', bg='gray',fg='white', font=("Century Gothic", 9))
title_pyt_ob3.grid(row=1, column=0, ipadx=0, ipady=0, padx=15, pady=0)
pyt_ob3 = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
pyt_ob3.event_add('<<Paste>>', '<Control-igrave>')
pyt_ob3.grid(row=2, column=0, ipadx=0, ipady=0, padx=15, pady=0)

title_csv_ob3 = Label(frame_for_center, text='Имя CSV', bg='gray',fg='white', font=("Century Gothic", 9))
title_csv_ob3.grid(row=1, column=1, ipadx=0, ipady=0, padx=15, pady=0)
csv_ob3 = Entry(frame_for_center, bg='white', font=("Century Gothic", 13, "bold"), justify=CENTER, width=25)
csv_ob3.grid(row=2, column=1, ipadx=0, ipady=0, padx=15, pady=0)



btngo_ob3 = Button(frame_for_center2, command=proc_data_choice, text='Обработать', bg='white', height=1, width=25, font=("Century Gothic", 10, "bold"))
btngo_ob3.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=8)

btngo_ob4 = Button(frame_for_center2, command=delete_new_col, text='Очистить обработку', bg='white', height=1, width=25, font=("Century Gothic", 10, "bold"))
btngo_ob4.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=8)




icon_plus_ob = PhotoImage(file="+.png")
photoimage_plus_ob = icon_plus_ob.subsample(2, 2)
btnp_ob = Button(frame_for_down, command=avtozap4, image=photoimage_plus, text='+', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnp_ob.grid(row=0, column=0, ipadx=0, ipady=0, padx=6, pady=0) 

icon_minus_ob = PhotoImage(file="-.png")
photoimage_minus_ob = icon_minus_ob.subsample(2, 2)
btnm_ob = Button(frame_for_down, command=minus4, image=photoimage_minus, text='-', bg='white', height=25, width=25, font=("Century Gothic", 10, "bold"), justify=CENTER)
btnm_ob.grid(row=0, column=1, ipadx=0, ipady=0, padx=6, pady=0)


def on_enter(e): title_version3['fg'] = 'white'
def on_leave(e): title_version3['fg'] = 'gray'
title_version3 = Label(frame_for_by, text='powered by Konstantin Kozhin', bg='gray',fg='gray', font=("Century Gothic", 9),justify=CENTER)
title_version3.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
title_version3.bind("<Enter>", on_enter)
title_version3.bind("<Leave>", on_leave)



note.pack(expand= True, fill='both', padx=0, pady=0)
root.mainloop()