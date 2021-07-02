#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string>
#include <Windows.h>
#include <fstream>
using namespace std;
using std::string;
#include "WeWorkFinanceSdk_C.h"

#pragma comment(lib, "WeWorkFinanceSdk.lib")

int main(int argc, char *argv[]){

    FILE *fp;
    fp=fopen("key.txt","r");
    int line=0;
    char c;
    while((c=getc(fp))!=EOF)
    {
      if(c=='\n')
        line++;
     }
    fclose(fp);
    // printf("%d\n\n\n",line);

    // 连接接口
    int ret=111;
    // printf("ret:%d\n",ret);
    WeWorkFinanceSdk_t* sdk = NewSdk();
    ret = Init(sdk,"ww6e3c545d87791cec","1Glr1VXDLGPnalNF5NrRuSlV8WqFoku4wek91CAy0mQ");
    // printf("ret:%d\n",ret);

    //读取解密内容
    int ret3=333;
    Slice_t* Msgs = NewSlice();

    int x=0;
    char encrypt_msg[500][999];
    ifstream in("encrypt_chat_msg.txt");
    char str[10240]={0};
    while( in.getline(str,sizeof(str),'\n' ) )
    {
        strcpy(encrypt_msg[x],str);
        x++;
    }
    in.close();
    

    int y=0;
    char encrypt_key[500][999];
    ifstream on("key.txt");
    char str2[10240]={0};
    while( on.getline(str2,sizeof(str2),'\n' ) )
    {
      strcpy(encrypt_key[y],str2);
      y++;
    }
    on.close();

    
    FILE *fp2;
    fp2=fopen("res.txt","w");
    setbuf(fp2,NULL);

    for(int i=0;i<line;i++){
        ret3 = DecryptData(encrypt_key[i], encrypt_msg[i], Msgs);
        printf("chatdata :%s ret :%d\n\n", Msgs->buf, ret);
        fprintf(fp2,Msgs->buf);
        fprintf(fp2,"\n");
        fflush(fp2);
        Sleep(100);
    }
    
    FreeSlice(Msgs);
    
}
