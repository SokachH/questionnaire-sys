from django.shortcuts import HttpResponse
import json
from myAdmin.models import *
from django.db import transaction,connection
from django.db.models import Q
from io import BytesIO
import base64
############################################################
#功能：问卷设计者操作主入口
#最后更新：2019-05-23
############################################################
def opera(request):
    response={'code':0,'msg':'success'}

    if request.method=='POST':
        body=str(request.body,encoding='utf-8')
        print(body)
        try:
            info = json.loads(body)#解析json报文
        except:
            response['code'] = '-2'
            response['msg'] = '请求格式有误'
        else:
            opera_type = info.get('opera_type')  # 获取操作类型
            username = request.session.get('username')

            if opera_type:#如果操作类型不为空
                if opera_type == 'login':
                    response = login(info, request)
                elif opera_type == 'adminlogin':
                    response = adminlogin(info, request)
                elif opera_type == 'logincheck':
                    response = loginCheck(request)
                elif opera_type == 'register':
                    response = register(info)
                elif opera_type == 'resetpass':
                    response = resetpass(info)
                elif opera_type == 'get_wj_list':  # 获取问卷列表
                    response = getWjList(info, username)
                elif opera_type == 'search_user':  #搜索用户
                    response = searchuser(info, username)
                elif opera_type == 'get_users_list':  # 获取用户列表
                    response = getUsersList(info, username)
                elif opera_type == 'ban_wj':  # 修改用户权限
                    response = banwj(info, username)
                elif opera_type == 'delete_wj':  # 删除问卷
                    response = deleteWj(info, username)
                elif opera_type == 'exit':
                    response = exit(request)

                else:
                    response['code'] = '-7'
                    response['msg'] = '请求类型有误'
            else:
                response['code'] = '-3'
                response['msg'] = '确少必要参数'
    else:
        response['code']='-1'
        response['msg']='请求方式有误'
    return HttpResponse(json.dumps(response))


def loginCheck(request):
    response = {'code': 0, 'msg': 'success'}
    # 查询django_session中是否有username，查询失败抛出异常
    # 查询成功判断username是否为空，若为空，返回404错误，不为空，返回成功信息
    try:
        adminname = request.session.get('adminname')
    except:
        response['code']='-4'
        response['msg']='操作失败'
    else:
        if adminname:
            response['data']={'admin':adminname}
        else:
            response['code'] = '404'
            response['msg'] = '未登录'
    return response

def getUsersList(info,username):
    response = {'code': 0, 'msg': 'success'}
    if username != '':
        obj = User.objects.all().order_by('username')
        detail = []
        for item in obj:
            temp = {}
            temp['username'] = item.username
            temp['email'] = item.email
            temp['status'] = item.status
            detail.append(temp)
        response['data'] = {'detail': detail}
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

def searchuser(info,username):
    response = {'code': 0, 'msg': 'success'}
    username = info.get('username')
    print(username)
    if username != '':
        obj = User.objects.filter(username=username)
        detail = []
        for item in obj:
            temp = {}
            temp['username'] = item.username
            temp['email'] = item.email
            temp['status'] = item.status
            detail.append(temp)
        response['data'] = {'detail': detail}
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

############################################################
#功能：获取问卷列表
#最后更新：2019-05-27
############################################################
def getWjList(info,username):
    response = {'code': 0, 'msg': 'success'}
    if username != '':
        obj = Wj.objects.all().order_by('id')
        detail=[]
        for item in obj:
            temp={}
            temp['id']=item.id
            temp['title']=item.title
            temp['username'] = item.username
            temp['desc']=item.desc
            temp['status']=item.status
            detail.append(temp)

        response['data']={'detail':detail}

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response
############################################################
#功能：删除问卷
#最后更新：2019-05-23
############################################################
def deleteWj(info,username):
    response = {'code': 0, 'msg': 'success'}
    id = info.get('id')#问卷id
    if id:
        try:
            Wj.objects.filter(id=id).delete()#删除问卷
            obj=Question.objects.filter(wjId=id)#查询所有关联问题
            for item in obj:
                Options.objects.filter(questionId=item.id).delete()#删除问题关联的选项
            obj.delete()#删除问卷所有关联问题

            Submit.objects.filter(wjId=id).delete()#删除该问卷的提交信息
            Answer.objects.filter(wjId=id).delete()#删除该问题的所有回答
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

def banwj(info,username):
    response = {'code': 0, 'msg': 'success'}
    username = info.get('username')
    email = info.get('email')
    status = info.get('status')

    try:
        if status == 0:
            User.objects.filter(email=email).update(status=1)
        else:
            User.objects.filter(email=email).update(status=0)

    except:
        response['code'] = '-4'
        response['msg'] = '操作失败'
    return response
