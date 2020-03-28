from typing import List
import aiohttp
import asyncio
import logging
import concurrent
from item import PageItem, ResponseItem
from pipelines import PipelineMainContent, PipelineToDB
from utils import UrlPool


class Spider:
    def __init__(self,
                 max_depth: int,
                 allow_domain: List[str],
                 pipelines: List,
                 max_thread: int = 10,
                 max_concurrent_request=100
                 ):
        self.pipelines = pipelines
        self.logger = logging.getLogger('[Spider]')

        self.url_que = UrlPool(max_depth)
        self.max_thread = max_thread
        self.max_concurrent_request= max_concurrent_request

        self.allow_domain = allow_domain
        self.cnt_request = 0

        for pipeline in self.pipelines:
            pipeline.open_spider()

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
            self.url_que.add(url, 0)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.fetch_all())
        loop.close()
        self.logger.warning(f'request_cnt: {self.cnt_request}')

        for pipeline in self.pipelines:
            pipeline.close()
    
    async def fetch_all(self):
        while len(self.url_que) != 0:
            self.logger.debug(f'url_pool_size: {len(self.url_que)}')
            tasks = []
            async with aiohttp.ClientSession() as session:
                urls = self.url_que.get_batch(self.max_concurrent_request)
                self.cnt_request += len(urls)
                for url,  depth in urls:
                    task = asyncio.create_task(
                        self.__fetch(url, depth, session))
                    tasks.append(task)
                results = await asyncio.gather(*tasks)
                
            with concurrent.futures.ProcessPoolExecutor(self.max_thread) as executor:
                futures = []
                for resp_item in results:
                    futures.append(executor.submit(Spider.pipelines_handler, resp_item, self.pipelines))
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        hrefs, depth = future.result()
                        for href in hrefs:
                            if self.allow_url(href):
                                self.url_que.add(href, depth+1)
                    except Exception:
                        pass
    
    def allow_url(self, href: str):
        fl = True
        for domain in self.allow_domain:
            if domain in href:
                fl = False
                break
        if fl:
            return False

        # fl = True
        # for f in ['.zip', '.whl']:
        #     if f in href:
        #         fl = False
        #         break
        # if fl:
        #     return False

        return True

    @staticmethod
    def pipelines_handler(resp_item, pipelines):
        if resp_item.drop:
            return False, False
        for pipeline in pipelines:
            resp_item = pipeline.in_resp_queue(resp_item)

        if resp_item.drop:
            return False, False
        page_item = resp_item.convert_to_page()

        for pipeline in pipelines:
            page_item = pipeline.in_page_queue(page_item)

        return page_item.a, page_item.depth_from_root


    async def __fetch(self, url: str, depth: int, session):
        """send aio request

        Arguments:
            url {str} -- a url

        Returns:
            item.ResponseItem()
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        item = ResponseItem()
        item.url = url
        item.depth_from_root = depth
        try:
            async with session.get(url, headers=headers, verify_ssl=False) as resp:
                item.html = await resp.text()
                item.resp_code = resp.status
        except Exception:
            item.drop = True
            self.logger.warning(f"url: {url} error happened.")

        return item


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    spider = Spider(pipelines=[
                    PipelineMainContent(), PipelineToDB()], allow_domain=['dcard.tw', 'ptt.cc'], max_depth=2, max_thread=10)
    spider.start_batch(
        ['https://www.ptt.cc/bbs/Baseball/index.html', 'https://www.dcard.tw/f'])
