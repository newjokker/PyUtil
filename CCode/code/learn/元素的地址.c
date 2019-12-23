#include <stdio.h>

/*
数组

* 初始化数组的时候需要指定数组的大小，不能动态的定义，不能用变量规范数组的大小

*/

int main(){
	
    int i[] = {1,2,3,4,5};
    float j[] = {1.0, 2.0, 3.0};
    printf("add is  %p\n", &i[0]);
    printf("add is  %p\n", &i[1]);
    printf("add is  %p\n", &i[2]);
    printf("-----------------\n");
    printf("add is  %p\n", &j[0]);
    printf("add is  %p\n", &j[1]);
    printf("add is  %p\n", &j[2]);


    return 0;
}