from typing import List
import json

from item import PageItem, ResponseItem


# TODO: Drop Item
 
class PipelineBase:
    def __init__(self):
        """init"""
        # print(type(self).__name__, end=', ')

    def open_spider(self):
        """
        run when open spider
        """
        pass

    def in_resp_queue(self, data):
        """call from resp_queue
        
        Arguments:
            resp {ResponseItem}
        return:
            {ResponseItem}
        """
        return data

    def in_page_queue(self, data):
        """call from resp_queue
        
        Arguments:
            data {PageItem}
        return:
            {pageItem}
        """
        return data
    
    def close(self):
        pass


class PipelineMainContent(PipelineBase):
    def open_spider(self):
        self.data = []

    def in_resp_queue(self, resp: ResponseItem):
        self.data.append({'url':resp.url, 'html': resp.html})
        
        return resp
    
    def close(self):
        with open('test.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f)

class PipelineToDB(PipelineBase):
    def in_page_queue(self, data: PageItem):
        return data
