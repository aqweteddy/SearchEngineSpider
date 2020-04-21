import asyncio
import time
import concurrent
import logging
from typing import List

import aiohttp

from item import PageItem, ResponseItem
from pipelines import PipelineToDB, PipelineMainContent
from utils.url_pool import UrlPool
# from cpp_ext.urlPool import PyUrlPool


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

        # self.url_que = PyUrlPool(max_depth)
        self.url_que = UrlPool(max_depth)
        self.max_thread = max_thread
        self.max_concurrent_request = max_concurrent_request

        self.allow_domain = allow_domain
        self.cnt_request = 0

        for pipeline in self.pipelines:
            pipeline.open_spider()

    def start_batch(self, urls: List[str]):
        """start spider

        Arguments:
            start_url {List[str]} -- urls
        """
        self.start_time = time.time()
        for url in urls:
            self.url_que.add(url, 0)

        self.request_handler()
        self.logger.warning(f'request_cnt: {self.cnt_request}')

        for pipeline in self.pipelines:
            pipeline.close()

    def request_handler(self):
        loop = asyncio.get_event_loop()

        # while self.url_que.pq_size() != 0:
        while len(self.url_que) != 0:
            results = loop.run_until_complete(self.fetch_all())
            with concurrent.futures.ProcessPoolExecutor(self.max_thread) as executor:
                futures = []
                for resp_item in results:
                    futures.append(executor.submit(
                        Spider.pipelines_handler, resp_item, self.pipelines))
                # print( f"[pipe time: {(time.time() - self.start_time):.2f} sec]")
                for future in concurrent.futures.as_completed(futures):
                    try:
                        page = future.result()
                        if not page:
                            continue
                        for href in page.a:
                            if self.allow_url(href):
                                self.url_que.add(href, page.depth_from_root+1)
                        for pipe in self.pipelines:
                            pipe.save(page)
                    except Exception as e:
                        self.logger.warning(f'[Pipelines]: {e}')


    async def fetch_all(self):
        # self.logger.debug(f'url_pool_size: {len(self.url_que)}')
        self.logger.info(f'[time: {time.time() - self.start_time:.2f} sec] queue_size: {len(self.url_que)} crawled_request: {self.cnt_request}')

        tasks = []
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            urls = self.url_que.get_batch(self.max_concurrent_request)
            self.cnt_request += len(urls)

            for url,  depth in urls:
                task = asyncio.create_task(
                    self.__fetch(url, depth, session))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
        return results

    def allow_url(self, href: str):
        if not self.allow_domain:
            return True
        fl = False
        for domain in self.allow_domain:
            if domain in href:
                fl = True
                break
        for file_type in ['.mpg', '.wmv', '.mov', '.jpg', '.avi', '.MPG', '.rmvb']:
            if file_type in domain:
                fl = False
        
        return fl

    @staticmethod
    def pipelines_handler(resp_item, pipelines):
        if resp_item.drop:
            return None
        for pipeline in pipelines:
            resp_item = pipeline.in_resp_queue(resp_item)

        if resp_item.drop:
            return None

        for pipeline in pipelines:
            tmp = pipeline.convert_resp_to_page(resp_item)
            if tmp:
                break

        page_item = tmp
        for pipeline in pipelines:
            page_item = pipeline.in_page_queue(page_item)

        return page_item

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
        except Exception as e:
            item.drop = True
            self.logger.warning(f"url: {url} Error:{e}")

        return item


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    spider = Spider(pipelines=[PipelineToDB(), PipelineMainContent()], 
                    allow_domain=None,
                    max_depth=5, 
                    max_thread=10)
    spider.start_batch(['https://www.dcard.tw/'])
