#include "myclasses.h"

MyClass::MyClass(int num)
{
    this->num = num;
}

void MyClass::set_num(int num)
{
    this->num = num;
}

int MyClass::get_num()
{
    return num;
}