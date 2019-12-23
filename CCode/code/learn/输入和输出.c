#include <stdio.h>


/*
* putchar() 输出一个字符
* getchar() 输入一个字符
* gets()    读取一行
* puts()    输出一行
* scanf()   输入
* printf()  输出
*/

int main(){
	
	int a,b,c,d;
	printf("input 3 number: \n");
	scanf("%d %d %d", &a, &b, &c);  // 输入的数据需要用空格分隔开来，程序才能识别，几个空格不重要，都能识别
	printf("the input number is : %d, %d, %d", a, b, c);
    return 0;
}