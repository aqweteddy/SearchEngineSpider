from typing import List
import aiohttp
import asyncio

from item import PageItem, ResponseItem
from pipelines import PipelineMainContent, PipelineToDB

class Spider:
    def __init__(self,
                 max_depth: int,
                 allow_domain: List[str],
                 pipelines: List
                 ):
        self.pipelines = pipelines
        self.resp_que = asyncio.Queue()
        self.page_que = asyncio.Queue()
        self.url_que = asyncio.Queue()

    def start_batch(self, urls: List[str]):
        """start spider

        Arguments:
            start_url {List[str]} -- urls
        """
        # TODO crawl html
        # analyze ip, domain
        # get url(<a>) and push them into wait_queue
        # get main main_content
        # generate a PageItem
        for url in urls:
            self.url_que.put_nowait(url)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__request_handler())
        loop.run_until_complete(self.__pipeline_page_handler())
        loop.run_until_complete(self.__pipeline_resp_handler())
        loop.close()
    
    async def __pipeline_resp_handler(self):
        while not self.resp_que.empty():
            resp_item = await self.resp_que.get()
            for pipeline in self.pipelines:
                resp_item = pipeline.in_resp_queue(resp_item)
    
    async def __pipeline_page_handler(self):
        while not self.page_que.empty():
            page_item = await self.page_que.get()
            for pipeline in self.pipelines:
                page_item = pipeline.in_page_queue(page_item)

    async def __request_handler(self): 
        while not self.url_que.empty():
            url = await self.url_que.get()
            resp_item = await self.__request(url)
            self.resp_que.put_nowait(resp_item)
    


    async def __request(self, url: str):
        """send aio request

        Arguments:
            url {str} -- a url

        Returns:
            item.ResponseItem()
        """
        item = ResponseItem()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                item.resp_code = response.status
                item.html = await response.read()
                item.url = url
                return item


if __name__ == '__main__':
    spider = Spider(1, ['ptt.cc'], pipelines=[PipelineMainContent(), PipelineToDB()])
    spider.start_batch(['https://zhuanlan.zhihu.com/p/36936574', 'https://24h.pchome.com.tw/prod/DHAI6Q-A900A8QO9?fq=/S/DHAU6H'])
    # print(spider.resp_que)