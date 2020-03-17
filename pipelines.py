from item import ResponseItem, PageItem


class PipelineBase:
    def __init__(self):
        print(type(self).__name__, end=', ')

    def open_spider(self):
        """
        run when open spider
        """
        pass

    def in_convert_queue(self, resp: ResponseItem):
        """call from convert_queue
        
        Arguments:
            resp {ResponseItem}
        return:
            {PageItem}
        """

    def in_resp_queue(self, data):
        """call from resp_queue
        
        Arguments:
            resp {ResponseItem}
        return:
            {ResponseItem}
        """
        pass

    def in_page_queue(self, data):
        """call from resp_queue
        
        Arguments:
            data {PageItem}
        return:
            {pageItem}
        """
        pass


class PipelineMainContent(PipelineBase):
    def in_resp_queue(self, resp: ResponseItem):
        print(resp.url)
        return resp


class PipelineToDB(PipelineBase):
    def in_page_queue(self, data: PageItem):
        print('DB')

        return data
