from django.db import models
# Create your models here.
class User(models.Model):
    user=models.CharField(verbose_name='用户名',max_length=32)
    pwd=models.CharField(verbose_name='密码',max_length=32)
    avatar = models.FileField(upload_to='avatar/', default="avatar/default.jpg")
    isonline=models.IntegerField(verbose_name='是否在线',default=0)
    def __str__(self):
        return self.user
class UserCate(models.Model):
    phone=models.IntegerField(verbose_name='手机号',)
    email=models.EmailField(verbose_name='email',)
    addr=models.CharField(verbose_name='地址',max_length=32)
    cnum=models.IntegerField(verbose_name='ID号',)
    user=models.OneToOneField(verbose_name='用户',to='User')
    def __str__(self):
        return self.user
class Group(models.Model):
    name=models.CharField(verbose_name='分组名',max_length=32)
    user=models.ForeignKey(verbose_name='属于哪个用户',to='User')
    def __str__(self):
        return self.name
class GroupFriend(models.Model):
    friend=models.ManyToManyField(verbose_name='分组下的好友',to='User')
    group=models.OneToOneField(verbose_name='分组',to='Group')
    def __str__(self):
        return self.group.name
class ChatHistory(models.Model):
    createtime=models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    content=models.CharField(verbose_name='聊天内容',max_length=256)
    user=models.ForeignKey(verbose_name='当前聊天主场用户',to='User')
    def __str__(self):
        return self.content
class ChatFriend(models.Model):
    friend=models.ForeignKey(verbose_name='当前聊天客场用户',to='User')
    history=models.OneToOneField(verbose_name='聊天内容',to='ChatHistory')
    def __str__(self):
        return self.history.content