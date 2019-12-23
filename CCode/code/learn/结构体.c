#include <stdio.h>
#include <string.h>

/*
结构体

* 结构体使用 . 符号呼出需要的属性
* 结构体分 定义，初始化，使用

* 结构体
    struct tag {
        member-list
        member-list
        member-list
        ...
    } variable-list ;

    * tag 是结构体标签。
    * member-list 是标准的变量定义，比如 int i; 或者 float f，或者其他有效的变量定义。
    * variable-list 结构变量，定义在结构的末尾，最后一个分号之前，您可以指定一个或多个结构变量。

* 在一般情况下，tag、member-list、variable-list 这 3 部分至少要出现 2 个

* 成员访问
    * 结构体访问成员
        * . 符号
    * 结构体指针访问成员
        * -> 符号

*/

struct Books
{
   char  title[50];
   char  author[50];
   char  subject[100];
   int   book_id;
}Book1, Books[100];  // 结构变量的意义就在于不用在其他地方继续声明对应的结构体了，就是这个意义

void print_book(struct Books book)
{
    // 使用结构体进行访问
    printf( "Book title : %s\n", book.title);
    printf( "Book author : %s\n", book.author);
    printf( "Book subject : %s\n", book.subject);
    printf( "Book book_id : %d\n", book.book_id);
    printf("------------------------------\n");
    return;
}

void print_book_pointer(struct Books * book)
{
    // 使用结构体指针进行访问
    printf( "Book title : %s\n", book->title);  // -> “指向”的意思，常用于结构体指针变量访问成员。
    printf( "Book author : %s\n", book->author);
    printf( "Book subject : %s\n", book->subject);
    printf( "Book book_id : %d\n", book->book_id);
    printf("------------------------------\n");
    return;
}


int main( )
{

//   struct Books Book1;        /* 声明 Book1，类型为 Books */
//   struct Books Book2;        /* 声明 Book2，类型为 Books */

    // 赋值给结构体
    strcpy( Book1.title, "C Programming");
    strcpy( Book1.author, "Nuha Ali");
    strcpy( Book1.subject, "C Programming Tutorial");
    Book1.book_id = 6495407;

    // 赋值给结构体数组中的元素
    strcpy( Books[0].title, "Telecom Billing"); //Book2.title = "Telecom Billing";  // 是不能直接这样赋值的, 这个是为什么，因为字符串不能这么简单的进行赋值的？
    strcpy( Books[0].author, "Zara Ali");
    strcpy( Books[0].subject, "Telecom Billing Tutorial");
    Books[0].book_id = 111111;

    // 使用结构体指针访问元素
    print_book_pointer(&Books[0]);
    print_book_pointer(&Book1);
    // 使用结构体访问元素
    print_book(Books[0]);
    print_book(Book1);

   return 0;
}