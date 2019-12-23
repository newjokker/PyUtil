#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h>


/*
#if(0)
{
* fscanf, fprintf，从磁盘中按照格式读入或者输出字符
    * fprintf( 文件指针, 格式字符串, 输出表列 )
    * fscanf( 文件指针, 格式字符串, 输出表列 )

* 顺序读写和随机速写
    * fseek(文件指针，位移量，起始点) , 改变文件位置指针

* ftell(fp)，都得到文件流的当前位置，离文件开头的偏移量，错误的时候返回 -1
* ferror(fp), 返回 0 正确，非 0 出错
}
#endif
*/

int get_file_line_num(char *file_name, int *line_start)
{
    int line_num = 0;  // 行数
    char buff[4000];
    FILE *fp;

	fp = fopen(file_name, "r");
	while(!feof(fp))
	{
	    line_start[line_num] = ftell(fp);
        fgets(buff, 4000, (FILE*)fp);
        line_num ++;
	}
	fclose(fp);
	return line_num;
}

void get_file_line_from_assign_start(char *file_name, int start_seek)
{
    char buff[4000];
    FILE *fp;

    if(!(fp = fopen(file_name, "r")))
    {
        printf("can not open this file");
    }

	rewind(fp);
    fseek(fp, start_seek, SEEK_SET);
    fgets(buff, 4000, (FILE*)fp);
    printf("%s\n", buff);
	fclose(fp);
}

int main()
{
    char file_name[200];
    int line_start[100];
    int line_num;
    strcpy(file_name, "C://Users//74722//Desktop//the_art_of_war.txt");
    line_num = get_file_line_num(file_name, line_start);

    for(int i=0;i<line_num;i++)
    {
        printf("%d\n", line_start[i]);
        get_file_line_from_assign_start(file_name, line_start[i]);
    }


}



























