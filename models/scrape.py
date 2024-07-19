from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import requests
import time
import json
#scrape content from requested network

#the search query object will scrape the queried results from the source
class search_query:
    url = 'https://pdfdrive.com'
    def __init__(self, q:str, pagecount='', pubyear='', searchin='',em='') -> None:
        self.q = q
        self.pagecount = pagecount
        self.pubyear = pubyear
        self.searchin = searchin
        self.em = em
    def get_search(self) -> json:
        search_url = f'{self.url}/search'
        response = requests.get(search_url,params={'q':self.q})
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('div',attrs={'class':'files-new'}).ul
        files = []
        for item in table.findAll('li'):
            details={}
            file_container_right = item.find('div', class_='file-right')
            file_container_left = item.find('div', class_='file-left')
            details['name'] = file_container_left.img['title']
            details['poster'] = file_container_left.img['src']
            details['description'] =''
            details['link'] = f"{self.url}{file_container_right.a['href']}"
            details['info'] = self.clean_data_info([span.text for span in file_container_right.div.findAll('span')])
            details['download_preview_link'] = self.extract_download_link(details['link'])
            files.append(details)
        return self.pass_data_to_json(files)
    @staticmethod
    def clean_data_info(data):
        while '·' in data:
            data.remove('·')
        return data
    @staticmethod
    def extract_download_link(link:str)-> None:
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
        return f'{search_query.url}{file}'
    @staticmethod
    def process_file_detail(container)-> None:
        file = {}
        file['title'] = container.find('div', class_='ebook-title').text
        file['author'] = container.find('span', itemprop_="creator").text
        file['info'] = [info for info in container.findAll('div', attrs= {'class':"info-green"})]
        file['description'] = container.find('div', class_="quotes").text
        file['download-link'] = container.find('a', 'download-button-link')['href']
        return file