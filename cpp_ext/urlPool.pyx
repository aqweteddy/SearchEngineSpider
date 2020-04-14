# distutils: language = c++

from urlPool cimport UrlPool

cdef class PyUrlPool:
    cdef UrlPool* url_pool

    def __cinit__(self, int max_depth, int url_r=1000, int url_c=1000, int url_p=1023, int dom_r=1000, int dom_c=1000, int dom_p=1023):
        self.url_pool = new UrlPool(max_depth, url_r, url_c, url_p, dom_r, url_c, url_p)
    
    # def __cinit__(self, int max_depth):
    #     self.url_pool = new UrlPool(max_depth, 1000, 1000, 19, 1000, 1000, 1023)
    
    def add(self, url, depth):
        cdef string c_url = str.encode(url)
        return self.url_pool.add(c_url, depth)
 
    def __len__(self):
        return self.url_pool.size()

    def pq_size(self):
        return self.url_pool.pq_size()

    def get(self):
        cdef string url
        cdef int depth
        self.url_pool.get(&url, &depth)
        return bytes.decode(url), depth
    
    def get_batch(self, k):
        result = []
        for i in range(k):
            tmp = self.get()
            if not tmp[0]:
                break
            result.append(tmp)
        return result
    
    def get_domain(self, url):
        cdef string c_url = str.encode(url)
        return bytes.decode(self.url_pool.get_domain(c_url))
    
    def query_url(self, url):
        cdef string c_url =  str.encode(url)
        return self.url_pool.query_url(c_url)
    
    def query_domain(self, dom):
        cdef string c_dom = str.encode(dom)
        return self.url_pool.query_domain(c_dom)
    
    def __dealloc__(self):
        del self.url_pool
