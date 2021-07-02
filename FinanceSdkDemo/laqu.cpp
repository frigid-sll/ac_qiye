#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string>
using std::string;
#include "WeWorkFinanceSdk_C.h"
#include <Windows.h>

#pragma comment(lib, "WeWorkFinanceSdk.lib")

int main(int argc, char *argv[]){

    // 连接接口
    int ret=111;
    // printf("ret:%d\n",ret);
    WeWorkFinanceSdk_t* sdk = NewSdk();
    ret = Init(sdk,"ww6e3c545d87791cec","1Glr1VXDLGPnalNF5NrRuSlV8WqFoku4wek91CAy0mQ");
    // printf("ret:%d\n",ret);

    //获取最新seq
    FILE *fp;
    fp=fopen("seq.txt","r");
    int c;
    fscanf(fp,"%d",&c);
    fclose(fp);

    //获取加密内容
    int ret2=222;
    // printf("ret2:%d\n",ret2);
    uint64_t iSeq = c;
    uint64_t iLimit = 499;
    uint64_t timeout = 10;        
    Slice_t* chatDatas = NewSlice();

    ret2 = GetChatData(sdk, iSeq, iLimit, "","", timeout, chatDatas);
    printf("ret2:%d\n",ret2);
    printf("GetChatData len:%d data:%s\n", chatDatas->len, GetContentFromSlice(chatDatas));
    FreeSlice(chatDatas);
}
