#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string>
#include <Windows.h>
#include "WeWorkFinanceSdk_C.h"
#include <fstream>
using namespace std;
using std::string;

#pragma comment(lib, "WeWorkFinanceSdk.lib")

int main(int argc, char *argv[]){

    // 连接接口
    int ret=111;
    // printf("ret:%d\n",ret);
    WeWorkFinanceSdk_t* sdk = NewSdk();
    ret = Init(sdk,"ww6e3c545d87791cec","1Glr1VXDLGPnalNF5NrRuSlV8WqFoku4wek91CAy0mQ");
    // printf("ret:%d\n",ret);

    //获取图片
    int ret4=444;
    std::string index;
    uint64_t timeout = 10;
    int isfinish = 0;
    
    int y=0;
    char img[500][999];
    ifstream on("img.txt");
    char str2[10240]={0};
    while( on.getline(str2,sizeof(str2),'\n' ) )
    {
      strcpy(img[y],str2);
      y++;
    }
    on.close();


    const char* sdkFileid=img[0];
    while (isfinish == 0) {

        MediaData_t* mediaData = NewMediaData();
        ret4 = GetMediaData(sdk, index.c_str(), sdkFileid, "", "", timeout, mediaData);
        // printf("ret4:%d\n",ret4);
        
        // printf("content size:%d isfin:%d outindex:%s\n", mediaData->data_len, mediaData->is_finish, mediaData->outindexbuf);
       
        char file[200];
        snprintf(file, sizeof(file), "%s", img[1]);
        FILE* fp = fopen(file, "ab+");
        // printf("filename:%s \n", file);
        if (NULL == fp) {
            FreeMediaData(mediaData);
            printf("open file err\n");
            return -1;
        }

        fwrite(mediaData->data, mediaData->data_len, 1, fp);
        fclose(fp);

        index.assign(string(mediaData->outindexbuf));
        isfinish = mediaData->is_finish;
        FreeMediaData(mediaData);

        
    }
       
}
