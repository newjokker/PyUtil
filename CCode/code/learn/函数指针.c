#include <stdio.h>

int max(int x, int y)
{
	return x > y? x:y;
}


int main(){
	
	int a,b,c,d;
	int (*p)(int, int) = &max; // 取地址符可以省略，但是 (*p) 的括号不能去掉
	
	printf("scanf three number : \n");
	scanf("%d %d %d", &a, &b, &c);
	//d = max(a,max(b,c));
	d = p(p(a,b),c);
	printf("the max number is : %d", d);
	
    return 0;
}