import enum
from django.shortcuts import render,redirect,reverse,HttpResponse
import json
from myapp import models
from django.db.models import Q
import os
import time
import datetime as dt
import pytz
import re
import base64
import rsa
import uuid

_path=os.getcwd().replace('\\','/')+"/FinanceSdkDemo"
seq=[]

name_dict={
        'Rikki':'小石总',
        'YuanJu':'袁菊',
        'NingJin':'宁锦',
        'HouYu':'张平',
        'LiQingXiang':'李清香',
        'XiaWenJuan':'夏文娟',
        'YeLingLing':'叶玲玲',
        'wmtOSfBgAARo-qdC9ITvReIb3OjPv8JA':'妙妙',
        'wmtOSfBgAAKFJD_UnyRbzUIbepAlTlaQ':'芳姐',
        'wmtOSfBgAAoc3qpSqCIdArcBDsa1xY4g':'邝老师',
        'wmtOSfBgAAOfS6YLf1LbgDY8hNOeMBXA':'袁菊家人',
        '2020005':'唐梦平',
        'wmtOSfBgAABH5A7Y2Ce05HtzNriPsqhw':'李姐',
        'wmtOSfBgAApr6HKDG9F0LThUaZ0vdEcw':'张老师',
        'wmtOSfBgAAO2N3hKG4ZvsM9rKUOSEw8g':'辉哥',
        'wotOSfBgAAd_NajBcFgiscDzoTOylc_g':'客服',
        'ShiTou':'大石总',
        'SunXiu':'孙秀',
        'ZhangPing':'张平',
        'wmtOSfBgAAaLGJ6b_tr4Qkrrzej_tPwg':'温总',
    }

def handle_name():
    health_name=[x.name for x in models.Health.objects.all()]
    customer_name=[x.name for x in models.Customer.objects.all()]
    customer_health=[x.health for x in models.Customer.objects.all()]
    send_name=list(set([x.send for x in models.Content.objects.all()]))
    recive_name=list(set([x.recive for x in models.Content.objects.all()]))
    customer_list=[x.customer_list for x in models.Health.objects.all()]
    new_customer_list=[x.customer_list for x in models.Health.objects.all()]
    content=[x.content for x in models.Content.objects.all()]
    new_content=[x.content for x in models.Content.objects.all()]

    for index in range(len(content)):
        for key,value in name_dict.items():
            if key in new_content[index]:
                new_content[index]=new_content[index].replace(key,value)
    
                
    for index,x in enumerate(content):
        models.Content.objects.filter(content=x).update(content=new_content[index])

    for x in customer_health:
        for key,value in name_dict.items():
            if x==key:
                models.Customer.objects.filter(health=key).update(health=value)

    for index in range(len(customer_list)):
        for key,value in name_dict.items():
            if key in new_customer_list[index]:
                new_customer_list[index]=new_customer_list[index].replace(key,value)
    
                
    for index,x in enumerate(customer_list):
        models.Health.objects.filter(customer_list=x).update(customer_list=new_customer_list[index])
    
    for x in health_name:
        for key,value in name_dict.items():
            if x==key:
                models.Health.objects.filter(name=key).update(name=value)
    for x in customer_name:
        for key,value in name_dict.items():
            if x==key:
                models.Customer.objects.filter(name=key).update(name=value)
    for x in send_name:
        for key,value in name_dict.items():
            if x==key:
                models.Content.objects.filter(send=key).update(send=value)
    for x in recive_name:
        for key,value in name_dict.items():
            if x==key:
                models.Content.objects.filter(recive=key).update(recive=value)
    
   

def flat(nums):
    res = []
    for i in nums:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res
                
