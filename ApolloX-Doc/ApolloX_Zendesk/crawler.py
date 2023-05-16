import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import re
import os

_BASE_URL = 'https://apollox.zendesk.com/hc/en-us'
_FILE_BASE_PATH = '/Users/zhangqixin/web3go_workspace/web3go_github/web3go-network-data-collection-agent/ApolloX-Doc/ApolloX_Zendesk/result/'
__MEAU_CLASS = 'css-175oi2r r-1yzf0co r-1sc18lr'


def getHTML(url):
    cookieJar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookieJar))
    opener.addheaders = [
    ('Authority', 'apollox.zendesk.com'),
    ('Method', 'GET'),
    ('Path', '/hc/en-us'),
    ('Scheme', 'https'),
    ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
    ('accept-encoding', 'gzip, deflate, br'),
    ('accept-language', 'zh-CN,zh;q=0.9'),
    ('cache-control', 'max-age=0'),
    ('cookie', '__cfruid=fa8dca6ab896fcb589f19f2421de873f80e77be5-1684222964; __cf_bm=rfk_02beXmG9CkubY1LFNsirN0pwUOZJ_jeeL9SiYsQ-1684239547-0-AUqEE1jJ4UoHRaAeMiu7NoIyWgE69hFYQot5PYCF3kavs+EK+N2gmA/R81vCQDZiykSWMlo/3RnchR1Hz//ZVy2zaWGIHGYDzqW5e322dugW; _help_center_session=SUtuRkQvb0psUk51THExbjZZZmwxQkJzSk5od0RYNW5oamVDRGNXYWFvM2MxNDYvd0dIdzB0M1ZULy9zdUdDOVN6b21XbVJPVE52UDVDL1M4eU9pOFZLaERFNWtremJrRlN2RXIvZnFMbTc2OG02Rk4zVzNVTmRxZzV6MzBuRmotLVVoTEE5UnR5VlBlLytzQjVEd0k1QWc9PQ%3D%3D--4dc2c2f088ffa55e213eafed887fe7d7d5f89c0d'),
    ('if-none-match', 'W/"db98ca9dd22cab3e21fe91a9e5a5999f"'),
    ('referer', 'https://apollox.zendesk.com/hc/zh-cn'),
    ('sec-ch-ua', '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"'),
    ('sec-ch-ua-mobile', '?0'),
    ('sec-ch-ua-platform', '"macOS"'),
    ('sec-fetch-dest', 'document'),
    ('sec-fetch-mode', 'navigate'),
    ('sec-fetch-site', 'same-origin'),
    ('sec-fetch-user', '?1'),
    ('upgrade-insecure-requests', '1'),
    ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36')]
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url)
    print("==> "+response.getcode())
    html_bytes = response.read()
    return html_bytes.decode('utf-8')


def download(url):
    filename = url.split('/')[-1]
    mk = _FILE_BASE_PATH
    dest_dir = os.path.join(mk, filename)
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, dest_dir)
    except Exception as e:
        print(e)
        print("is wrong ")


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
    open(_FILE_BASE_PATH + file_name,
         mode='w').write(text_soup.get_text('\r\n'))


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
    home_file = '/Users/zhangqixin/web3go_workspace/web3go_github/web3go-network-data-collection-agent/ApolloX-Doc/ApolloX_Zendesk/result/home.html'
    os.mknod(home_file)
    home = open(home_file, mode='w')
    home.write(html_doc)
    # soup = BeautifulSoup(html_doc, 'html.parser')
    # head_soups = parseHead(soup)
    # parseNext(head_soups, soup)
    # parseIndex(soup)
    # print(soup.title)
    # download(_BASE_URL)
