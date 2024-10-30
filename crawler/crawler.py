#-*- coding: utf-8 -*-
import os
import sys
import formatter
import http.client #2.7's httplib
from urllib.parse import *
from urllib.request import *
import html.parser #2.7's htmllib
import io     #2.7's cStringIO

import bs4    #beautifulsoup4


class Retriever():
    __slots__ = ('url', 'file')
    
    def __init__(self, url):
        self.url, self.file = self.make_dir(url)

    def make_dir(self, url, default='index.html'):
        #Create usable local filename from URL
        parsed = urlparse(url)
        host = parsed.netloc.split('@')[-1].split(':')[0] #user:passwd@host:port/path
        filepath = '%s%s' % (host, parsed.path)
        if not os.path.splitext(parsed.path)[1]:
            filepath = os.path.join(filepath, default)
        linkdir = os.path.dirname(filepath)
        if not os.path.isdir(linkdir):
            if os.path.exists(linkdir):
                os.unlink(linkdir)
            os.makedirs(linkdir)
        return url, filepath

    def download(self):
        #Download URL to file(make_dir)
        try:
            #url에 한글 들어가 있을 경우를 위해 quote()로 처리
            fname = urlretrieve(quote(self.url, safe='/:'), self.file)
        except (IOError, http.client.InvalidURL) as e:
            fname = (('* ERROR: pad URL "%s": %s' % (self.url, e)), )
        return fname


    def bs_lxml(self):
        #한글 파일은 utf-8 지정해서 열어야한다
        f = open(self.file, 'r', encoding='utf-8') 
        markupdata = f.read()
        f.close()
        only_a_tags = bs4.SoupStrainer(('a', 'link'))
        soup = bs4.BeautifulSoup(markupdata, "lxml", parse_only=only_a_tags)
        #generator 형식으로 값(링크)만 반환
        return (urljoin(self.url, path.get('href')) for path in soup.find_all()) 

'''
bs4는 자체 parser가 아니라 원하는 parser를 입력하면
알아서 처리해주는 인터페이스에 가깝다.

bs4.BeautifulSoup(markupcode, "parser")
형태로 사용하며 parser로는 보통 다음 네가지를 사용한다.
html.parser : 내장 모듈이며 노멀한 성능이다
lxml : 매우 빠르다 보통 이걸 사용하는게 좋다
lxml-xml : xml을 파싱할 때는 이걸 사용한다 다른건 html파서다
html5lib : 웹브라우저가 페이지를 파싱하는 것과 동일한 방식을 사용한다 그러나 느리다
'''


class Crawler():
    __slots__ = ('count', 'q', 'seen', 'dom')

    def __init__(self, url):
        self.count = 0
        self.q = [url]    #list is used as queue
        self.seen = set()
        self.dom = self._get_domain(url)
        print("domain :", self.dom)

    def _get_domain(self, url):
        secure_toplevel_domain = ('com', 'edu', 'gov', 'info', 'net', 'org')
        parsed = urlparse(url)
        host = parsed.netloc.split('@')[-1].split(':')[0]
        if host.split('.')[-1] in secure_toplevel_domain:
            return '.'.join(host.split('.')[-2:])
        else:
            return '.'.join(host.split('.')[-3:])

    #main crawling routine
    def crawling(self, url, media=False):
        r = Retriever(url)
        fname = r.download()[0]
        if fname[0] == '*':
            print(fname, '...skipping parse')
            return
        self.count += 1
        print('\n(', self.count, ')')
        print('URL:', url)
        print('FILE:', fname)
        self.seen.add(url)
        ftype = os.path.splitext(fname)[1]
        if ftype not in ('.htm', '.html'):
            return

        for link in r.bs_lxml():
            if link.startswith('mailto:'):
                print('... discarded, mailto link')
                continue
            if not media:    #media is flag
                ftype = os.path.splitext(link)[1]
                if ftype in ('.mp3', '.mp4', '.m4v', '.wav'):
                    print('... discarded, media file')
                    continue
            if not link.startswith('http://'):
                link = urljoin(url, link)
            print('*', link)
            if link not in self.seen:
                if self.dom not in link:
                    print("... discarded, not in domain")
                else:
                    if link not in self.q:
                        self.q.append(link)
                        print("... new, added to Q")
                    else:
                        print("... discarded, already in Q")
            else:
                print("... discarded, already processed")

    def start(self, media=False):
        #Process next page in queue (if any)
        while self.q:
            url = self.q.pop()
            self.crawling(url, media)

'''
기존에 코딩하던 방식대로 코딩했으면 queue검사부터 안하고,
__init__에서 Crawler의 main격 함수를 호출하게 했을 것이다.
그럼 그냥 _main()에서 Crawler 인스턴스 생성과 동시에 
'''


def _main():
    #사용자 입력과 KeyboardInterrupt는 이런식으로 처리
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        try:
            url = "localhost:50000"
            #url = input('Enter starting URL: ')
        except (KeyboardInterrupt, EOFError):
            url = ''
    if not url:
        return
    if not url.startswith('http://') and not url.startswith('ftp://'):
        url = "http://%s/" % url
    
    robot = Crawler(url)
    robot.start()

if __name__ == '__main__':
    _main()


