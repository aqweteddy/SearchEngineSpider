import dns.resolver as resolver


class DNSCacheCountIp:
    def __init__(self):
        self.domain2ip = dict()
        self.ip_cnt = dict()
    
    def query_dns(self, domain: str):
        if domain not in self.domain2ip.keys():
            A = resolver.query(domain, 'A')
            ips = []
            for i in A.response.answer:
                for j in i.items:
                    ips.append(j.address)

            self.domain2ip[domain] = ips # list
            return ips
        else:
            return self.domain2ip[domain]

    def query_ip_cnt(self, ip: str):
        pass

if __name__ == '__main__':
    dns = DNSCacheCountIp()
    print(dns.query_dns('slido.com'))