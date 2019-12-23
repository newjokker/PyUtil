#ifndef GETFILES_H
#define GETFILES_H
#include <iostream>  
#include <cstdlib>  
#include <cstdio>  
#include <string>  
#include <vector>
#include <algorithm>
#ifdef linux  
#include <unistd.h>  
#include <dirent.h> 
#include <string.h>
#endif 
#ifdef WIN32  
//#include <direct.h>  
#include <io.h>  
#endif  
#endif
using namespace std; 
class CGetFiles
{
	public:
	/************************************/
	// 函数名	: CGetFiles
	// 功能描述 : 构造函数
	// 返回值	: 
	/************************************/
	CGetFiles(void);
	/************************************/
	// 函数名	: ~CGetFiles
	// 功能描述 : 析构函数
	// 返回值	: 
	/************************************/
	~CGetFiles(void);
	/***************************************************/
	//   函数名   ：getfilesname
	//   功能描述 ：获取文件夹下所有文件名
	//   返回值   ：bool
	//   参数     ：string cate_dir 文件夹路径
	/****************************************************/

	bool getfilesname(string cate_dir,vector<string> &files);
};
