from pymongo import MongoClient

class News:
    def __init__(self, _ID) -> None:
        self.ID = _ID
    
    def getID(self):
        return self.ID
    
    def setTitle(self, title):
        self.Title = title
        
    def getTitle(self):
        return self.Title
    
    def setLink(self, link):
        self.Link = link
        
    def getLink(self):
        return self.Link

    def setSummary(self, summary):
        self.Summary = summary
        
    def getSummary(self):
        return self.Summary
    
    def setDate(self, date):
        self.Date = date
        
    def getDate(self):
        return self.Date
    
    def setBody(self, body):
        self.Body = body
        
    def getBody(self):
        return self.Body
    
    def setCategory(self, category):
        self.Category = category
        
    def getCategory(self):
        return self.Category
    
    def to_string(self):
        print("ID:"+str(self.ID)+" Category:"+self.Category+"\n")
        print("Link:"+self.Link+"\n")
        print("Title: "+self.Title+"\n")
        print("Summary: "+self.Summary+"\n")
        print("Date: "+self.Date+"\n")
        print("Body: "+self.Body+"\n\n")
        
    def get_JSON(self):
        record = {
            "ID": self.ID,
            "Title": self.Title,
            "Link": self.Link,
            "Summary": self.Summary,
            "Category": self.Category,
            "Date": self.Date,
            "Body": self.Body
        }
        
        return record

class MongoDBConnector:
    
    def __init__(self) -> None:
        self.connection = MongoClient("mongodb://localhost:27017/")
        self.db = self.connection["TRNews"]
        self.sozcunews = self.db["SozcuNews"]
    
    def insert_news(self, record):
        x = self.sozcunews.insert_one(record)