def ac_jiami(text):
    global seq
    ###ip加入，开始获取内容
    r=re.findall('"chatdata":(.*)}',text)[0][1:-1].split('},')
    ### print(r)

    ##获取加密字段encrypt_random_key,encrypt_chat_msg,seq
    encrypt_random_key,encrypt_chat_msg,limit_num=[],[],len(r)-1

    for value in r:
        key=re.findall('"encrypt_random_key":(.*),"encrypt_chat_msg"',value)[0][1:-1]
        encrypt_random_key.append(key)

        msg=re.findall('"encrypt_chat_msg":(.*)',value)[0][1:-1]
        encrypt_chat_msg.append(msg)

        s=int(re.findall('"seq":(.*),"msgid"',value)[0])
        # print(s)
        seq.append(s)
    
    encrypt_chat_msg[-1]=encrypt_chat_msg[-1][:-1]

    # ##将得到的加密字段encrypt_random_key存入encrypt_random_key.txt中
    with open('{}/encrypt_random_key.txt'.format(_path),'w') as f:
        for x in encrypt_random_key:
            f.write(x)
            f.write('\n')
    f.close()

    # #将得到的加密字段encrypt_chat_msg存入encrypt_chat_msg.txt中
    with open('{}/encrypt_chat_msg.txt'.format(_path),'w') as f:
        for x in encrypt_chat_msg:
            f.write(x)
            f.write('\n')
    f.close()


def jiemi():
    # ##将encrypt_random_key进行base64解码
    with open('{}/encrypt_random_key.txt'.format(_path),'r') as f:
        b=f.readlines()
    f.close()
    c=[x[:-1] for x in b if x!='\n']
    # print(c[0])
    crypt_text=[]
    for x in c:
        s=bytes(x,'utf-8')
        res=base64.b64decode(s)
        crypt_text.append(res)
    # print(len(crypt_text))

    # ###解密encrypt_random_key放入key.txt中
    f2=open('{}/key.txt'.format(_path),'w')

    with open('{}/private.pem'.format(_path), 'rb') as f:
        p = f.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
        for y in crypt_text:
            lase_text = rsa.decrypt(y, privkey).decode() # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str
            f2.write(lase_text)
            f2.write('\n')
    f.close()
    f2.close()


def ruku():
    ## #获取解密后的明文并存放在res.txt中
    os.system('cd {}&\
                call vcvars64.bat&\
                cl result.cpp&\
                result.exe'.format(_path))
    
    time.sleep(0.5)
    # ## 读取res.txt,整理需要的内容
    content=[]
    with open("{}/res.txt".format(_path),'rb') as f:
        for x in f.readlines():
            try:
                content.append(x.decode('utf-8'))
            except:
                content.append(str(x))
    # print(content)
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
    
    for index,value in enumerate(_msgtype):
        if value in ['image','emotion','file']:
            f=open('{}/img.txt'.format(_path),'w') if value !='file' else open('{}/img.txt'.format(_path),'w',encoding='gbk')
            txt_content=_msgcontent[index] if value !='file' else _msgcontent[index].split('###')[1]
            f.write(txt_content)
            f.write('\n')
            img_name='img/'+str(uuid.uuid4())+'.jpg' if value !='file' else 'file/'+_msgcontent[index].split('###')[0]
            f.write('../vue/static/'+img_name)
            _msgcontent[index]='../../static/'+img_name
            
            f.close()
            time.sleep(0.5)
            os.system('cd {}&\
                    call vcvars64.bat&\
                    cl img.cpp&\
                    img.exe'.format(_path))
            time.sleep(1)

    _many_list=[]

    for index,value in enumerate(_tolist):
        if '","' in value:
            _tolist[index]=_tolist[index].split('","')
            _many_list.append(index)
        
    
    if _many_list:
        for x in _many_list:
            if type(_tolist[x])==list:
                seq[x]=[seq[x] for y in range(len(_tolist[x]))]
                _form[x]=[_form[x] for y in range(len(_tolist[x]))]
                _msgtime[x]=[_msgtime[x] for y in range(len(_tolist[x]))]
                _msgtype[x]=[_msgtype[x] for y in range(len(_tolist[x]))]
                _msgcontent[x]=[_msgcontent[x]+'(群发消息:{})'.format(_tolist[x]) for y in range(len(_tolist[x]))]
        
        
        seq2=flat(seq)
        _form=flat(_form)
        _tolist=flat(_tolist)
        _msgtime=flat(_msgtime)
        _msgtype=flat(_msgtype)
        _msgcontent=flat(_msgcontent)

    ##将新获取的内容入库
    for index in range(len(_msgtime)):
        models.Content.objects.create(
                    seq=seq2[index] if _many_list else seq[index],
                    send=_form[index],
                    recive=_tolist[index],
                    msgtime=_msgtime[index],
                    msgtype=_msgtype[index],
                    content=_msgcontent[index]
                    )

    # 将最新seq放入seq.txt中
    with open('{}/seq.txt'.format(_path),'w') as f:
        r=str(seq[-1]) if type(seq[-1])!=list else str(seq[-1][0])
        f.write(r)
    f.close()

