/* ----------------------------------------------------------------------------
	Sample source code for Himawari Satandard Data

	Copyright (C) 2015 MSC (Meteorological Satellite Center) of JMA

	Disclaimer:
		MSC does not guarantee regarding the correctness, accuracy, reliability,
		or any other aspect regarding use of these sample codes.

	Detail of Himawari Standard Format:
		For data structure of Himawari Standard Format, prelese refer to MSC
		Website and Himawari Standard Data User's Guide.

		MSC Website
		http://www.jma-net.go.jp/msc/en/

		Himawari Standard Data User's Guide
		http://www.data.jma.go.jp/mscweb/en/himawari89/space_segment/hsd_sample/HS_D_users_guide_en.pdf

	History
		March,   2015  First release
        June,    2015  Version 2015-06
                       Fixed bug in getData() (3-4 get count value)
                       Fixed bug in function function hisd_read_header() (hisd_read.c)
                       Fixed bug in fucntion lonlat_to_pixlin() (hisd_pixlin2lonlat.c)
                       ((8) check the reverse side of the Earth)
---------------------------------------------------------------------------- */
# include <stdio.h>
# include <string.h>
# include <stdlib.h>
# include <time.h>
# include <math.h>
#include <vector>
# include "hisd.h"
//#include "omp.h"
# include "date_utl.h"
#include "GetFiles.h"
# define  MAXFILE   10
# define  INVALID   -1
#include<iostream>
# define  WIDTH     5501	/* default pixel number */
# define  HEIGHT    2001	/* default line number */
# define  LTLON     90.0	/* default left top longitude */
# define  LTLAT     10.0	/* default left top latitude */
# define  DLON      0.01	/* default Spatial resolution (longitude) */
# define  DLAT      0.01	/* default Spatial resolution (latitude) */
# define NORMAL_END 0
# define  ERROR_ARG         1
# define  ERROR_FILE_OPEN   2
# define  ERROR_CALLOCATE   3
# define  ERROR_READ_HEADER 4
# define  ERROR_INFO        5
# define  ERROR_READ_DATA   6
# define  ERROR_PARAMETER   7
# define  ERROR_MAKE_HEADER 8
# define  ERROR_MAKE_DATA   9
# define  ERROR_WRITE       10
using namespace std;
typedef struct{
	char	*InFile[MAXFILE+1];
 	char	*OutFile;
	int	filenum;
}argument;

typedef struct{
	float	*lon;
	float	*lat;
	float	*phys;
	double	startTime;
	double	endTime;
	char	satName[32];
}outdata;

typedef struct{
	short	width;		/* -width    pixel number */
	short	height;		/* -height   line number  */
	double	ltlon;		/* -lon      left top longitude */
	double	ltlat;		/* -lat      left top latitude  */
	double	dlon;		/* -dlon     Spatial resolution (longitude) */
	double	dlat;		/* -dlat     Spatial resolution (latitude) */
	short	band;
}parameter;

typedef struct{
	int		ncid;
	int		latVarId;
	int		lonVarId;
	int		physVarId;
	int		startTimeVarId;
	int		endTimeVarId;
}ncparam;


/* ---------------------------------------------------------------------------
  getArg()
 -----------------------------------------------------------------------------*/
