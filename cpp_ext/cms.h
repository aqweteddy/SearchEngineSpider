#include <algorithm>
#include <functional>
#include <vector>


using std::string;
using std::hash;
using std::vector;

// template which the type name is T
template<class T>
class CmsHash
{
    // some shortcuts.
    typedef std::pair<int, int> pii;    // save data as a pair(a, b)
    const int INF = 0x3f3f3f3f;         // define infinity

    private:
    // private variables
    int row, col, prime;
    vector<int> a, b;           // 1D arrays a, b
    vector<vector<int> >map;    // 2D array map

    // private methods

    inline int myHash(const T& str, int count)
    {   // int myHash(the string to be hashed, the index of map[count][])
        // get hash number.
        hash<T> h;  // declare a hash calculator named h with type T.
        return (a[count] * h(str) + b[count]) % prime % col;
    }

    inline int randint(int a, int b) // get random int in [a, b]
    {
        // get random int in [a, b] 
        return (rand() + a) % (b+1);
    }

    public:
    CmsHash(){};
    CmsHash(int r, int c, int p)
    {
        // constructor
        // get row, column, prime to construct a object.

        // random seed
        srand(time(NULL));

        row = r, col = c, prime = p;
        // let map has r rows.
        map.resize(r);

        // O(row * column)
        for(int i=0; i<r; ++i){
            // let map[i] has c columns.
            map[i].resize(c);
            for(int j=0; j<c; ++j)
                // initial map[i][j] = 0
                map[i][j] = 0;
            // get random integers into a and b.
            a.push_back(randint(1, r));
            b.push_back(randint(1, r));
        }
    }

    void insert(const T& str)
    {
        // insert a T to CMSHash
        // O(row)

        // a vector store min <count, hashCode>
        vector<pii> mi; // count, hashCode

        for(int i=0; i<row; ++i){
            // first(i = 0) must push into mi.
            if(mi.empty()) 
                mi.push_back(pii(i, myHash(str, i)));
            else {
                int hash = myHash(str, i);
                // if equal, push into mi
                if(map[mi.back().first][mi.back().second] == map[i][hash])
                    mi.push_back(pii(i, hash));
                // if small than old, clear mi and push into mi.
                else if(map[mi.back().first][mi.back().second] > map[i][hash]){
                    mi.clear();
                    mi.push_back(pii(i, hash)); 
                }
            }
        }

        // ++ minimum
        for(const pii &p: mi){
            ++ map[p.first][p.second];
        }
    }

    int query(const T& str)
    {
        // query count of str.
        // O(row)

        int ans = INF;

        // get minimum.
        for(int i=0; i<row; ++i){
            int hash = myHash(str, i);
            ans = std::min(ans, map[i][hash]);
        }
        return ans;
    }
};