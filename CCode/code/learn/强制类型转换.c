#include <stdio.h>

/*
C 强制类型转换

* 强制类型转换是把变量从一种类型转换为另一种数据类型。例如，如果您想存储一个 long 类型的值到一个简单的整型中，
    您需要把 long 类型强制转换为 int 类型。您可以使用强制类型转换运算符来把值显式地从一种类型转换为另一种类型，如下所示：
    (type_name) expression

* 整数提升是指把小于 int 或 unsigned int 的整数类型转换为 int 或 unsigned int 的过程。请看下面的实例，在 int 中添加一个字符

* 常用的算术转换是隐式地把值强制转换为相同的类型。编译器首先执行整数提升，如果操作数类型不同，则它们会被转换为下列层次中出现的最高层次的类型：
    int -> unsigned int -> long -> unsigned long -> long long -> unsigned long long -> float -> double -> long double

*/

int main()
{
   int sum = 17, count = 5;
   double mean;
   mean = (double) sum / count;
   printf("Value of mean : %f\n", mean );

   int  i = 17;
   char c = 'd';  // ascii 值是 99
   sum = i + c;
   printf("Value of sum : %d\n", sum );

}