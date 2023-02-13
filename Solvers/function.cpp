#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <unordered_map>

using namespace std;
namespace N
{
    typedef std::tuple<ushort, ushort> key_t;

    struct key_hash : public std::unary_function<key_t, std::size_t>
    {
        std::size_t operator()(const key_t &k) const
        {
            return std::get<0>(k) ^ (359 + std::get<1>(k));
        }
    };

    struct key_equal : public std::binary_function<key_t, key_t, bool>
    {
        bool operator()(const key_t &v0, const key_t &v1) const
        {
            return (
                std::get<0>(v0) == std::get<0>(v1) &&
                std::get<1>(v0) == std::get<1>(v1));
        }
    };
    typedef std::unordered_map<const key_t, ushort, key_hash, key_equal> map_t;

    ushort binary_exponent(ushort x, ushort y, ushort mod)
    {
        ushort res = 1;
        ushort p = x;
        while (y)
        {
            if (y % 2)
            {
                res = (res * p) % mod;
            }
            p = (p * p) % mod;
            y /= 2;
        }
        return res;
    }

    ushort gp_sum(ushort a, int n, ushort mod)
    {
        ushort A = 1;
        int num = 0;
        ushort res = 0;
        ushort degree = 1;
        while (n)
        {
            if (n & (1 << num))
            {
                n &= (~(1 << num));
                res = (res + (A * binary_exponent(a, n, mod)) % mod) % mod;
            }
            A = (A + (A * binary_exponent(a, degree, mod)) % mod) % mod;
            degree *= 2;
            num++;
        }
        return res;
    }
    ushort recursive_formula(ushort a, ushort b, ushort u_0, ushort n)
    {
        // u_n=a^n u_0+\frac{a^n-1}{a-1}\,b\qquad(n\ge 1),
        // see : https://math.stackexchange.com/questions/3261910/what-is-the-general-formula-for-a-sequence-that-is-neither-arithmetic-nor-geomet/3261932#3261932
        return ((binary_exponent(a,n,32768)*u_0)%32768 + gp_sum(a,n,32768)*b)%32768;
    }
    ushort recursive(ushort a, ushort b, ushort h, map_t m)
    {
        key_t key = std::make_tuple(a, b);
        if (m.find(key) != m.end())
        {
            return m[key];
        }
        if (a == 0)
        {
            ushort result = (b + 1) % 32768;
            m.insert_or_assign(key, result);
            return result;
        }
        if (a == 1)
        {
            ushort result = (b + h + 1) % 32768;
            m.insert_or_assign(key, result);
            return result;
        }
        if (a == 2)
        {
            ushort result = ((h + 1) * b + 2 * h + 1) % 32768;
            m.insert_or_assign(key, result);
            return result;
        }
        if (a == 3)
        {
            ushort u_0 = ((h + 1) * h + 2 * h + 1) % 32768;
            // ushort call = b == 1 ? u_0 : recursive((ushort)3, (b - 1) % 32768, h, m);
            // ushort result = ((h + 1) * call + 2 * h + 1) % 32768;
            ushort result = b== 0 ? u_0 : recursive_formula(h+1, 2*h + 1,u_0,b);
            m.insert_or_assign(key, result);
            return result;
        }
        else
        {
            if (b == 0)
            {
                ushort result = recursive((a - 1) % 32768, h, h, m);
                m.insert_or_assign(key, result);
                return result;
            }
            else
            {
                ushort result = recursive((a - 1) % 32768, recursive(a, (b - 1) % 32768, h, m), h, m);
                m.insert_or_assign(key, result);
                return result;
            }
        }
    }


}
using namespace N;
int main()
{
    cout << "Hello World!" << endl;
    for (int h = 0; h <= 32768; h++)
    {
        map_t map;
        if (h % 1000 == 0)
            cout << "Starting with h =" << h << endl;
        if (6 == recursive(4, 1, h, map))
        {
            cout << h << endl;
            return 0;
        }
        map.clear();
    }
    cout << endl;
}