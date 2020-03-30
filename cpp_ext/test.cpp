#include "urlPool.h"
#include <bits/stdc++.h>

using namespace std;

int main()
{
    UrlPool pool(1000, 2000, 997, 2000, 4000, 1237, 2);
    pool.add("https://zhuanlan.zhihu.com/p/74219095", 1);
    pool.add("https://zhuanlan.zhihu.com/p/7421995", 1);
    pool.add("https://zhuanlan.zhihu.com/p/7219095", 1);
    pool.add("https://github.com/cython/cython/wik", 1);
    pool.add("https://github.com/cyton/cython/wik", 1);
    string url;
    int k;
    pool.get(&url, &k);
    cout << url << " " << k << endl;

    cout << pool.query_domain(pool.get_domain("https://github.com")) << endl;
    // for(auto r:result) cout << r << '\n';
    // cout << pool.query_domain("google.com") << endl;
    // cout << pool.get_domain("http://example.www.com") << endl;
}