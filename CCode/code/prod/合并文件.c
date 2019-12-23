#include <stdio.h>
#include <stdlib.h>

/*

* 使用方法
    * 准备一个 png 图片，一个 zip 文件
    * 执行 exe 分别输入 png 图片 zip 文件 和输出文件路径
    * 更改输出文件后缀为 .zip 打开即可获取压缩的文件

*/



int main()
{
    FILE *f_pic, *f_file, *f_res;
    char ch, pic_name[200], file_name[200], res_name[200];

    // 输入文件名
    printf("in file path :");
    scanf("%s", pic_name);
    printf("hide file path :");
    scanf("%s", file_name);
    printf("res path :");
    scanf("%s", res_name);

    // 打开需要读取的文件
    if( !(f_pic = fopen(pic_name, "rb")))
    {
        printf("can not open pic_name file");
    }
    // 打开需要写入的文件
    if( !(f_file = fopen(file_name, "rb")))
    {
        printf("can not open rar file");
    }
    // 打开需要进行合并的文件
    if( !(f_res = fopen(res_name, "wb")))
    {
        printf("can not open res file");
    }

    // 写图片文件
    while (! feof(f_pic))  // feof 判断文件是否已经到结尾
    {
        ch = fgetc(f_pic);
        fputc(ch, f_res);
    }
    // 写rar文件
    while (! feof(f_file))
    {
        ch = fgetc(f_file);
        fputc(ch, f_res);
    }

    // 关闭文件
    fclose(f_pic);
    fclose(f_file);
    fclose(f_res);

    system("pause");

    getchar();

    return 0;

}