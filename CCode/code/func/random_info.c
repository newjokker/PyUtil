#include <stdio.h>
#include <stdlib.h>


// 返回一个小于一个值的随机数
int get_random_value_less_then_assign_value(int assign_line_num)
{
    int random_num;
    random_num = rand() % assign_line_num;
    return random_num;
}
