#include <io.h>
#include <stdio.h>
#include <string.h>
#include <time.h>


/*
    栈的特性：先进后出。
    栈在计算语言处理和将递归算法改为非递归算法等方面起着非常重要的作用。
*/

#define INITSIZE 100 //储存空间的初始分配量
typedef int ElemType;

typedef struct
{
    int top;           //栈顶指针
    ElemType *base;    //存放元素的动态数组空间
    int stacksize;     //当前栈空间的大小
}sqstack;

//初始化操作
//创建一个空栈，栈顶指针top初始化为0
void initstack(sqstack *S)
{
    s->base = (ElemType *)malloc(INITSIZE * sizeof(ElemType));    //申请存储空间
    s->top = 0;             //栈顶指针初始值为0
    s->stacksize = INITSIZE;       //容量为初始值
}

//求栈长操作
int getlen(sqstack *S)
{
    return (S->top);
}

//取栈顶元素操作
//将栈顶元素值存入e指向的内存单位，top值不变
int gettop(sqstack *S,ElemType *e)
{
    if(S->top==0) return 0;      //栈空，返回0
    *e = S->base[S->top-1];      //栈顶元素值存入指针e所指向的内存单元
    return 1;
}

//压栈操作
//将入栈元素x存入top所指的位置上，然后栈顶指针top增1
int push(sqstack *S,ElemType x)
{
    if(S->top == S->stacksize)  //若栈满，增加一个存储单元
    {
        S->base = (ElemType *)realloc(S->base,(S->stacksize+1)*sizeof(ElemType));
        if(!S->base) return 0;
        S->stacksize++;
    }
    S->base[S->top++] = x;
    return 1;
}

//弹栈操作
//先将栈顶指针top减1，再将top单元中的元素存入指针e所指向的内存单元
int pop(sqstack *S,ElemType *e)
{
    if(S->top==0)return 0;
    *e = S->base[--S->top];
    return 1;
}

//判栈S是否为空
int emptystack(sqstack *S)
{
    if(S->top==0) return 1;
    else return 0;
}

//输出栈操作
void list(sqstack *S)
{
    int i;
    for(i=S->top-1;i>=0;i--)
    {
        printf("%4d",S->base[i]);
    }
    printf("\n");
}