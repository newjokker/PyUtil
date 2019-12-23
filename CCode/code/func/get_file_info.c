#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


// 获得文本一共有多少行，返回每一行开始的位置
int get_file_line_num(char *file_name, int *line_start)
{
    int line_num = 0;  // 行数
    char buff[40000];
    FILE *fp;

	fp = fopen(file_name, "r");

	if(!(fp = fopen(file_name, "r")))
	{
	    printf("can not open file : %s", file_name);
	    exit(1);
	}

	while(!feof(fp))
	{
	    line_start[line_num] = ftell(fp);
        fgets(buff, 40000, (FILE*)fp);
        line_num ++;
	}
	fclose(fp);
	return line_num;
}

// 获取指定行，指定指定行的位置即可(可以支持较大的文件进行操作)
void get_file_line_from_assign_start(char *file_name, int start_seek, char *buffer)
{
    FILE *fp;

    if(!(fp = fopen(file_name, "r")))
    {
        printf("can not open this file");
    }

	rewind(fp); // 文件指针指向文件首
    fseek(fp, start_seek, SEEK_SET);  // 文件指针指向指定位置
    fgets(buffer, 40000, (FILE*)fp);  // 获取一行
	fclose(fp);
}