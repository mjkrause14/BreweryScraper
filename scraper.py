import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pymysql.cursors

connection = pymysql.connect(host='localhost', user='****', password='*****', db='brewerytour', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
brewery_list_url = "https://www.beeradvocate.com/place/city/2/?show=all"

response = requests.get(brewery_list_url)
html = response.content

soup = BeautifulSoup(html, "html.parser")
section = soup.find('div', id='ba-content')
breweries = section.find_next('ul')

try :
    for brewery in breweries.findAll('li'):
        breweryRef = brewery.find('a', href=True)
        breweryName = brewery.find('b')
        breweryAddr = brewery.find('span')
        with connection.cursor() as cursor:
            sql = "INSERT INTO `breweries` (`brewery_name`, `brewery_addr`) VALUES (%s, %s)"
            cursor.execute(sql, (breweryName.text.replace('&amp', ''), breweryAddr.text.replace(' - ', '')))
        
        with connection.cursor() as cursor:
            sql = "SELECT `brewery_id`, `brewery_addr` FROM `breweries` WHERE `brewery_name`=%s"
            cursor.execute(sql, (breweryName.text.replace('&amp', '')))
            result = cursor.fetchone()
            print(result)
finally:
    connection.close()

brewery_list = {}
for brewery in breweries.findAll('li'):
        breweryRef = brewery.find('a', href=True)
        breweryName = brewery.find('b')
        brewery_list.update({breweryName.text.replace('&amp', '') : "https://www.beeradvocate.com" + breweryRef['href']})


try:    
    for key, val in brewery_list.items():
        print(val)
        req = Request(val, None, {'User-Agent':'Mozilla/5.0'})
        brewery_url = urlopen(req).read()

        brew_soup = BeautifulSoup(brewery_url, "lxml")
        brew_section = brew_soup.findAll('div', id='ba-content')[0]
        brew_table = brew_section.find('table', attrs={'class': 'sortable'})
        beerInfo = []
        beerList = []
        beerDetail = []
        count = 0

        for row in brew_table.findAll('tr'):
            for cell in row.findAll('td')[0:3]:
                beerInfo.append(cell.text)
                count += 1
                if count == 3:
                    beerList.append(beerInfo)
                    count = 0
            beerInfo = []

        for li in beerList:
            for sub_li in li:
                beerDetail.append(sub_li.replace('?', '0.00'))
            with connection.cursor() as cursor:
                sql = "INSERT INTO `beers` (`brewery_name`, `beer_name`, `beer_type`, `abv`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (key, beerDetail[0], beerDetail[1], beerDetail[2]))
            
            connection.commit()
            beerDetail = []
finally:
    connection.close()