int getArg(int argc, char **argv, argument *arg,parameter *param){
	
	int		ii,nn=0;
  if( argc!=9){
	  cout<<"Incoming parameter errors !"<<endl;
	  return(ERROR_ARG);	  
  }
	  string  inputpath(argv[1]);
	  string  outpath(argv[2]);
	  if (access(inputpath.c_str() , 0)!=0 )
	{
		cout<<"inputFilepath  Not Exist !!!"<<endl;
		 return(ERROR_ARG);	  
	}
	 if (access(outpath.c_str() , 0)!=0 )
	{
		cout<<"outputFilepath  Not Exist !!!"<<endl;
		 return(ERROR_ARG);	  
	}
	arg->OutFile = new char[1000];
	CGetFiles  getfiles;
	string outfilename("H8.out");
	string OutFile=outpath+outfilename;
	strcpy(arg->OutFile,OutFile.c_str());
	cout<<OutFile<<endl;
	for(ii=0;ii<MAXFILE;ii++){
		arg->InFile[ii] = new char[1000];
	} 
	  vector<string> files;
	  
	  getfiles.getfilesname(inputpath,files);
	  if(files.size()==0)
	  {
		 cout<<"Folder no files !"<<endl;
		 return(NORMAL_END);	   
	  }  
	   // cout<<files.size()<<endl;
	  for(int filesi=0;filesi<(int)files.size();filesi++)
	{   
	     string  tmpfile= files[filesi];
		  //cout<<tmpfile<<endl;
		int tmpfilelength = tmpfile.size();
		string datasuffix(tmpfile,tmpfilelength-3,3);
		if(datasuffix=="DAT")
		{
		
		//	string InFile=inputpath+tmpfile;
			//cout<<InFile<<endl;
		  strcpy(arg->InFile[nn],tmpfile.c_str());
		 
		//arg->InFile[nn]=InFile.c_str();
		nn++;
		}
	}
	    if(nn==0)
	  {
		 cout<<"Folder does not satisfy the required file !"<<endl; 
		 return(ERROR_ARG);	   
	  } 
	 // cout<<arg->InFile[9]<<endl;
	   arg->filenum=nn;
	   param->ltlat=atof(argv[3]);
	   param->ltlon=atof(argv[4]);
	   param->width = atoi(argv[5]);
	   param->height = atoi(argv[6]);
	   param->dlon = atof(argv[7]);
	   param->dlat = atof(argv[8]);
	   
	/* 4 check parameter */
	if(param->width < 10){param->width =10;}
	if(param->height< 10){param->height=10;}
	if(param->ltlat < -90.  || 90.< param->ltlat){ param->ltlat = LTLAT;}
	if(param->ltlon <-180.  ||180.< param->ltlon){ param->ltlon = LTLON;}
	if(param->dlat  < 0. || 10. < param->dlat ){param->dlat = DLAT;}
	if(param->dlon  < 0. || 10. < param->dlon ){param->dlon = DLON;}
	//cout<<param->dlat<<endl;
	//cout<<param->dlon<<endl;
	//cout<<param->dlon<<endl;
	//cout<<arg->InFile[9]<<endl;
	return(NORMAL_END);
}

/* ---------------------------------------------------------------------------
  getData()
 -----------------------------------------------------------------------------*/
