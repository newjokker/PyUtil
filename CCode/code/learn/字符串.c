#include <stdio.h>
#include <string.h>

/*
* <字符串>

字符串实际上是使用 null 字符 '\0' 终止的一维字符数组
* 两种初始化方法
     * char greeting[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
     * char greeting[] = "Hello";
     * 不需要把 null 字符放在字符串常量的末尾。C 编译器会在初始化数组时，自动把 '\0' 放在字符串的末尾。

* 字符串函数
    * strcpy(s1, s2);    复制字符串 s2 到字符串 s1。
    * strcat(s1, s2);    连接字符串 s2 到字符串 s1 的末尾。  // 无返回值的，直接改变 s1 而不是新生成一个 char[]
    * strlen(s1);        返回字符串 s1 的长度。
    * strcmp(s1, s2);    如果 s1 和 s2 是相同的，则返回 0；如果 s1<s2 则返回小于 0；如果 s1>s2 则返回大于 0。
    * strchr(s1, ch);    返回一个指针，指向字符串 s1 中字符 ch 的第一次出现的位置。
    * strstr(s1, s2);    返回一个指针，指向字符串 s1 中字符串 s2 的第一次出现的位置。
*/

int main(){
	
    char greeting[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
    printf("Greeting message: %s\n", greeting);

    char str1[12] = "Hello";
    char str2[12] = "World";
    char str3[12];
    int  len ;

    strcpy(str3, str1);  // 复制 str1 到 str3
    printf("strcpy( str3, str1) :  %s\n", str3 );

    strcat( str1, str2);  // 连接 str1 和 str2
    printf("strcat( str1, str2):    %s\n", str1 );

    len = strlen(str1);  // 连接后，str1 的总长度
    printf("strlen(str1) :  %d\n", len );

    char aa[] = "123456789";
    strcat(aa, "456");
    printf("length : %s\n", aa);
    printf("value %c", aa[5]);

    return 0;
}