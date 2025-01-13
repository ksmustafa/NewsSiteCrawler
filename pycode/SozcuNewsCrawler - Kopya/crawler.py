import requests as r
from pyquery import PyQuery as pq

from data import News, MongoDBConnector

class Crawler:
    
    def __init__(self) -> None:
        self.base_url = "https://www.sozcu.com.tr/gundem-p"
        self.imagedefs_file = "./images/image_definitions.csv"

        self.headers = {
            'User-Agent' :
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/111.0.0.0 Safari/537.36'
        }
        self.home_url = 'https://www.sozcu.com.tr/'
        self.dbconnector = MongoDBConnector()
        
    def get_news(self, begin, end):
        
        current = begin
        step = 1
        
        for i in range(begin, end):
            
            try: 
                current_link = self.base_url + str(current)
                resp = r.get(url=current_link, timeout=5,
                             headers=self.headers)
                
                current_url = resp.url
                if current_url != self.home_url:
                    temp = News(current)
                    source = pq(resp.content)
                    image_link = source.find('div.main-image img').attr('src')
                    image_def = source.find('div.main-image img').attr('alt')
                    self.save_image(image_link, image_def, current)
                    
                    temp.setLink(current_url)
                    temp.Title = source.find('h1').text()
                    temp.Summary = source.find('p.description').text()
                    temp.Date = source.find('time').text().split(' ')[0]
                    temp.Body = source.find('div.article-body p').text()
                    
                    news_parts = current_url.rstrip('/').split('/')
                    if len(news_parts) > 1:
                        temp.Category = news_parts[-1]
                    else:
                        print(f"Invalid URL format: {current_url}")
                        continue
                    
                    record = temp.get_JSON()
                    self.dbconnector.insert_news(record=record)
                
                current = current + step
            
            except r.exceptions.ConnectionError:
                print("Connection error!")
            except r.exceptions.Timeout:
                print("Time Out!")
            
    def save_image(self, image_link, image_def, ID):
        if not image_link:
            print(f"No image found for ID: {ID}")
            return
        
        res_image = r.get(image_link, headers=self.headers)
        image_name = './images/' + str(ID) + ".jpg"

        with open(image_name, "wb") as f:
            f.write(res_image.content)
        
        with open(self.imagedefs_file, "a", encoding="utf-8") as im:
            im.write(str(ID) + "\t" + image_def + "\n")
