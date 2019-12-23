#include <stdio.h>
#include <stdlib.h>

/*
文件

* 文件指针

* 对下面常见的方法进行总结，各写一个例子

* fputs();  写数据
* fgets();  读取数据

* fgetc()  读取一个字符
* fputc()  打印一个字符

* (FILE*)fp  这里的 (FILE*) 是什么，干什么用的？ 目前猜测是用于文件类型的强转

*/

void print_file(char *file_path)
{
    // 读取文件并打印出来
    int i=0;
    FILE *fp;
    char buff[1000];  // 当 buffer 比较小的时候，读取较多的数据会报错，应该是分配的空间不够
    fp = fopen(file_path, "r");
    // 打印文件
    while ( !feof(fp))
    {
        fgets(buff, 255, fp);
        printf("%d: %s", i, buff );
        i++;
    }
    fclose(fp);
    return;
}

//// 将键盘的输入写到文件里面
//void write_scanf_to_file(char *file_path)
//{
//    char buffer[1000];
//    while true
//    {
//        printf("scanf file : ");
//        scanf("%s", &buffer);
//    }
//}


void main()
{
     char fileNameWrite[100],  fileNameRead[100];

     printf("scanf file path : ");
     scanf("%s", &fileNameRead);

     print_file(fileNameRead);
     //write_scanf_to_file(fileNameRead);

     system("pause");
     return;


}