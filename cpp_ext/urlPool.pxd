from libcpp.string cimport string

cdef extern from "urlPool.h":
    cdef cppclass UrlPool:
        UrlPool(int, int, int, int, int, int, int) except +
        int add(string, int)
        void get(string*, int*)
        int query_url(string)
        int query_domain(string)
        int size()
        int pq_size()
        string get_domain(string)
