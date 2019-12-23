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
	// ������	: CGetFiles
	// �������� : ���캯��
	// ����ֵ	: 
	/************************************/
	CGetFiles(void);
	/************************************/
	// ������	: ~CGetFiles
	// �������� : ��������
	// ����ֵ	: 
	/************************************/
	~CGetFiles(void);
	/***************************************************/
	//   ������   ��getfilesname
	//   �������� ����ȡ�ļ����������ļ���
	//   ����ֵ   ��bool
	//   ����     ��string cate_dir �ļ���·��
	/****************************************************/

	bool getfilesname(string cate_dir,vector<string> &files);
};
