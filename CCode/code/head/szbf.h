#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include "..//func//get_file_info.c"  // 使用相对路径载入模块
#include "..//func//random_info.c"

int get_file_line_num(char *file_name, int *line_start);
void get_file_line_from_assign_start(char *file_name, int start_seek, char *buffer);
int get_random_value_less_then_assign_value(int assign_line_num);