int getData(argument *arg,parameter *param,outdata *data){

	HisdHeader		**header;
	FILE			**fp;
	float			*Pix,*Lin;
	unsigned short	*startLine;
	unsigned short	*endLine;
	unsigned int	ii,jj,kk,ll;
	int				n;
	unsigned short	count;
	float			radiance;
	unsigned long	n_size = param->height * param->width;
	double			phys;
	float 			minLine = 99999.0;
	float			maxLine =-99999.0;

	/* 1 allocate */
	if(	NULL == ( header = (HisdHeader **)calloc(arg->filenum,sizeof(HisdHeader *))) ||
		NULL == ( fp = (FILE **)calloc(arg->filenum,sizeof(FILE *))) || 
		NULL == ( startLine = (unsigned short *)calloc(arg->filenum,sizeof(unsigned short *))) ||
		NULL == ( endLine   = (unsigned short *)calloc(arg->filenum,sizeof(unsigned short *))) ||
		NULL == ( Pix = (float *)calloc(n_size,sizeof(float *))) ||
		NULL == ( Lin = (float *)calloc(n_size,sizeof(float *)))
	){
		fprintf(stderr,"callocate error\n");
		return(ERROR_CALLOCATE);
	}
	n = -1;
	for(ii=0;ii<arg->filenum;ii++){
		/* 2-1 open file */
		if(NULL == ( fp[ii] = fopen(arg->InFile[ii],"rb"))){
			fprintf(stderr,"error : can not open [%s]\n",arg->InFile[ii]);
			continue;
		}
		/* 2-2 callocate */
		if(NULL == (header[ii] = (HisdHeader *)calloc(1,sizeof(HisdHeader)))){
			fprintf(stderr,"callocate error\n");
			return(ERROR_CALLOCATE);
		}
		/* 2-3 read hisd header */
		if(NORMAL_END != hisd_read_header(header[ii],fp[ii])){
			fprintf(stderr,"error : read header [%s]\n",arg->InFile[ii]);
			continue;
		}
		/* 2-4 starLine and endLine */
		startLine[ii] = header[ii]->seg->strLineNo;
		endLine[ii]   = startLine[ii] + header[ii]->data->nLin -1;
		/* 2-5 check header consistency */
		if(n==-1)n=ii;
		if(	header[n]->calib->bandNo       != header[ii]->calib->bandNo ||
			header[n]->calib->gain_cnt2rad != header[ii]->calib->gain_cnt2rad ||
			header[n]->proj->loff          != header[ii]->proj->loff    ||
			header[n]->proj->coff          != header[ii]->proj->coff    ){
			fprintf(stderr,"header consistency error\n");
			fprintf(stderr,"%s : %s\n",arg->InFile[n],arg->InFile[ii]);
			return(ERROR_INFO);
		}
		n=ii;
	}
	/* 2-6 check file open */
	if(n==-1){
		//
		fprintf(stderr,"error : can not open all files\n");
		return(ERROR_FILE_OPEN);
	}
	/* 2-6 satellite name & band number */
	param->band = header[n]->calib->bandNo;
	strcpy(data->satName , header[n]->basic->satName);

	/* 3 get data */
	for(jj=0;jj<param->height;jj++){
	for(ii=0;ii<param->width;ii++){
		/* 3-1 init */
		count = header[n]->calib->outCount;
		kk = jj * param->width + ii;
		/* 3-2 convert lon & lat to pix & lin */
		lonlat_to_pixlin(header[n],data->lon[ii],data->lat[jj],&Pix[kk],&Lin[kk]);
		/* 3-3 min & max line */
		if(minLine > Lin[kk]) minLine =  Lin[kk];
		if(maxLine < Lin[kk]) maxLine =  Lin[kk];
		/* 3-4 get count value */
		for(ll=0;ll<arg->filenum;ll++){
            // 2015.06.06  fixed bug
	//		if(startLine[ll] <=  Lin[kk]+0.5 && Lin[kk]+0.5 <= endLine[ll]){
			if(startLine[ll] -0.5 <=  Lin[kk] && Lin[kk] < endLine[ll] + 0.5){
				hisd_getdata_by_pixlin(header[ll],fp[ll],Pix[kk],Lin[kk],&count);
				break;
			}
		}
		/* 3-5 check count value */
		if( count == header[n]->calib->outCount || 
			count == header[n]->calib->errorCount){
			data->phys[kk] = INVALID;
		}else{
		/* 3-6 convert count value to radiance */
		  const char  *oldverName="1.2";
		  if( strcmp(header[n]->basic->verName,oldverName)==0)
		  {		  
			radiance = (float)count * header[n]->calib->gain_cnt2rad +
						header[n]->calib->cnst_cnt2rad;
		  }else{
			  if((header[n]->calib->bandNo>=7 &&
				 strstr(header[n]->basic->satName,"Himawari")!=NULL ) ||
				(header[n]->calib->bandNo>=2 &&
				 strstr(header[n]->basic->satName,"MTSAT-2") !=NULL )){
				hisd_radiance_to_tbb(header[n],radiance,&phys);
				radiance = (float)count * header[n]->calib->gain_cnt2rad +
						header[n]->calib->cnst_cnt2rad;
			}else{
				/* visible or near infrared band */
				radiance = (float)count * header[n]->calib->gain_cnt2rad_mod +
						header[n]->calib->cnst_cnt2rad_mod;
						//radiance = (float)count * header[n]->calib->gain_cnt2rad +
						//header[n]->calib->cnst_cnt2rad;
			}			 			  
		  }
		/* 3-6 convert radiance to physical value */
			if(	(header[n]->calib->bandNo>=7 &&
				 strstr(header[n]->basic->satName,"Himawari")!=NULL ) ||
				(header[n]->calib->bandNo>=2 &&
				 strstr(header[n]->basic->satName,"MTSAT-2") !=NULL )){
				/* infrared band */
				hisd_radiance_to_tbb(header[n],radiance,&phys);
				data->phys[kk] = (float)100*phys ;
			}else{
				/* visible or near infrared band */
				data->phys[kk] = (float)10000*header[n]->calib->rad2albedo * radiance;
			}
		}
	}
	}

	/* 4 convert maxLine & minLine to scanTime */
	for(ll=0;ll<arg->filenum;ll++){
		/* 4-1 startTime */
		if(startLine[ll] <= minLine && minLine <= endLine[ll]){
			for(ii=1;ii<header[ll]->obstime->obsNum;ii++){
				if(minLine < header[ll]->obstime->lineNo[ii]){
					data->startTime = header[ll]->obstime->obsMJD[ii-1];
					break;
				}else if(minLine == header[ll]->obstime->lineNo[ii]){
					data->startTime = header[ll]->obstime->obsMJD[ii];
					break;
				}
			}
		}
		/* 4-2 endTime */
		if(startLine[ll] <= maxLine && maxLine <= endLine[ll]){
			for(ii=1;ii<header[ll]->obstime->obsNum;ii++){
				if(maxLine < header[ll]->obstime->lineNo[ii]){
					data->endTime = header[ll]->obstime->obsMJD[ii-1];
				}else if(maxLine == header[ll]->obstime->lineNo[ii]){
					data->endTime = header[ll]->obstime->obsMJD[ii];
				}
			}
		}
	}

	/* 5 check data */
	printf("Satellite Name : %s\n",data->satName);
	printf("Band Number    : %d\n",param->band);
	printf("physical value :\n      ");
	for(jj=0;jj<param->width ;jj=jj+param->width/20){
		printf("%6.1f ",data->lon[jj]);
	}
	printf("\n");
	for(ii=0;ii<param->height;ii=ii+param->height/20){
		kk = ii * param->width + jj;
		printf("%6.1f ",data->lat[ii]);
		for(jj=0;jj<param->width ;jj=jj+param->width/20){
			kk = ii * param->width + jj;
			printf("%6.2f ",data->phys[kk]);
		}
		printf("\n");
	}

	/* 6 free */
	for(ii=0;ii<arg->filenum;ii++){
		if(header[ii] != NULL){
			hisd_free(header[ii]);
		}
		if(fp[ii]     != NULL){
			 fclose(fp[ii]);
		}
	}
	free(header);
	free(fp);
	free(startLine);
	free(endLine);
	free(Pix);
	free(Lin);
	return(NORMAL_END);
}


