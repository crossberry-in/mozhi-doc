// helper.cpp — Example C++ file for run_cpp() demo
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

int main() {
    std::cout << "Hello from C++!" << std::endl;

    // Vector operations
    std::vector<int> numbers = {5, 3, 1, 4, 2};
    std::sort(numbers.begin(), numbers.end());

    std::cout << "Sorted: ";
    for (int n : numbers) {
        std::cout << n << " ";
    }
    std::cout << std::endl;

    // String manipulation
    std::string greeting = "Mozhi + C++ = ";
    greeting += "Awesome!";
    std::cout << greeting << std::endl;

    // Lambda
    auto square = [](int x) { return x * x; };
    std::cout << "square(7) = " << square(7) << std::endl;

    return 0;
}
