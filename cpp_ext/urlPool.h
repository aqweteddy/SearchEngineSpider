#include "cms.h"
#include <queue>
#include <string>
#include <vector>
typedef std::pair<std::string, int> psi;

struct Url {
    std::string url, domain;
    int domain_cnt, depth;

    Url(const std::string& url, const std::string& domain, int domain_cnt, int depth)
    {
        this->domain_cnt = domain_cnt;
        this->url = url;
        this->domain = domain;
        this->depth = depth;
    }
};

struct Comparator {
    int operator()(const Url& p1, const Url& p2)
    {
        if (p1.domain_cnt == p2.domain_cnt)
            return p1.depth > p2.depth;
        return p1.domain_cnt > p2.domain_cnt;
    }
};

class UrlPool {
public:
    UrlPool(int max_depth, int url_r, int url_c, int url_p, int dom_r, int dom_c, int dom_p)
        : max_depth(max_depth)
        , url_pool(url_r, url_c, url_p)
        , domain_pool(dom_r, dom_c, dom_p)
    {
        pq_max_size = 70000;
    };

    int add(const std::string& url, int depth)
    {
        if (query_url(url) || depth > max_depth)
            return 0;

        ++cnt_url;
        if (pq.size() < pq_max_size) { // direct in url_pool
            std::string domain = get_domain(url);
            domain_pool.insert(domain);
            url_pool.insert(url);
            pq.push(Url(url, domain, query_domain(domain), depth));
        } else { // store in backup queue
            backup.push(psi(url, depth));
        }
        return 1;
    }

    int pq_size()
    {
        return pq.size();
    }

    int size()
    {
        return cnt_url;
    }

    void get(std::string* url, int* depth)
    {
        if (pq.size() == 0) {
            while (pq.size() != pq_max_size && backup.size() != 0) {
                psi tmp = backup.front();
                backup.pop();
                std::string domain = get_domain(tmp.first);
                pq.push(Url(tmp.first, domain, query_domain(domain), tmp.second));
            }
        }
        if (pq.size()) {
            (*url) = pq.top().url;
            (*depth) = pq.top().depth;
            pq.pop();
        } else {
            (*url) = "";
            (*depth) = 0;
        }
    }

    int query_url(const std::string& url)
    {
        return url_pool.query(url) > 0;
    }

    int query_domain(const std::string& url)
    {
        return domain_pool.query(url);
    }

    std::string get_domain(const std::string& url)
    {
        if (url.empty())
            return "";

        const std::string http = "http://";
        const std::string https = "https://";

        bool is_https = url.find(https) != string::npos ? true : false;
        std::string domain;

        if (url.find(http) != string::npos || url.find(https) != string::npos) {
            string::size_type start_pos = is_https ? https.size() : http.size();
            string::size_type end_pos = url.find("/", start_pos);
            if (end_pos != string::npos) {
                domain = url.substr(start_pos, end_pos - start_pos);
            } else {
                domain = url.substr(start_pos);
            }
        }

        return domain;
    }

private:
    int max_depth, cnt_url, pq_max_size;
    CmsHash<string> domain_pool, url_pool;
    std::priority_queue<Url, vector<Url>, Comparator> pq;
    std::queue<psi> backup;
};