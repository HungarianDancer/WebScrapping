from bs4 import BeautifulSoup as bs
import requests
import csv
import re
import string


url = 'https://www1.ussailing.org/Utilities/ReportViewer.aspx?repPath=RegionalSailingAssociations&stb=f&spp=f;w=1000&h=500'
agent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
req = requests.get(url, headers=agent)
soup = bs(req.content, features="lxml")


realist = []
headers = []
c = []
for a in soup.findAll('tr'):
    for b in a.findAll('td'):
        c.append(b.text)


first_p = c.index("Manchester Sailing Association")
second_p = c.index("http://asdf")
realist = c[first_p - 1:second_p + 1]


my_list = []


def finaldelivery(listvar):
    result = []
    for i in range(0, len(realist)-5, 6):
        newdict = {}

        newdict['Area'] = listvar[i]
        newdict['Name'] = listvar[i+1]
        newdict['Acronym'] = listvar[i+2]
        newdict['City'] = listvar[i+3]
        newdict['State'] = listvar[i+4]
        newdict['Website'] = listvar[i+5]
        newdict['Affiliated'] = 'US Sailling'
        newdict['Recorded By'] = 'Eduardo Fernandes'
        newdict['Recorded Date'] = '14/02/2022'


        result.append(newdict)
    return result


my_list = finaldelivery(realist)

keys = my_list[0].keys()
with open('Ussailing.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    fieldnames = keys
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(my_list)

    csvfile.close()
