#include <stdio.h>

/*
回调函数，通过函数指针来调用的函数，就是将函数使用函数指针的方式当做变量传给另外一个函数，就是写的有点复杂

*/


#include <stdlib.h>
#include <stdio.h>

// 获取随机值
int getNextRandomValue(void)
{
    return rand();
}

// 回调函数
void populate_array(int *array, size_t arraySize, int (*getValue)(void))  // void 可以省略，函数后面的括号不能省略
{
    for (size_t i=0; i<arraySize; i++)
        array[i] = getValue();
}

int main(void)
{
    int myarray[10];
    populate_array(myarray, 10, getNextRandomValue);
    for(int i = 0; i < 10; i++) {
        printf("%d ", myarray[i]);
    }
    printf("\n");
    return 0;
}