from django.db import models

# Create your models here.
class Health(models.Model):
    name=models.CharField(max_length=50,verbose_name='健康师姓名')
    customer_list=models.CharField(max_length=200,verbose_name='负责的客户列表')
    class Meta:
        verbose_name_plural='健康师表'
    def __str__(self):
        return self.name

class Customer(models.Model):
    name=models.CharField(max_length=50,verbose_name='客户姓名')
    health=models.CharField(max_length=200,verbose_name='所属健康师')
    class Meta:
        verbose_name_plural='客户表'
    def __str__(self):
        return self.name

class Content(models.Model):
    seq=models.IntegerField(verbose_name='seq值',default=0)
    send=models.CharField(max_length=50,verbose_name='发送方')
    recive=models.CharField(max_length=50,verbose_name='接收方')
    msgtype=models.CharField(max_length=20,verbose_name='发送内容类型')
    content=models.CharField(max_length=500,verbose_name='发送的内容')
    msgtime=models.CharField(max_length=50,verbose_name='发送时间戳')

    class Meta:
        verbose_name_plural='聊天表'
    def __str__(self):
        res=str(self.seq)+'：'+self.send+'-->'+self.recive
        return res