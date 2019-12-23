#include <stdio.h>
#include <time.h>
#include <stdlib.h>

/*
const 关键字

* 参考 ：http://c.biancheng.net/view/2041.html

* 常量关键字

*/


int getNum(){
    return 100;
}

int main(){
    int n = 90;
    const int MaxNum1 = getNum();   //运行时初始化
    const int MaxNum2 = n;          //运行时初始化
    const int MaxNum3 = 80;         //编译时初始化
    printf("%d, %d, %d\n", MaxNum1, MaxNum2, MaxNum3);
    return 0;
}