from urlPool import PyUrlPool

pool = PyUrlPool(100, 200, 3, 200, 300, 19, 10)
pool.add("https://zhuanlan.zhihu.com/p/74219095", 2)
pool.add("https://zhuanlan.zhihu.com/p/7421995", 2)
pool.add("https://zhuanlan.zhihu.com/p/7219095", 2)
pool.add("https://github.com/cython/cython/wik", 2)
pool.add("https://github.com/cyton/cython/wik", 2)

print(pool.get_batch(100))
domain = pool.get_domain('https://github.com')
print(pool.query_domain(domain))
print(len(pool))