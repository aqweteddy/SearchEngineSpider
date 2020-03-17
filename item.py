class PageItem:
    main_content: str = None
    url: str = None
    domain: str = None
    depth_from_root: int = None
    ip: str = None


class ResponseItem:
    resp_code: int = None
    html: str = None
    url: str = None
    depth_from_root: int = 0
    
    def convert_to_page(self):
        item = PageItem()
        item.main_content = self.html
        item.url = self.url
        item.depth_from_root = self.depth_from_root
    
    def __repr__(self):
        return f"""
                resp_code: {self.resp_code}
                url: {self.url}
                """

