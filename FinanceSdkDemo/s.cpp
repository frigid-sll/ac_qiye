#include <iostream>
#include <fstream>
using namespace std;
int main()
{
      char c[300][1000];
      int i=0;
      int a=10;
      ifstream on("encrypt_chat_msg.txt");
      char str2[2048]={0};
      while( on.getline(str2,sizeof(str2),'\n' ) )
      {
         strcpy(c[i],str2);
         i++;
      }
      on.close();
      printf(c[0]);
      printf("\n\n");

   // int y=0;
   // char d[3][999];
   // ifstream in("encrypt_chat_msg.txt");
   // char str[1024]={0};
   // while( in.getline(str,sizeof(str),'\n' ) )
   // {
   // strcpy(d[y],str);
   // y++;
   // }
   // in.close();
   // printf(d[0]);
   // printf("\n\n");

   // FILE *fp;
   // fp=fopen("seq.txt","r");
   // int c;
   // fscanf(fp,"%d",&c);
   // printf("%d",c);
   // fclose(fp);
}

// #include <iostream>
// #include <fstream>
// using namespace std;

// int main()
// {
//    FILE *fp;
//    fp=fopen("res.txt","r");
//    int line=0;
//    char c;
//    while((c=getc(fp))!=EOF)
//     {
//       if(c=='\n')
//         line++;
//      }
//     printf("%d",line);
// }