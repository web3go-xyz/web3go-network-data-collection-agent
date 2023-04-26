import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import os
import re

_BASE_URL = 'https://docs.litentry.com'
_FILE_BASE_PATH = '/Users/zhangqixin/web3go_workspace/Litentry/crawler/'
__MEAU_CLASS = 'css-175oi2r r-1yzf0co r-1sc18lr'


def getHTML(url):
    cookieJar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookieJar))
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'), ('Cookie', '')]
    urllib.request.install_opener(opener)
    html_bytes = urllib.request.urlopen(url).read()
    return html_bytes.decode('utf-8')


def parseHead(soup):
    # 1. the text of About Litentry
    write_text_to_file(soup, '1_About_Litentry.txt')
    # 2. the text near About Litentry
    # crs = soup.find_all('div', attrs={'class': 'css-175oi2r r-1jkjb'})
    head_soups = soup.find('div', class_='css-175oi2r r-1yzf0co r-1sc18lr').find_all(
        href=re.compile('^/about\\-litentry.*'))
    for n in range(len(head_soups)):
        name = '1_' + str(n+1) + '_' + head_soups[n].get_text() + '.txt'
        # request for each item
        href = head_soups[n].attrs['href']
        cr_soup = BeautifulSoup(getHTML(_BASE_URL + href), 'html.parser')
        write_text_to_file(cr_soup, name)
    return head_soups


def parseNext(head_soups, soup):
    first_layer_soups = soup.find(
        'div', class_='css-175oi2r r-1yzf0co r-1sc18lr').find_all('a')
    new_first_layer_soups = [
        i for i in first_layer_soups if i not in head_soups]
    seq = 2
    for first_layer_soup in new_first_layer_soups:
        # name_f_prefix = str(n+2) + '_'
        # second_layer_soups = first_layer_soup.find_all('a')
        # for second_layer_soup in second_layer_soups:
        #     name_prefix = str(seq) + '_'
        #     seq += 1
        #     name = name_prefix + second_layer_soup.get_text() + '.txt'
        #     href = second_layer_soup.attrs['href']
        #     cr_soup = BeautifulSoup(getHTML(_BASE_URL + href), 'html.parser')
        #     write_text_to_file(cr_soup, name)
        #     # deeper
        #     deeper(name_prefix, href, cr_soup)
        href = first_layer_soup.attrs['href']
        if href != '/':
            name_prefix = str(seq) + '_'
            seq += 1
            name = name_prefix + first_layer_soup.get_text() + '.txt'
            cr_soup = BeautifulSoup(getHTML(_BASE_URL + href), 'html.parser')
            write_text_to_file(cr_soup, name)
            # deeper
            deeper(name_prefix, href, cr_soup)


def deeper(name_prefix, href, new_soup):
    meau_soup = new_soup.find(
        'div', class_='gitbook-root').find('div', class_=__MEAU_CLASS)
    deeper_soups = meau_soup.find_all(
        href=re.compile('^' + href + '/.+'))
    if deeper_soups:
        for n in range(len(deeper_soups)):
            new_name_prefix = name_prefix + str(n+1) + '_'
            name = new_name_prefix + deeper_soups[n].get_text() + '.txt'
            new_href = deeper_soups[n].attrs['href']
            new_soup = BeautifulSoup(getHTML(_BASE_URL + href), 'html.parser')
            write_text_to_file(new_soup, name)
            deeper(new_name_prefix, new_href, new_soup)


def write_text_to_file(soup, file_name):
    text_soup = soup.find('div', attrs={'class': 'css-175oi2r r-13awgt0'})
    open(_FILE_BASE_PATH + file_name,
         mode='w').write(text_soup.get_text())


def parseIndex(index_soup):
    layer = ["css-175oi2r r-1r5su4o", "", ""]
    aaa = index_soup.find_all(
        name='div', attrs={"class": "css-175oi2r r-1jkjb"})
    file = open(
        _FILE_BASE_PATH + '/urls.txt', mode="w")
    for aa in aaa:
        print("==>"+aa.a.attrs['href'])
        file.write(aa.a.attrs['href'])


if __name__ == '__main__':
    html_doc = getHTML(_BASE_URL)
    # 先把首页html采集下来
    # os.mknod('/Users/zhangqixin/web3go_workspace/Litentry/crawler/home.html')
    # home = open(
    #     '/Users/zhangqixin/web3go_workspace/Litentry/crawler/home.html', mode='w')
    # home.write(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    head_soups = parseHead(soup)
    parseNext(head_soups, soup)
    # parseIndex(soup)
    # print(soup.title)
