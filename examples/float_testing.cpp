#include <iostream>

int main(int argc, char* argv[])
{
    // -infinity
    int64_t r = 11;
    int64_t p = 52;
    int64_t expo = (1 << (r+1)) - 1;  // 1111.1111.1
    int64_t expo_shifted = expo << p;
    int64_t mantissa = 0;
    int64_t int_repr = (expo_shifted|mantissa);
    double floating = *(double*) &int_repr;
    std::cout << floating << std::endl;
    // infinity
    expo = (1 << r) - 1;  // 1111.1111
    expo_shifted = expo << p;
    mantissa = 0;
    int_repr = (expo_shifted|mantissa);
    floating = *(double*) &int_repr;
    std::cout << floating << std::endl;
    // nan
    expo = (1 << (r+1)) - 1;  // 1111.1111.1
    expo_shifted = expo << p;
    mantissa = 1;
    int_repr = (expo_shifted|mantissa);
    floating = *(double*) &int_repr;
    std::cout << floating << std::endl;
    // nan
    expo = (1 << r) - 1;  // 1111.1111
    expo_shifted = expo << p;
    mantissa = 1;
    int_repr = (expo_shifted|mantissa);
    floating = *(double*) &int_repr;
    std::cout << floating << std::endl;
    return 0;
}

int main2(int argc, char* argv[])
{
    // -infinity
    int r = 8;
    int p = 23;
    int expo = (1 << (r+1)) - 1;  // 1111.1111.1
    int expo_shifted = expo << p;
    int mantissa = 0;
    int int_repr = (expo_shifted|mantissa);
    float floating = *(float*) &int_repr;
    std::cout << floating << std::endl;
    // infinity
    expo = (1 << r) - 1;  // 1111.1111
    expo_shifted = expo << p;
    mantissa = 0;
    int_repr = (expo_shifted|mantissa);
    floating = *(float*) &int_repr;
    std::cout << floating << std::endl;
    // nan
    expo = (1 << (r+1)) - 1;  // 1111.1111.1
    expo_shifted = expo << p;
    mantissa = 1;
    int_repr = (expo_shifted|mantissa);
    floating = *(float*) &int_repr;
    std::cout << floating << std::endl;
    // nan
    expo = (1 << r) - 1;  // 1111.1111
    expo_shifted = expo << p;
    mantissa = 1;
    int_repr = (expo_shifted|mantissa);
    floating = *(float*) &int_repr;
    std::cout << floating << std::endl;
    return 0;
}
