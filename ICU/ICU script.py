from bs4 import BeautifulSoup as bs
import requests
import csv
import re

complete_url = []
nations_id_list = []
urlfull_list = []
url = ''
sct_list = []
Continents = ['africa', 'americas', 'asia', 'europe', 'oceania']
for i in Continents:
    Variator = 'https://cheerunion.org/membership/nations/{}/'.format(i)
    sct_list.append(Variator)

for c in sct_list:
    url = c
    req = requests.get(url)
    soup = bs(req.content, 'html5lib')
    each_nation_url = soup.findAll(class_='nation')
    for each in each_nation_url:
        question_mark_position = str(each).find('?')
        closing_position = str(each).find('">')
        urlfull_list.append(str(each)[question_mark_position:closing_position])
        a = each.text
        nations_id_list.append(a)
        b = url + str(each)[question_mark_position:closing_position]
        if b not in complete_url:
            complete_url.append(b)


# name url dict
list_a = nations_id_list
list_b = complete_url

keys_list = list_b
values_list = list_a
zip_iterator = zip(keys_list, values_list)
a_dictionary = dict(zip_iterator)


# finding President function


def finding_president(e):

    e = e.text

    string_no_punctuation = re.sub("[^\w\s]", "", e)
    word_list = string_no_punctuation.split()

    finding_index = word_list.index('President')
    first_index = int(finding_index)
    second_index = first_index + 1
    third_index = second_index + 1

    result = word_list[first_index] + ' ' + \
        word_list[second_index] + ' ' + word_list[third_index]
    return result


# Finding Phone function


def PhoneNumber(i):
    y = i.text
    z = y.split()

    special = '+'
    for c in z:
        if special in c:
            return c


# Affiliation function

def Affiliation(a):

    question_mark_position = str(a).find('<strong>')
    closing_position = str(a).find('</strong>')
    b = (str(a)[question_mark_position:closing_position])
    c = b[8:]
    return c


# EmailFunction
def decodeEmail(e):
    decode = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        decode += chr(int(e[i:i+2], 16) ^ k)

    return decode

# AcronymFunction


def find_acronym(upper):
    acronym = ''

    if '(' in upper:
        acronym = upper[upper.find('(')+1:upper.find(')')]
    else:
        return ''

    return acronym


# NameAjustFunction
def Name_adjust(namein):

    if '(' in namein:

        a = namein[:namein.find('(')]
    else:
        return namein

    return a


# creating empty list
my_list = []


# function that inputs individual urls into the Beautifulsoup/request and creates the final dict.
def find_every_info(lista_de_urls):
    result = []
    for each_url in lista_de_urls:
        final_request = requests.get(each_url)
        second_soup = bs(final_request.content, 'html5lib')

        # creating new dictionaty
        my_dict = {}

        # if there's no email, it will jump this try
        try:
            my_dict['Email'] = decodeEmail(second_soup.find('div', class_='bio').find(
                'a')['href'].replace('/cdn-cgi/l/email-protection#', '')).strip()
        except:
            my_dict['Email'] = ''

        try:
            my_dict['Leadership'] = finding_president(
                second_soup.find('div', class_='bio')).strip()
        except:
            my_dict['Leadership'] = ''

        try:
            my_dict['Phone'] = PhoneNumber(
                second_soup.find('div', class_='bio')).strip()
        except:
            my_dict['Phone'] = ''

        try:

            my_dict['Name'] = Name_adjust(second_soup.find(
                'div', class_='bio').text.split('\n')[1].strip())

            if my_dict['Name'] == "		":

                my_dict['Name'] = second_soup.find(
                    'div', class_='bio').text.split('\n')[2].strip()
        except:
            my_dict['Name'] = ''

        try:
            my_dict['Acronym'] = find_acronym(second_soup.find(
                'div', class_='bio').text.split('\n')[1].strip())
        except:
            my_dict['Acronym'] = ''

        my_dict['Nation'] = a_dictionary[each_url]
        my_dict['Affiliated'] = "International Cheer Union"
        my_dict['Recorded By'] = 'Eduardo Fernandes'
        my_dict['Recorded Date'] = '03/02/2022'

        result.append(my_dict)

    return result


# put dicts into list
my_list = find_every_info(complete_url)

keys = my_list[0].keys()
with open('International Cheer Union Full6.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    fieldnames = keys
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(my_list)

    csvfile.close()