############################################################
#功能：获取问题列表
#最后更新：2019-05-27
############################################################
def getQuestionList(info,username):
    response = {'code': 0, 'msg': 'success'}
    wjId=info.get('wjId')#wjid
    if username:
        res=Wj.objects.filter(id=wjId,username=username)
        if res.exists():#判断该问卷id是否为本人创建
            obj=Question.objects.filter(wjId=wjId)
            detail=[]
            for item in obj:
                temp={}
                temp['title']=item.title
                temp['type']=item.type
                temp['id']=item.id#问题id
                temp['row']=item.row
                temp['must']=item.must
                #获取选项
                temp['options']=[]
                if temp['type'] in ['radio', 'checkbox']:  # 如果是单选或者多选
                    optionItems = Options.objects.filter(questionId=item.id)
                    for optionItem in optionItems:
                        temp['options'].append({'title': optionItem.title, 'id': optionItem.id})
                temp['radioValue']=-1#接收单选框的值
                temp['checkboxValue'] =[]#接收多选框的值
                temp['textValue']=''#接收输入框的值
                detail.append(temp)
            response['detail']=detail
        else:
            response['code'] = '-6'
            response['msg'] = '权限不足'

    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


############################################################
#功能：删除问题
#最后更新：2019-05-23
############################################################
@transaction.atomic
def deleteQuestion(info,username):
    response = {'code': 0, 'msg': 'success'}
    questionId=info.get('questionId')
    if questionId and username:
        try:
            s_wjId=Question.objects.get(id=questionId).wjId#该题目所属的问卷id
            s_username=Wj.objects.get(id=s_wjId).username#该题目所属的用户名
            if username==s_username:#该题目是此用户创建的 有权限删除
                Question.objects.filter(id=questionId).delete()#删除问题
                Options.objects.filter(questionId=questionId).delete()#删除关联选项
            else:#该题目不是此用户创建的 无权限删除
                response['code'] = '-6'
                response['msg'] = '权限不足'
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


############################################################
#功能：登录
#最后更新：2019-05-28
############################################################
def login(info,request):
    response = {'code': 0, 'msg': 'success'}
    username = info.get('username')  #用户名
    password = info.get('password')  #密码
    if username and password:
        try:
            # 根据前台传回的用户名查找密码和用户状态
            # 若查询失败，抛出异常错误
            # 若查询成功，判断密码是否正确和用户状态是否正常
            t_password = User.objects.get(username=username).password
            t_status = User.objects.get(username=username).status
        except:
            response['code'] = '-5'
            response['msg'] = '不存在该用户'
        else:
            if password==t_password and 0==t_status:
                request.session["username"]= username
                return response
            else:
                response['code'] = '-4'
                response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response


def adminlogin(info,request):
    response = {'code': 0, 'msg': 'success'}
    username = info.get('username')  #用户名
    password = info.get('password')  #密码
    if username and password:
        try:
            # 根据前台传回的用户名查找密码和用户状态
            # 若查询失败，抛出异常错误
            # 若查询成功，判断密码是否正确和用户状态是否正常
            t_password = Adminn.objects.get(adminname=username).adminpassword

        except:
            response['code'] = '-5'
            response['msg'] = '不存在该用户'
        else:
            if password==t_password:
                request.session["adminname"]= username
                return response
            else:
                response['code'] = '-4'
                response['msg'] = '操作失败'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

############################################################
#功能：退出登录
#最后更新：2019-05-28
############################################################
def exit(request):
    response = {'code': 0, 'msg': 'success'}
    # 对django_session中的用户名执行删除操作
    # 若删除成功，返回成功信息
    # 若删除失败，抛出异常操作失败
    try:
        del request.session['username']
    except:
        response['code'] = '-4'
        response['msg'] = '操作失败'
    else:
        return response
    return response



############################################################
#功能：注册
#最后更新：2019-05-29
############################################################
def register(info):
    response = {'code': 0, 'msg': 'success'}
    t_username = info.get('username') #用户名
    t_password = info.get('password') #密码
    if t_username and t_password:  #用户名和密码不为空时，执行操作
        #将用户名和密码，以及初始状态status=0插入数据库中
        #若插入失败，抛出异常操作失败
        #若插入成功，返回成功信息
        try:
            User.objects.create(username=t_username,password=t_password)
        except:
            response['code'] = '-4'
            response['msg'] = '操作失败'
        else:
            return response
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response

############################################################
#功能：重置密码
#最后更新：2019-05-28
############################################################
def resetpass(info):
    response = {'code': 0, 'msg': 'success'}
    username = info.get('username') #用户名
    email = info.get('email') #邮箱
    if username and email:#用户名和邮箱不为空，执行操作
        #根据用户名查询对应邮箱是否正确
        #若正确，返回成功信息，若不正确，抛出异常
        try:
            t_email = User.objects.get(username=username).email
        except:
            response['code'] = '-5'
            response['msg'] = '不存在该用户'
        else:
            if email==t_email:
                return response
            else:
                response['code'] = '-10'
                response['msg'] = '未绑定邮箱'
    else:
        response['code'] = '-3'
        response['msg'] = '确少必要参数'
    return response