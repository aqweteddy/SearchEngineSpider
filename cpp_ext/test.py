from urlPool import PyUrlPool
import random
T = 1000000
pool = PyUrlPool(5, 1000, 2000, 997)
print(len(pool))

for i in range(T):
    # print(T)
    pool.add(f"https://zhuanlan.zhihu.com/p/74219095{i}", 2)
print(len(pool.get_batch(T-10)))
print(len(pool))
print(pool.pq_size())
# print(len(pool.get_batch(T)))