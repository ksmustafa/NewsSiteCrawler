import time 
from crawler import Crawler

craw = Crawler()

start = time.time()
craw.get_news(6000, 6180)
end = time.time()

print(end-start)