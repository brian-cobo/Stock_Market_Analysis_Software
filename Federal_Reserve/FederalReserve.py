# File Imports

# Library Imports
import re
from nltk.util import ngrams
from bs4 import BeautifulSoup
import requests

# Archive Home
# https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm

# 2019 Home
# https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm

# Reports

# Jan 16, 2019 https://www.federalreserve.gov/monetarypolicy/beigebook201901.htm
# Jan 17, 2018 https://www.federalreserve.gov/monetarypolicy/beigebook201801.htm
# Jan 18, 2017 https://www.federalreserve.gov/monetarypolicy/beigebook201701.htm

# Jan 13, 2016 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201601.htm
#              https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201601.htm?summary
# Jan 14, 2015 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201501.htm
# Jan 14, 2014 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201401.htm
# Jan 16, 2013 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201301.htm
# Jan   , 2012 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201201.htm
# Jan 12, 2011 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201101.htm

# Jan 13, 2010 https://www.federalreserve.gov/fomc/beigebook/2010/20100113/default.htm
# Jan 14, 2009 https://www.federalreserve.gov/fomc/beigebook/2009/20090114/FullReport.htm
#              https://www.federalreserve.gov/fomc/beigebook/2009/20090114/default.htm
# Jan 17, 2007 https://www.federalreserve.gov/fomc/beigebook/2007/20070117/FullReport.htm
# Jan 19, 2005 https://www.federalreserve.gov/fomc/beigebook/2005/20050119/FullReport.htm
#              https://www.federalreserve.gov/fomc/beigebook/2005/20050119/default.htm
# Jan 22, 1997 https://www.federalreserve.gov/fomc/beigebook/1997/19970122/default.htm

monthURL = []

def get_2019_beige_links(currentURL):
    currentLinks = []
    currentURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm'
    page = requests.get(currentURL)
    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.findAll('td')
    for i in links:
        if re.match('.*htm.*', str(i)):
            i = str(i)
            i = i.split('"')
            if 'htm' in i[1]:
                urlEnding = i[1].split('/')[-1]
                currentLinks.append('https://www.federalreserve.gov/monetarypolicy/'+ urlEnding)
    return currentLinks

def get_archive_beige_links():
    archiveURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm'
    yearlyLinks = []
    monthlyLinks = []
    page = requests.get(archiveURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.findAll(re.compile(r'a'))
    for i in links:
        if re.match('.*beigebook.*', str(i)):
            i = str(i)
            i = i.split('"')
            if 'htm' in i[1]:
                urlEnding = i[1].split('/')[-1]
                yearlyLinks.append('https://www.federalreserve.gov/monetarypolicy/' + urlEnding)
    for yearLink in yearlyLinks:
        print(yearlyLinks)
        page = requests.get(yearLink)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll('td')
        for i in links:
            if re.match('.*htm.*', str(i)) and \
                    'default' not in str(i):
                i = str(i)
                i = i.split('"')
                if 'htm' in i[1]:
                    urlEnding = i[1].split('/')[-1]
                    if (re.match(r'.*2018', urlEnding) or
                            re.match(r'.*2017', urlEnding)):
                        monthlyLinks.append('https://www.federalreserve.gov/monetarypolicy/' + urlEnding)
                    else:
                        monthlyLinks.append('https://www.federalreserve.gov/monetarypolicy/beigebook/' + urlEnding)



#links2019 = get_2019_beige_links(currentURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm')
linksArchive = get_archive_beige_links()

# for i in links2019:
#     monthURL.append(i)
