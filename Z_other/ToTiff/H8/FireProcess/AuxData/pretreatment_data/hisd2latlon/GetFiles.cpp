//#include "stdafx.h"
#include "GetFiles.h"
using namespace::std;
CGetFiles::CGetFiles(void)
{
	//构造函数
}
CGetFiles::~CGetFiles(void)
{
	//析构函数
}
bool CGetFiles::getfilesname(string cate_dir,vector<string> &files)
{
	#ifdef WIN32  
    //文件句柄  
  long   hFile   =   0;  
   //文件信息  
    struct _finddata_t fileinfo;  
    string p;  
   if((hFile = _findfirst(p.assign(cate_dir).append("\\*").c_str(),&fileinfo)) !=  -1)  
    {  
       do  
       {  
          //如果是目录,迭代之  
            //如果不是,加入列表  
            if((fileinfo.attrib &  _A_SUBDIR))  
            {  
               if(strcmp(fileinfo.name,".") != 0  &&  strcmp(fileinfo.name,"..") != 0)  
                    getfilesname( p.assign(cate_dir).append("\\").append(fileinfo.name), files );  
            }  
            else  
           {  
                files.push_back(p.assign(cate_dir).append(fileinfo.name) );  
           }  
       }while(_findnext(hFile, &fileinfo)  == 0);  
        _findclose(hFile);  
    }  

#endif  
//  
#ifdef linux  
    DIR *dir;  
    struct dirent *ptr;  
    char base[1000];  
   
    if ((dir=opendir(cate_dir.c_str())) == NULL)  
        {  
        perror("Open dir error...");  
                exit(1);  
        }  
   
    while ((ptr=readdir(dir)) != NULL)  
    {  
        if(strcmp(ptr->d_name,".")==0 || strcmp(ptr->d_name,"..")==0)    ///current dir OR parrent dir  
                continue;  
       else if(ptr->d_type == 8)    ///file  
            //printf("d_name:%s/%s\n",basePath,ptr->d_name); 
            files.push_back(ptr->d_name);  
       else if(ptr->d_type == 10)    ///link file  
            //printf("d_name:%s/%s\n",basePath,ptr->d_name);  
           continue;  
       else if(ptr->d_type == 4)    ///dir  
        {  
            files.push_back(ptr->d_name);  
            /* 
                memset(base,'\0',sizeof(base)); 
                strcpy(base,basePath); 
                strcat(base,"/"); 
                strcat(base,ptr->d_nSame); 
                readFileList(base); 
            */  
        }  
    }  
    closedir(dir);  
#endif  
  
    //排序，按从小到大排序  
   sort(files.begin(), files.end());  
   return false;  

}