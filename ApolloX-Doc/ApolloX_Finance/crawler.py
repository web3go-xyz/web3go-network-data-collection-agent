import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import re

_BASE_URL = 'https://apollox-finance.gitbook.io/'
_HOME_URL = _BASE_URL + 'apollox-finance/'
_FILE_BASE_PATH = '/Users/zhangqixin/web3go_workspace/web3go_github/web3go-network-data-collection-agent/ApolloX-Doc/ApolloX_Finance/result/'
__MEAU_CLASS = 'css-175oi2r r-1yzf0co r-1sc18lr'
__EXCLUDE_HREF = 'https://www.gitbook.com/'


def getHTML(url):
    print("==> "+url)
    cookieJar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookieJar))
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'), ('Cookie', '')]
    urllib.request.install_opener(opener)
    html_bytes = urllib.request.urlopen(url).read()
    return html_bytes.decode('utf-8')


def parse(soup):
    first_layer_soups = soup.find(
        'div', class_='css-175oi2r r-1yzf0co r-1sc18lr').find_all('a')
    new_first_layer_soups = [
        i for i in first_layer_soups]
    seq = 1
    for first_layer_soup in new_first_layer_soups:
        href = first_layer_soup.attrs['href']
        if href != '/' and not href.startswith(__EXCLUDE_HREF):
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
    if meau_soup is None:
        print("1111")
        return
    deeper_soups = meau_soup.find_all(
        href=re.compile('^' + href + '/.+'))
    for n in range(len(deeper_soups)):
        new_name_prefix = name_prefix + str(n+1) + '_'
        name = new_name_prefix + deeper_soups[n].get_text() + '.txt'
        new_href = deeper_soups[n].attrs['href']
        new_soup = BeautifulSoup(
            getHTML(_BASE_URL + new_href), 'html.parser')
        write_text_to_file(new_soup, name)
        deeper(new_name_prefix, new_href, new_soup)


def write_text_to_file(soup, file_name):
    text_soup = soup.find('div', attrs={'class': 'css-175oi2r r-13awgt0'})
    if text_soup is not None:
        try:
            open(_FILE_BASE_PATH + file_name.replace('/','_'), mode='w').write(text_soup.get_text('\r\n'))
        except Exception as error:
            print(error)


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
    html_doc = getHTML(_HOME_URL)
    soup = BeautifulSoup(html_doc, 'html.parser')
    parse(soup)
