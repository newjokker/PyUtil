#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include "..//head//szbf.h"

/*
* 打开文件中文乱码问题
    * 用记事本打开，另存为 ansi 格式即可

* 如何将读取的文件放到字符串数组里面
    * 现在采取的方法是，不将文件内容进行存储，只是每次打开文件读取一行，输出
    * 后面可以改进为不要一行行的遍历，直接根据文件指正对文件进行指定行读取
    * 因为文本文件并不是每一行占多少字节，所以还是要一行行读取文件，或者是先将文件存储到一个合适的数据结构中去

* 获取随机行
    * 获取随机行的时候一定要注意，初始化种子点不要写在循环里面
*/


int main()
{
	FILE *fp = NULL;
	char file_name[200],  buffer[4000];
//	int line_start[500000];  // 前面不加 static 关键字，是存在栈里面的，windows 系统限制只能用 1 M，这个地方要好好看看是为什么
	static int line_start[10000000];
	int random_index, interval_time, line_num;
	srand((unsigned)time(NULL));  // 这句话不能写在循环里面

	printf("file path : ");
	scanf("%s", file_name);  // 输入文件的路径
    //	strcpy(file_name, "C://Users//74722//Desktop//sunzibingfa//the_art_of_war.txt");  // 尝试将 txt 文件打包到 exe 里面这样就不要随时带着文件了
	printf("interval time (s) : ");
	scanf("%d", &interval_time);  // 输入打印一行的时间间隔
    line_num = get_file_line_num(file_name, line_start);  // 得到文本的行数
    printf("line num : %d\n", line_num);
    printf("sizeof line_start : %f M\n", ((float)(sizeof(line_start))/(1024*1024)));

    while(1)
    {
        random_index = get_random_value_less_then_assign_value(line_num);               // 返回一个小于一个值的随机数
        get_file_line_from_assign_start(file_name, line_start[random_index], buffer);   // 返回文本的指定行

        // 去掉空的一行
        if (memcmp(buffer, "\n", 1) != 0)
        {
            printf("-----------------------------------------------------------------------------------------\n");
            printf("%d : %s", random_index, buffer);  // 打印获取的指定行
        }
        else{
            continue;
        }

        Sleep(1000 * interval_time);
    }

    return 0;
}