def ac_old():
    exist_all=models.Content.objects.all()
    exist_send=[x.send for x in exist_all]
    exist_recive=[x.recive for x in exist_all]
    exist_res=set([exist_send[x]+'——>'+exist_recive[x] for x in range(len(exist_all))])
    return exist_res

def ac_new():
    exist_all=models.Content.objects.all()
    exist_send=[x.send for x in exist_all]
    exist_recive=[x.recive for x in exist_all]
    exist_res=set([exist_send[x]+'——>'+exist_recive[x] for x in range(len(exist_all))])
    return exist_res

###获取新的聊天内容入库--->ac_content.vue
def ac_content(request):
    mes={'code':0,'ip':'','add':''}
    if request.method == 'GET':
        ##发起请求
        a=os.popen('cd {}&\
                    call vcvars64.bat&\
                    cl laqu.cpp&\
                    laqu.exe'.format(_path))                     
        text = a.read()                     
        a.close()

        
        ip=re.findall('ip:(.*?),',text)
        # print((ip))
        if ip:
            mes['ip']=ip[0][1:]    #ip没有加入
        else:
            t=re.findall('"chatdata":(.*)?}',text)[0]
            #判断是否有新的聊天内容，如果有开始获取
            # print(len(t))
            if len(t)>3:
                old_res=ac_old()
                ac_jiami(text)      ###获取加密字段：encrypt_random_key，encrypt_chat_msg,seq
                jiemi()             ###对字段encrypt_random_key进行解密
                ruku()              ###明文入库
                handle_name()       ###修改名字
                new_res=ac_new()
                ###查看有没有新增的健康师或者客户,在前端显示需要添加的具体信息
                is_new=[x for x in new_res if x not in old_res]
                if is_new:
                    mes['add']=is_new
                mes['code']=200     ###ip加入开始操作
            else:
                mes['code']=100
    return HttpResponse(json.dumps(mes,ensure_ascii=False))



###获取健康师与客户的信息--->health.vue 展示健康师与客户的关系 点击进入聊天界面
def ac_health(request):
    mes={'code':0}
    is_gai=True
    if request.method == 'GET':
        # handle_name()
        ac_old()
        health_list=models.Health.objects.all()
        name=[x.name for x in health_list]

       
        customer=[]
        for x in health_list:
            c=x.customer_list.split(',') if ',' in x.customer_list else [x.customer_list]
            customer.append(c)
        

        if is_gai:
            for index,value in enumerate(name):
                res=''
                for x in customer[index]:
                    res=res+str(x)+','
                models.Health.objects.filter(name=value).update(customer_list=res[:-1])


        mes['health']={}
        name=[x.name for x in health_list]
        b=[[{'name':x,'customer':y} for x in name] for y in customer]
        mes['health']=[b[x][x] for x in range(len(b))]
        
        mes['code']=200

        is_gai2=True

        ask=models.Content.objects.all()
        send=[x.send for x in ask]
        recive=[x.recive for x in ask]
        
    return HttpResponse(json.dumps(mes,ensure_ascii=False))


def ac_time(utc_ms_ts, tz_info):
    utc_datetime = dt.datetime.utcfromtimestamp(utc_ms_ts / 1000.)
    return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz_info)

