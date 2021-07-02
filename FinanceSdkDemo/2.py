# #获取需要的加密字段

# import os
# import re

# path=os.getcwd().replace('\\','/')

# a=os.popen('cd path&\
# 			call vcvars64.bat&\
# 			cl t.cpp&\
# 			t.exe')

# text = a.read()
# a.close()

# r=re.findall('"chatdata":(.*)}',text)[0][1:-1].split('},')

# # print(r)

# encrypt_random_key,encrypt_chat_msg,length=[],[],len(r)-1

# for index,value in enumerate(r):
# 	key=re.findall('"encrypt_random_key":(.*),"encrypt_chat_msg"',value)[0][1:-1]
# 	encrypt_random_key.append(key)

# 	msg=re.findall('"encrypt_chat_msg":(.*)',value)[0][1:-1] if index!=length else re.findall('"encrypt_chat_msg":(.*)',value)[0][1:-2]
# 	encrypt_chat_msg.append(msg)

# with open('encrypt_random_key.txt','w') as f:
# 	for x in encrypt_random_key:
# 		f.write(x)
# 		f.write('\n')
# f.close()

# with open('encrypt_chat_msg.txt','w') as f:
# 	for x in encrypt_chat_msg:
# 		f.write(x)
# 		f.write('\n')
# f.close()




##将encrypt_random_key进行base64解码
# import base64
# with open('encrypt_random_key.txt','r') as f:
# 	b=f.readlines()
# f.close()
# c=[x[:-1] for x in b if x!='\n']
# # print(c[0])
# crypt_text=[]
# for x in c:
# 	s=bytes(x,'utf-8')
# 	res=base64.b64decode(s)
# 	crypt_text.append(res)
# print(len(crypt_text))


# ##解密encrypt_random_key
# import rsa

# f2=open('key.txt','w')

# with open('private.pem', 'rb') as f:
# 	p = f.read()
# 	privkey = rsa.PrivateKey.load_pkcs1(p)
# 	for y in range(0,3):
# 		lase_text = rsa.decrypt(crypt_text[y], privkey).decode() # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str
# 		f2.write(lase_text)
# 		f2.write('\n')
# f.close()
# f2.close()


##将时间戳转化为本地时间
# import datetime as dt
# import pytz

# def tz_from_utc_ms_ts(utc_ms_ts, tz_info):
#     utc_datetime = dt.datetime.utcfromtimestamp(utc_ms_ts / 1000.)

#     return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz_info)

# utc_ts = [	1619399640042,1619399270311,1619396618500,1619394509174,1619351560661,
# 			1619351158358,1619351013697,1619351006061,1619351002573,1619350724602,
# 			1619350718441,1619350709945,1619350696847,1619350671878,1619350661563,
# 			1619350650178,1619350643878,1619350642139,1619350615977,1619350605319,
# 			1619350599951,1619350580385,1619350572670,1619350559098,1619350511100,
# 			1619350509000,1619349016606,1619349012936,1619347775074,1619347713501,
# 			1619340738248,1619337321885,1619337301969,1619337279862,1619336856646,
# 			1619336799740,1619336778298,1619336761419,1619336716757,1619336344809,
# 			1619335492027,1619331095359,1619331015724,1619331005992,1619330954609,
# 			1619330937972,1619322614668,1619322599816,1619322595009,1619314783702,
# 			1619310067631,1619310033956,1619268374245,1619268367079,1619268201546,
# 			1619265751564,1619265636123,1619265209345,1619256014874,1619225626426,
# 			1619225596722,1619225586833,1619225552984
# 		]

# for x in range(0,63):
# 	tz_dt = tz_from_utc_ms_ts(utc_ts[x], pytz.timezone('Asia/Shanghai'))

# 	print(tz_dt.strftime('%Y-%m-%d\t%H:%M:%S'))




from selenium import webdriver
import threading
import requests
import re
import uuid
import time
import os



content=[]
with open("res.txt",'rb') as f:
    for x in f.readlines():
        try:
            content.append(x.decode('utf-8'))
        except:
            content.append(str(x))
f.close()
_form=[re.findall('"from":"(.*?)",',x)[0] for x in content]
_tolist=[re.findall('"tolist":(.*?),"roomid"',x)[0][2:-2] for x in content]
_msgtime=[re.findall('"msgtime":(.*?),"',x)[0] for x in content]
_msgtype=[re.findall('"msgtype":"(.*?)",',x)[0] for x in content]
_msgcontent=[]

for index,value in enumerate(_msgtype):
    if value=='text':
        _msgcontent.append(re.findall('"content":(.*?)}}',content[index])[0][1:-1])
    if value in ['image','emotion']:
        _msgcontent.append(re.findall('"sdkfileid":(.*?)}}',content[index])[0][1:-1])
        
    if value=='location':
        _msgcontent.append(
            re.findall('"address":(.*?),"title"',content[index])[0][1:-1]+re.findall('"title":(.*?),"zoom"',content[index])[0][1:-1]
            )
    if value=='revoke':
        _msgcontent.append(
            '撤回了一条消息'
        )
    if value=='file':
        name=re.findall('"filename":(.*?),"',content[index])[0][1:-1]
        sdkfileid=re.findall('"sdkfileid":(.*?)}}',content[index])[0][1:-1]
        _msgcontent.append(
            name+'###'+sdkfileid
            )
    if value=='weapp':
        _msgcontent.append(
            re.findall('displayname":(.*)}}',content[index])[0][1:-1]+'小程序'
        )
    if value not in ['text','location','image','revoke','emotion','file','weapp']:
        _msgcontent.append(content[index])


f=open('code.txt','w') if value !='file' else open('code.txt','w',encoding='gbk')
ff=open('name.txt','w') if value !='file' else open('name.txt','w',encoding='gbk')

for index,value in enumerate(_msgtype):
    if value in ['image','emotion','file']:
    	
    	txt_content=_msgcontent[index] if value !='file' else _msgcontent[index].split('###')[1]
    	f.write(txt_content)
    	f.write('\n')

    	img_name='img/'+str(uuid.uuid4())+'.jpg' if value !='file' else 'file/'+_msgcontent[index].split('###')[0]
    	ff.write('static/'+img_name)
    	ff.write('\n')

    	_msgcontent[index]='../../static/'+img_name
        
f.close()        
ff.close()

os.system('call vcvars64.bat&\
        cl img2.cpp&\
        img2.exe'
)