int main(int argc, char *argv[]){
	parameter	param;
	argument	arg;
	outdata		data;
	long		n_size;
	long		ii;

	/* -----------------------------------------------------------------------
		1 get argument
	 -----------------------------------------------------------------------*/
	if(ERROR_ARG == getArg(argc,argv,&arg,&param)){
		return(ERROR_ARG);
	}
	/* -----------------------------------------------------------------------
		2 check parameter
	 -----------------------------------------------------------------------*/
	printf("Left top (lat,lon) : (%6.2f,%6.2f)\n",param.ltlat,param.ltlon);
	printf("width,height       : (%6d,%6d)\n",param.width,param.height);
	printf("Spatial resolution : (%6.2f,%6.2f)\n",param.dlat,param.dlon);
	n_size      = param.width * param.height;
	/* -----------------------------------------------------------------------
		3 allocate
	 -----------------------------------------------------------------------*/
	/* allocate */
	if(	NULL == (data.lat = (float *)calloc(param.height,sizeof(float *))) ||
		NULL == (data.lon = (float *)calloc(param.width, sizeof(float *))) ||
		NULL == (data.phys= (float *)calloc(n_size,      sizeof(float *))) 
	){
		fprintf(stderr,"allocate error\n");
		return(ERROR_CALLOCATE);
	}
	/* init */
	for(ii=0;ii<n_size;ii++){
		data.phys[ii] = INVALID;
	}
	/* -----------------------------------------------------------------------
		4 set longitude and latitude
	 -----------------------------------------------------------------------*/
	for(ii=0;ii<param.height;ii++){
		data.lat[ii] = param.ltlat - param.dlat * ii; 
	}
	for(ii=0;ii<param.width ;ii++){
		data.lon[ii] = param.ltlon + param.dlon * ii; 
	}
	/* -----------------------------------------------------------------------
		5 get data
	 -----------------------------------------------------------------------*/
	if(NORMAL_END != getData(&arg,&param,&data)){
		fprintf(stderr,"get data error\n");
		free(data.lon);
		free(data.lat);
		free(data.phys);
		return(ERROR_READ_DATA);
	}
	
	FILE *fpout=fopen(arg.OutFile,"wb");
	for (int dataij=0;dataij<n_size;dataij++)
	{
		 //cout<<data.phys[dataij]<<endl;
		 fwrite(&(data.phys[dataij]), sizeof(float),1, fpout);	  	
	}
	free(data.lon);
	free(data.lat);
	free(data.phys);
	printf("NORMAL END\n");
	return(NORMAL_END);
}

