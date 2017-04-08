
import bs4

soup = bs4.BeautifulSoup('<div id="paging">' \
                '<a href="/category/System/LINUX%20%26%20UNIX?page=1" class="prev ">PREV</a>'\
				'<a class="numbox" href="/category/System/LINUX%20%26%20UNIX?page=1"><span>1</span></a><a class="numbox"><span class="selected">2</span></a>'\
				'<a class="next no-more-next">NEXT</a>'\
			    '</div>', "lxml")

soup2 = bs4.BeautifulSoup('<div id="paging">'\
				'<a class="prev no-more-prev"></a>'\
				'<a class="numbox"><span class="selected">1</span></a><a class="numbox" href="/category/System/LINUX%20%26%20UNIX?page=2"><span>2</span></a>'\
				'<a href="/category/System/LINUX%20%26%20UNIX?page=2" class="next ">NEXT</a>'\
			    '</div>', "lxml")
print(soup2.find('a', class_="prev").contents)
print(soup.find('a', class_="next").get('href'))

print(soup2.find('a', class_="next").get('href'))