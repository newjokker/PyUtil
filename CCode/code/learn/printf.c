#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int main()
{
    int a = 23;
    printf("%12d\n", 23);  // 一共12个位置，多余的地方使用空格来表示
    printf("%p\n", &a);  // 打印变量的地址
    return 0;
}