#include "myclasses.h"
#include <iostream>
using namespace std;

int main()
{
    MyClass obj(7);
    int x = obj.get_num();
    cout<< x << endl;
    obj.set_num(8);
    x = obj.get_num();
    cout<< x;
}