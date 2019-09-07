# File Imports

# Library Imports
import re
import requests
import os
import csv
from bs4 import BeautifulSoup
from nltk import ngrams
from nltk import FreqDist

"""
NOTES:
I'm still working out some issues with the webscraping part. 
At the moment I have the webscraper for 2019 working correctly, i'm having some issues 
with the archive stuff since the formats for the URLs and the sites vary between years. 
I should have 2011-2018 working correctly soon. Earlier articles will take a lot more effort
since the URLs are more advanced and require specific dates as a part of them. I can work
on that if you find value for it, if not I can hold off on it. I'm taking the articles, and
running the through a function to get the ngrams. I'm currently generating unigrams through
sextagrams (not sure if that's the correct name, but it sounds right) and printing them.

ALGORITHM:
* Read in https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm HTML code
* Look for the table rows which contains links to all the articles written this year
* Append that to a list that will hold all Monthly URLs
* Extract article content by looking for P tags in the HTML
* Add content to a string
* Create NGrams with N looping from 1 - 6
* Print NGram

TODO:
* Rather than rely on URL to grab article, I want to write the article to a text file.
    * Doing so will make it a bit faster to read and create the n grams and we can
      specify which article we can look at.
* Fix the 2011-2018 webscraper portions
* Come up with better ngram output. Possibly writing each ngram to a file per URL
* Want to look at Ngram for all articles combined
    * Writing articles to text files will help with that
"""


# Archive Home
# https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm

# 2019 Home
# https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm

# URLs separated by URL pattern

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



def get_2019_beige_links(currentURL):
    """Gets links for 2019 Articles"""
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
    """Gets links for the archived years"""
    archiveURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm'
    yearlyLinks = []
    monthlyLinks = []
    try:
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
    except Exception as e:
        print("ERROR EXTRACTING YEAR URLS", e)

    for yearLink in yearlyLinks:
        try:
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
                        elif (re.match(r'.*2011', urlEnding) or
                                  re.match(r'.*2012', urlEnding) or
                                  re.match(r'.*2013', urlEnding) or
                                  re.match(r'.*2014', urlEnding) or
                                  re.match(r'.*2015', urlEnding) or
                                  re.match(r'.*2016', urlEnding)):
                            monthlyLinks.append('https://www.federalreserve.gov/monetarypolicy/beigebook/' + urlEnding)
                        else:
                            break
        except Exception as e:
            print("ERROR GRABBING ARCHIVE MONTHS URLS", e)


def get_ngrams(articleFile, date, n):
    """Takes in a file name and a number n to create a file with
        each ngram it produces"""
    year = date.group(0)[:4]
    month = date.group(0)[4:]

    # Check if ngram folder exists, if not make it
    path = f"Federal_Reserve/NGrams/{year}/"
    if not os.path.exists(path):
        os.makedirs(path)

    # Check if ngram file exists, if not write it
    fileName = f"{path}{year}_{month}_ngram_n={n}.csv"
    if not os.path.exists(fileName):
        with open(articleFile) as articlefile:
            article = articlefile.read()
        article = re.sub(r'([^\s\w]|_)+', '', article)
        ngramsResult = ngrams(article.split(), n)
        frequency = FreqDist(ngramsResult).most_common()

        articleNGrams = {}
        for ngram in frequency:
            words = ngram[0]
            freq = ngram[1]
            articleNGrams[words] = freq

        with open(fileName, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('NGram', 'Frequency'))
            for key, value in articleNGrams.items():
                writer.writerow([key, value])
        print('Created', fileName)



def get_article_info(url):
    date = re.search('\d\d\d\d\d\d', url)
    if date:
        year = date.group(0)[:4]
        month = date.group(0)[4:]

    # Check if Article folder exists, if not make it
    path = f"Federal_Reserve/Articles/{year}/"
    if not os.path.exists(path):
        os.makedirs(path)

    # Check if Article is already written if not, webscrape it and save it
    fileName = f"{path}{year}_{month}_Report.txt"
    if not os.path.exists(fileName):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        articleTag = soup.findAll('p')
        articleContent = ''
        for i in articleTag:
            articleContent += (i.get_text())

        file = open(fileName, "w+")
        file.write(articleContent)
        file.close()
        print("\nCreated", fileName)

        for i in range(1, 6):
            get_ngrams(fileName, date, i)


def get_monthly_links():
    monthURL = []
    links2019 = get_2019_beige_links(currentURL='https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm')
    for i in links2019:
        monthURL.append(i)

    # linksArchive = get_archive_beige_links()
    # for i in linksArchive:
    #     monthURL.append(i)

    for i in monthURL:
        get_article_info(i)

get_monthly_links()
