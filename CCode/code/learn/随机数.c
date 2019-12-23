#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>


// 返回一个小于一个值的随机数
int get_random_value_less_then_assign_value(int assign_line_num)
{
    int random_num;
    random_num = rand() % assign_line_num;
    return random_num;
}


int main(){
    int a;
    int rand_index;
    srand((unsigned)time(NULL));  // 这一行不能放在循环里面，只能进入程序的时候设置一下
    while (1)
    {
        rand_index = get_random_value_less_then_assign_value(125);
        printf("%d", rand_index);
        Sleep(100);
    }

    return 0;
}