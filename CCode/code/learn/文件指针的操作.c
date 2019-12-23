#include <stdio.h>
#include <wchar.h>
#include <locale.h>


/*

# 参考 : https://www.cnblogs.com/liang-chen/p/11397558.html

* rewind(文件指针)； 它的功能是把文件内部的位置指针移到文件首

* fseek函数用来移动文件内部位置指针，其调用形式为： fseek(文件指针，位移量，起始点)；
    * 文件首 　　　SEEK—SET　　　　0
    * 当前位置 　　SEEK—CUR　　　　1
    * 文件末尾 　　SEEK—END 　　　 2

*/



int main()
{
    printf("你好，世界");
    return 0;
}