#include <stdio.h>
#include <time.h>
#include <stdlib.h>

void get_rand_array(int a[][5])  // 数组中的定义，不能忽略第二维的大小，为什么？
{
	for (int i=0;i<5;i++)
	{
		for (int j=0;j<5;j++)
		{
			a[i][j] = i+j;
		}
	}	
}

void print_array(int a[][5], int x, int y)
{	
	for (int i=0;i<x;i++)
	{
		printf("\n");
		for (int j=0;j<y;j++)
		{
			if (a[i][j] == 0)
			{
				printf("- ");
			}
			else
			{
				printf("%d ", a[i][j]);
			}
		}
	}
}

int main()
{
	int a[5][5];
	get_rand_array(a);
	print_array(a, 5, 5);
}