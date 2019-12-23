#include <stdio.h>


/*
C 头文件

* 头文件是扩展名为 .h 的文件，包含了 C 函数声明和宏定义，被多个源文件中引用共享。
    * 程序员编写的头文件  #include "file"
    * 编译器自带的头文件  #include <file>

* 如果一个头文件被引用两次，编译器会处理两次头文件的内容，这将产生错误。为了防止这种情况，标准的做法是把文件的整个内容放在条件编译语句中，如下：
    #ifndef HEADER_FILE
    #define HEADER_FILE
    the entire header file file
    #endif

*/


int main(){
	
	int a,b,c,d;
	printf("input 3 number: \n");
	scanf("%d %d %d", &a, &b, &c);  // 输入的数据需要用空格分隔开来，程序才能识别，几个空格不重要，都能识别
	printf("the input number is : %d, %d, %d", a, b, c);
    return 0;
}