#include <stdio.h>

/*
#define	    定义宏
#include	包含一个源代码文件
#undef	    取消已定义的宏
#ifdef	    如果宏已经定义，则返回真
#ifndef	    如果宏没有定义，则返回真
#if	        如果给定条件为真，则编译下面代码
#else	    #if 的替代方案
#elif	    如果前面的 #if 给定条件不为真，当前条件为真，则编译下面代码
#endif	    结束一个 #if……#else 条件编译块
#error	    当遇到标准错误时，输出错误消息
#pragma	    使用标准化方法，向编译器发布特殊的命令到编译器中


#define MAX_ARRAY_LENGTH 20
这个指令告诉 CPP 把所有的 MAX_ARRAY_LENGTH 替换为 20。使用 #define 定义常量来增强可读性。


*/


int main()
{

#if(0)
   printf("File :%s\n", __FILE__ );
   printf("Date :%s\n", __DATE__ );
   printf("Time :%s\n", __TIME__ );
   printf("Line :%d\n", __LINE__ );  // 代码所在行
   printf("ANSI :%d\n", __STDC__ );  // 当编译器以 ANSI 标准编译时，则定义为 1。
   return 0;
#endif

    printf("real start");

}