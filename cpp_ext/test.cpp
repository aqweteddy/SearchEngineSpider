#include "urlPool.h"
#include <bits/stdc++.h>

using namespace std;

UrlPool run_add(int k, int pq_max_size)
{
    UrlPool pool(1000, 2000, 997, 2000, 4000, 1237, 2);
    for (int i = 0; i < k; ++i) {
        pool.add("https://github.com/cyton/cython/wik" + to_string(i), 1);
    }
    return pool;
}

void run_pop(int k, UrlPool pool)
{
    string s;
    int d;
    for (int i = 0; i < k; ++i) {
        pool.get(&s, &d);
    }
}

void run(int k_times, int pq_max_size)
{
    clock_t t1 = clock();
    UrlPool pool = run_add(k_times, pq_max_size);
    run_pop(k_times - 10, pool);
    cout << "pq_max_size: " << pq_max_size << " " << (clock() - t1) / 1000000.0 << "sec\n";
}

int main()
{
    // for(int i=40000; i< 100001; i+=10000) {
    //     run(1000000, i);
    // }
    run(100000, 70000);
}