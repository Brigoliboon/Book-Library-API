from selenium import webdriver
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Union
import datetime
import requests
import time
import json
#scrape content from requested network
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'
}
base_url = 'https://pdfdrive.com'

#the search query object will scrape the queried results from the source
def request_network(baseurl, params:dict|None = None):
    url = baseurl
    status = 200|int
    try:
        response = requests.get(url,params=params)
        status = response.status_code()
        if status == 200:
            return response.content
        return status
    except:
        return status
class File(BaseModel):
    name: Union[str, None]
    poster: Union[str, None]
    description: Union[str, None]
    link: Union[str, None]
    info: Union[str, None]
    download_link: Union[str, None]
class Query:
    def __init__(self, q:str, pagecount='', pubyear='', searchin='',em='') -> None:
        self.q = q
        self.pagecount = pagecount
        self.pubyear = pubyear
        self.searchin = searchin
        self.em = em
        
    def get_result(self):
        search_url = f'{base_url}/search'
        response = requests.get(search_url,headers=headers, params={'q': self.q, 'pagecount':self.pagecount, 'pubyear':self.pubyear, 'searchin':self.searchin, 'em':self.em})
        soup = BeautifulSoup(response.content, 'html.parser')
        files = self.extract_files(soup)
        return self.pass_data_to_json(files)
    @staticmethod
    def extract_files(soup: BeautifulSoup) -> list[dict]:
        files = []
        table = soup.find('div', attrs={'class': 'files-new'}).ul
        for item in table.findAll('li'):
            file_container_right = item.find('div', class_='file-right')
            file_container_left = item.find('div', class_='file-left')
            file_data = {
                'name': file_container_left.a.img['title'],
                'poster': file_container_left.a.img['src'],
                'description': '',
                'link': f"{base_url}{file_container_right.a['href']}",
                'info': Query.clean_data_info([span.text for span in file_container_right.div.findAll('span')]),
                'download_preview_link': Query._extract_download_link(file_container_right.a['href'])
            }
            files.append(file_data)
        return files
    @staticmethod
    def clean_data_info(data:list):
        while '·' in data:
            data.remove('·')
        return data
    @staticmethod
    def _extract_download_link(link:str)-> None:
        index=link.rfind('e')
        download_link = f'{link[:index]}d{link[index+1:]}'
        return download_link
    @staticmethod
    def pass_data_to_json(data:list)-> None:
        current_time = datetime.datetime.now()
        json_data = {'updated_time':current_time.isoformat(), 'results':data}
        return json.dumps(json_data)
#this will get the single file information when clicked or is chosen
class file_detail():
    def __init__(self, url) -> None:
        self.url = url
    def get_file_detail(self, file_path):
        file_url = f'{self.url}{file_path}'
        response = requests.get(file_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        detail_container = soup.find('div', attrs={'class':"ebook-main"})
        similar_ebook_container = soup.find('div', attrs={"id":"similar"}).div.ul
        return {}
    def download(download_link:str)-> None:
        driver = webdriver.Chrome()
        time.sleep(5)
        driver.get(download_link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        file = soup.find('div',attrs={'class':"btn-group"}).a['href']
        return f'{base_url}{file}'
    @staticmethod
    def process_file_detail(container)-> None:
        file = {}
        file['title'] = container.find('div', class_='ebook-title').text
        file['author'] = container.find('span', itemprop_="creator").text
        file['info'] = [info for info in container.findAll('div', attrs= {'class':"info-green"})]
        file['description'] = container.find('div', class_="quotes").text
        file['download-link'] = container.find('a', 'download-button-link')['href']
        return file
q = Query('nice')
print(q.get_result())