###接收前端发送来的健康师和客户呢称获取聊天内容展示---> talk.vue
def ac_talk(request):
    mes={'code':200}
    if request.method == 'POST':
        health=request.POST.get('health')
        customer=request.POST.get('customer')
        start_y=request.POST.get('start_y')
        start_h=request.POST.get('start_h')
        end_y=request.POST.get('end_y')
        end_h=request.POST.get('end_h')

        all_=models.Content.objects.filter(Q(send=health,recive=customer)|Q(send=customer,recive=health))

        t=[x.msgtime for x in all_]
        # print(t)
        if len(t)<1:
            mes['code']=100
            return HttpResponse(json.dumps(mes,ensure_ascii=False))
        
        if start_h:

            y_list,h_list=start_y.split('-'),start_h.split(':')
            year,mouth,day,hour,m=y_list[0],y_list[1],y_list[2],h_list[0],h_list[1]
            start_msgstrap=str(dt.datetime(int(year),int(mouth),int(day),int(hour),int(m)).timestamp())[:-2]+'000'

            y_list,h_list=end_y.split('-'),end_h.split(':')
            year,mouth,day,hour,m=y_list[0],y_list[1],y_list[2],h_list[0],h_list[1]
            end_msgstrap=str(dt.datetime(int(year),int(mouth),int(day),int(hour),int(m)).timestamp())[:-2]+'000'
            
            if start_msgstrap>end_msgstrap:
                mes['code']=0
                return HttpResponse(json.dumps(mes,ensure_ascii=False))
            start_index,end_index=0,0
            for index,value in enumerate(t):
                if int(value)>=int(start_msgstrap):
                    start_index=index
                    break
                if index==len(t)-1:
                    mes['code']=100
                    return HttpResponse(json.dumps(mes,ensure_ascii=False))

            for index,value in enumerate(t):
                if int(value)==int(end_msgstrap):
                    end_index=index
                    break
                if int(value)>int(end_msgstrap):
                    end_index=index-1
                    break
                if index==len(t)-1:
                    end_index=len(t)-1
            t=t[start_index:end_index+1]
            all_=all_[start_index:end_index+1]
        
        mes['res_msg']=[x.content for x in all_]
        
        more={}
        for index,value in enumerate(t):
            if t.count(value)>1:
                if value not in more:
                    more[value]=[index]
                else:
                    more[value].append(index)
        res_list=[]
        if more:
            for x in more.values():
                res_list.extend(x[1:])
                for i in reversed(x[1:]):
                    t[i]=1
                    mes['res_msg'][i]=1
        for x in res_list:
            t.remove(1)
            mes['res_msg'].remove(1)
        mes['send']=[models.Content.objects.filter(msgtime=x).first().send for x in t]
        mes['res_time']=[ac_time(int(x),pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d\t%H:%M:%S') for x in t]
        mes['msgtype']=[models.Content.objects.filter(msgtime=x).first().msgtype for x in t]
        # print(mes['msgtype'])
        # print(mes['res_msg'])
    return HttpResponse(json.dumps(mes,ensure_ascii=False))

def zeng(msg):
    res=models.Health.objects.filter(name=msg)
    if res:
        return None
    else:
        res.create(name=msg,customer_list='')
    return 1

def shan(msg):
    res=models.Health.objects.filter(name=msg)
    if res:
        res.delete()
        models.Customer.objects.filter(health=msg).delete()
        return 1
    return None

def gai(msg):
    res=models.Health.objects.filter(name=msg)
    if res:
        return 1
    return None

def cha(msg):
    res=models.Health.objects.filter(name=msg)
    return res.first().name if res else None


def handle_health(request):
    mes={'code':0,'zeng':'','shan':'','gai':'','cha':''}
    if request.method == 'POST':
        msgtype=request.POST.get('msgtype')
        msg=request.POST.get('msg')
        if msgtype=='增加':
            mes['zeng']=zeng(msg)
            mes['code']=200 if mes['zeng'] else 0
        if msgtype=='删除':
            mes['shan']=shan(msg)
            mes['code']=200 if mes['shan'] else 0
        if msgtype=='修改':
            mes['gai']=gai(msg)
            mes['code']=200 if mes['gai'] else 0
        if msgtype=='查询':
            mes['cha']=cha(msg)
            mes['code']=200 if mes['cha'] else 0
    return HttpResponse(json.dumps(mes,ensure_ascii=False))

def gai_health(request):
    mes={'code':200}
    if request.method == 'POST':
        gai_ever=request.POST.get('gai_ever')
        gai_res=request.POST.get('gai_res')
        models.Health.objects.filter(name=gai_ever).update(name=gai_res)
        models.Customer.objects.filter(health=gai_ever).update(health=gai_res)
        models.Content.objects.filter(send=gai_ever).update(send=gai_res)
        models.Content.objects.filter(recive=gai_ever).update(recive=gai_res)
    return HttpResponse(json.dumps(mes,ensure_ascii=False))


def ac_customer(request):
    mes={'code':200}
    if request.method == 'GET':
        customer_list=models.Customer.objects.all()
        customer_name=[x.name for x in customer_list]
        customer_health=[x.health for x in customer_list]
        mes['customer_list']={x:y for x,y in zip(customer_name,customer_health)}
        mes['health_list']=[x.name for x in models.Health.objects.all()]
        
    return HttpResponse(json.dumps(mes,ensure_ascii=False))

def gai_customer(request):
    mes={'code':200}
    if request.method == 'POST':
        old_customer=request.POST.get('old_customer')
        customer=request.POST.get('customer')
        old_health=request.POST.get('old_health')
        health=request.POST.get('health')
        if old_health!=health:
            c=models.Health.objects.filter(name=old_health).first().customer_list.split(',')
            models.Customer.objects.filter(name=old_customer).update(health=health)
            cus_list=[x for x in c if x!=old_customer]
            cus_str=''
            for x in cus_list:
                cus_str=cus_str+x+','
            models.Health.objects.filter(name=old_health).update(customer_list=cus_str[:-1])

            add=old_customer if old_customer==customer else customer
            ever=models.Health.objects.filter(name=health).first().customer_list
            c2=ever+','+add if ever else add
            models.Health.objects.filter(name=health).update(customer_list=c2)

            c3=customer if customer==old_customer else old_customer
            models.Content.objects.filter(Q(send=old_health,recive=c3)).update(send=health)
            models.Content.objects.filter(Q(send=c3,recive=old_health)).update(recive=health)

        if old_customer!=customer:
            models.Customer.objects.filter(name=old_customer).update(name=customer)
            c=models.Health.objects.filter(name=old_health).first().customer_list.split(',')
            for index,value in enumerate(c):
                if value==old_customer:
                    c[index]=customer
            res_cus=''
            for x in c:
                res_cus=res_cus+x+','
            models.Health.objects.filter(name=old_health).update(customer_list=res_cus[:-1])

            models.Content.objects.filter(Q(send=old_customer,recive=health)).update(send=customer)
            models.Content.objects.filter(Q(send=health,recive=old_customer)).update(recive=customer)

    return HttpResponse(json.dumps(mes,ensure_ascii=False))


def del_customer(request):
    mes={'code':200}
    if request.method == 'POST':
        customer=request.POST.get('customer')
        health=request.POST.get('health')
        models.Customer.objects.filter(name=customer).delete()
        c=models.Health.objects.filter(name=health).first().customer_list.split(',')
        c2=[x for x in c if x!=customer]
        s=''
        for x in c2:
            s=s+x+','
        models.Health.objects.filter(name=health).update(customer_list=s[:-1])
    return HttpResponse(json.dumps(mes,ensure_ascii=False))


def add_customer(request):
    mes={'code':200}
    if request.method == 'POST':
        customer=request.POST.get('customer')
        health=request.POST.get('health')
        if not models.Customer.objects.filter(Q(name=customer)&Q(health=health)):
            models.Customer.objects.create(name=customer,health=health)
            c=models.Health.objects.filter(name=health).first().customer_list
            c2=c+','+customer if c else customer
            models.Health.objects.filter(name=health).update(customer_list=c2)
        else:
            mes['code']=0
    return HttpResponse(json.dumps(mes,ensure_ascii=False))


def cha_customer(request):
    mes={'code':0}
    if request.method == 'POST':
        customer=request.POST.get('customer')
        res=models.Customer.objects.filter(name=customer).first()
        if res:
            mes['code']=200
            mes['health']=res.health
    return HttpResponse(json.dumps(mes,ensure_ascii=False))
    