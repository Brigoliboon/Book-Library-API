from scrape import base_url, requests, BeautifulSoup as BS
default_category = 0
categories = []
class Category:
    url = f'{base_url}/category/'
    def __init__(self, type:str) -> None:
        self.type = type
    def default(self):
        response = Category(default_category)
        response.request_network()
    @staticmethod
    def request_network(url:str, type:str):
        r = requests.get(url + type)
        return {'status':r.status_code, 'body':r.content}
    @staticmethod
    def scrape_trending(body:str):
        pass