#include <io.h>
#include <stdio.h>
#include <string.h>
#include <time.h>


void printDir(char* path )
{
    struct _finddata_t data;  // 定义变量 data 为 _finddata_t 结构
    long hnd = _findfirst( path, &data );    // 查找文件名与正则表达式chRE的匹配第一个文件，handle 用于查找的句柄

    if ( hnd < 0 )
    {
        perror( path );  //
    }
    int  nRet = (hnd <0 ) ? -1 : 1;

    while ( nRet >= 0 )
    {
        if ( data.attrib == _A_SUBDIR )  // 如果是目录
        {
            printf("- name -> %s \n", data.name );
            printf("- time_create -> %s", ctime(&(data.time_create)));
            printf("- time_access -> %s", ctime(&(data.time_access)));
            printf("- time_write -> %s", ctime(&(data.time_write)));
            printf("---------------------------------------------\n");
        }
        else
        {
            printf("- name -> %s \n", data.name );
            printf("- size -> %f M \n", ((float)data.size)/(1024.0*1024.0) );
            printf("- time_create -> %s", ctime(&(data.time_create)));
            printf("- time_access -> %s", ctime(&(data.time_access)));
            printf("- time_write -> %s", ctime(&(data.time_write)));
            printf("---------------------------------------------\n");
            }

        nRet = _findnext( hnd, &data );  //
    }
    _findclose( hnd );     // 关闭当前句柄
}

void main()
{
    char file_path[100];
    while (1)
    {
        printf("dir path : ");
        scanf("%s", &file_path);
        printDir(strcat(file_path, "/*.*"));  // 文件路径正则表达式
//        printDir(file_path);  // 文件路径正则表达式
    }
}