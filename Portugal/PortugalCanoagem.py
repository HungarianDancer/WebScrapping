import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import requests
from selenium.webdriver.chrome.options import Options
import csv

options = Options()
options.add_argument('--headless')



navegador = webdriver.Chrome(options=options)

url ='https://www.fpcanoagem.pt/comunidade/clubes'
#open selenium
PATH = "C:/Python/Python310/chromedriver.exe"
navegador = webdriver.Chrome(PATH)
navegador.get(url)

sleep(10)

try:
    buttom_press_1 = navegador.find_element(By.XPATH, '//*[@id="corpo-content"]/div[3]/div[2]/div/div[4]/div[21]/div')
    buttom_press_1.click()
    sleep(3)
    buttom_press_2 = navegador.find_element(By.XPATH, '//*[@id="corpo-content"]/div[3]/div[2]/div/div[4]/div[42]/div')
    buttom_press_2.click()
    sleep(3)
    buttom_press_3 = navegador.find_element(By.XPATH, '//*[@id="corpo-content"]/div[3]/div[2]/div/div[4]/div[63]/div')
    buttom_press_3.click()
    sleep(3)
except:
    pass

sleep(1)
url_list = []
a = navegador.page_source.encode('utf-8')
b = str(a)
c = b.split()


emptystr = ""
for i in c:

    if 'comunidade/clubes/' in i:
        k = re.findall(r'\d+', i)
        url_list.append(k)

flat_list = []
for sublist in url_list:
    for item in sublist:
        flat_list.append(item)

        


#creating each complete URL list
completeurl_list = []
for i in flat_list:
    variator = 'https://www.fpcanoagem.pt/comunidade/clubes/{}'.format(i)
    completeurl_list.append(variator)
    


#breaking big list into smaller chunks
lista1 = completeurl_list[0:14]
lista2 = completeurl_list[14:30]
lista3 = completeurl_list[30:44]
lista4 = completeurl_list[44:60]
lista5 = completeurl_list[60:]


#finding email funct

def finding_email(address):

    req = requests.get(address)
    soup = bs(req.content, 'html5lib', from_encoding='utf-8')


    lista_deinfos = []
    for a in soup.findAll('div'):
        a = a.text
        lista_deinfos.append(a)

    lista_unica= []
    for i in lista_deinfos:
        i = i.split()
        for b in i:
            if '@' in b:
                if b not in lista_unica:
                    lista_unica.append(b)
            
    return lista_unica[0]
            
#finding website function
def finding_website(address):
    
    req = requests.get(address)
    soup = bs(req.content, 'html5lib', from_encoding='utf-8')


    lista_deinfos = []
    for a in soup.findAll('div'):
        a = a.text
        lista_deinfos.append(a)

        lista_unica= []
    for i in lista_deinfos:
        i = i.split()
        for b in i:
            if 'www' in b:
                if b not in lista_unica:
                    lista_unica.append(b)
    return lista_unica[0]
            
#finding phone1 function

def finding_phone1(address):
    lista_telefonica = []
    req = requests.get(address)
    soup = bs(req.content, 'html5lib', from_encoding='utf-8')
    for a in soup.findAll('div'):
        a = a.text
        texto = a
        t = re.compile(r'\d{9}')
        check = t.findall(texto)
        
        for i in check:
            if i not in lista_telefonica:
                lista_telefonica.append(i)
    return lista_telefonica[0]

#finding phone2 function

def finding_phone2(address):
    lista_telefonica = []
    req = requests.get(address)
    soup = bs(req.content, 'html5lib', from_encoding='utf-8')
    for a in soup.findAll('div'):
        a = a.text
        texto = a
        t = re.compile(r'\d{9}')
        check = t.findall(texto)
        
        for i in check:
            if i not in lista_telefonica:
                lista_telefonica.append(i)
    return lista_telefonica[1]


#Acronym function
def finding_acronym(address):

    req = requests.get(address)
    soup = bs(req.content, 'html5lib', from_encoding='utf-8')

                
    a = soup.find('h1').text
    temp = []
    for i in a:
        if i.isupper() == True:
            temp.append(i)
        

    return temp[0] + temp[1] + temp[2]
#creating final function with dictionary
my_list = []

def finalresultfunct(lista_de_urls):
    result = []
    for each_url in lista_de_urls:
        final_request = requests.get(each_url)
        final_soup = bs(final_request.content, 'html5lib')

        the_dict = {}

        try:
            the_dict['Name'] = final_soup.find('h1').text
        except:
            the_dict['Name'] = ''


        try:        
            the_dict['Acronym'] = finding_acronym(each_url)
        except:
            the_dict['Acronym'] = ''
       
        try:
            the_dict['Email'] = finding_email(each_url)
        except:
            the_dict['Email'] = ''

        try:
            the_dict['Website'] = finding_website(each_url)
        except:
            the_dict['Website']= ''
        
        try:
            the_dict['Phone1'] = finding_phone1(each_url)
        except:
            the_dict['Phone1'] = ''
        try:
            the_dict['Phone2'] = finding_phone2(each_url)
        except:
            the_dict['Phone2'] = ''
        



        the_dict['Affiliated'] = 'Federação Portuguesa de Canoagem'
        the_dict['Recorded By'] = 'Eduardo Fernandes'
        the_dict['Recorded Date'] = '02/03/2022'

        result.append(the_dict)
        
    return result

my_list = finalresultfunct(lista5)

keys = my_list[0].keys()
with open('Canoagem Portuguesa5.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    fieldnames = keys
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(my_list)

    csvfile.close()