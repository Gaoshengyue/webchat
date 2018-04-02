from django.shortcuts import render,HttpResponse,redirect
from app01.geetest import GeetestLib
from django.http import JsonResponse
from app01.models import *
from django.db.models import Q
# Create your views here.
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"
def register(request):
    if request.method=='POST':
        user=request.POST.get('user')
        pwd=request.POST.get('pwd')
        avatar_img = request.FILES.get("file_img")
        userc=User.objects.filter(user=user).first()
        if userc:
            return HttpResponse(3)
        else:
            users=User.objects.create(user=user,pwd=pwd,avatar=avatar_img)
            group=Group.objects.create(name=user+'的分组',user=users)
            GroupFriend.objects.create(group=group)
            if users:
                return HttpResponse(1)
            else:
                return HttpResponse(2)
    return render(request, 'register.html')
def login(request):
    if request.method=='POST':
        user=request.POST.get('user')
        pwd=request.POST.get('pwd')
        users=User.objects.filter(user=user,pwd=pwd).first()
        useru=User.objects.filter(user=user).first()
        if users:
            User.objects.filter(user=user).update(isonline=1)
            users = User.objects.filter(user=user, pwd=pwd).first()
            userd = {'id': users.id, 'user': users.user, 'isonline': users.isonline,'avatar': '/media/' + str(users.avatar)}
            request.session['user']=userd
            return HttpResponse(1)
        elif useru:
            return HttpResponse(2)
        else:
            return HttpResponse(3)
    return render(request,'login.html')
def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)
def index(request):
    if request.session.get('user'):
        uid = request.session['user']['id']
        user=User.objects.filter(id=uid).first()
        friend=Group.objects.filter(user=user).values('groupfriend__friend__user','groupfriend__friend__avatar','groupfriend__friend__isonline','groupfriend__friend__id')
        return render(request,'index.html',locals())
    else:
        return redirect('/login/')
def select(request):
    if request.method=='POST':
        user=request.POST.get('user')
        friend=User.objects.filter(user__contains=user).first()
        ret ={}
        if friend:
           ret['friend_avatar']=str(friend.avatar)
           ret['friend_name']=friend.user
           ret['friend_id']=friend.id
           ret['sta']=1
        else:
            ret['sta']=2
        return JsonResponse(ret)
def addfriend(request):
    if request.method=='POST':
        uid = request.session['user']['id']
        fid=request.POST.get('fid')
        friend=User.objects.filter(id=fid).first()
        user=User.objects.filter(id=uid).first()
        friend_behind=Group.objects.filter(user_id=uid).values('groupfriend__friend__id')
        ret = {}
        behind = []
        for item in friend_behind:
            behind.append(item['groupfriend__friend__id'])
        if int(fid) in behind:
            ret['sta'] = 3
            return JsonResponse(ret)
        friend_obj=GroupFriend.objects.filter(group__user_id=uid).first()
        friend_obj.friend.add(friend)
        user_obj = GroupFriend.objects.filter(group__user_id=fid).first()
        user_obj.friend.add(user)
        friends = Group.objects.filter(user_id=uid).values('groupfriend__friend__id')
        le=[]
        for item in friends:
             le.append(item['groupfriend__friend__id'])
        if int(fid) in le:
            ret['sta']=1
            ret['friend_avatar'] = str(friend.avatar)
            ret['friend_name'] = friend.user
            ret['friend_id'] = friend.id
        else:
            ret['sta']=2
    return JsonResponse(ret)
def logout(request,id):
    User.objects.filter(id=id).update(isonline=0)
    request.session.clear()
    return redirect('/login/')

def chatlog(request):
    uid=request.GET.get('uid')
    fid = request.GET.get('fid')
    chatlist=ChatHistory.objects.filter(Q(user_id=uid,chatfriend__friend_id=fid)|Q(user_id=fid,chatfriend__friend_id=uid)).order_by('createtime').reverse()
    if chatlist:
        dit={}
        le=[]
        for item in chatlist.reverse():
            dit['createtime']=item.createtime.strftime("%Y-%m-%d %H:%M")
            dit['content']=item.content
            dit['userid']=item.user_id
            us=User.objects.filter(id=item.user_id).first()
            dit['username']=us.user
            dit['avatar']=str(us.avatar)
            le.append(dit)
            dit={}

        return JsonResponse(le,safe=False)
    else:
        return JsonResponse(1,safe=False)

def addchat(request):
    if request.method=='POST':
        content=request.POST.get('content')
        uid=request.POST.get('uid')
        fid = request.POST.get('fid')
        history=ChatHistory.objects.create(content=content,user_id=uid)
        chaf=ChatFriend.objects.create(friend_id=fid,history_id=history.id)
        ret={}
        if chaf:
            ret['sta']=1
        else:
            ret['sta']=2
        return JsonResponse(ret)
# def chathitory(request):
#
