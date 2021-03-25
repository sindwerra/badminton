import json
from django.http import HttpResponse, JsonResponse



from account.models import User

# 注册新的用户
def register(request):
    if request.method == "POST":
        if not request.POST.get('code'):
            code = 205
            msg = '没有code！'
            data=[]
        else:
            nickname = request.POST.get('nickname')
            avatarUrl = request.POST.get('avatar')
            is_manager = request.POST.get('is_manager')
            cur_user = User.objects.filter(nickname=nickname).first()
            if cur_user:
                print('已经注册过了哦~')
                is_manager = cur_user.is_manager
                code = 201
                data = {
                    'nickname': nickname,
                    'is_manager': is_manager
                }
                msg = '已经注册过了哦！'
            else:
                newUser = User()

                newUser.user_avatarurl = avatarUrl
                newUser.nickname = nickname

                newUser.is_manager = is_manager
                try:
                    newUser.save()
                    print('新用户注册成功！')
                    data = {
                        'nickname': nickname,
                        'is_manager': is_manager
                    }
                    code = 200
                    msg = '新用户注册成功'
                except Exception as e:
                    print('error', e)  # 打印错误
                    code = 202
                    data = {}
                    msg = '注册失败！'
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")


# 获取用户的个人资料
def get_user_profile(request):
    if request.method == "POST":
        print(request.POST)
        nickname = request.POST.get('nickname')
        if_exist = User.objects.filter(nickname=nickname)
        if if_exist and len(if_exist)>0:
            cur_user = if_exist[0]
            code = 200
            msg = '找到该用户，并获取个人资料'
            data = {
                'nickname' : cur_user.nickname,
                'user_avatarurl' : cur_user.user_avatarurl,
                'user_id': cur_user.user_id,
                'is_manager': cur_user.is_manager,
            }
        else:
            code = 201
            msg = '未找到该用户，无法获取资料'
            data = []
        result = {"code": code, "msg": msg, "data": data}
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
    return HttpResponse(json.dumps(result), content_type="application/json")


# 更改用户的管理员权限
def change_authority(request):
    if request.method == "POST":
        print(request.POST)
        nickname = request.POST.get('nickname')
        is_manager = request.POST.get('is_manager')

        cur_user = User.objects.filter(nickname=nickname).first()
        if cur_user :
            code = 200
            msg = '找到该用户，并更新个人资料'
            if str(is_manager) == '0':
                cur_user.is_manager = '1'
            elif str(is_manager) == '1':
                cur_user.is_manager = '0'
            cur_user.save()
            data = {
                'nickname': cur_user.nickname,
                'user_avatarurl': cur_user.user_avatarurl,
                'user_id': cur_user.user_id,
                'is_manager': cur_user.is_manager,
            }
        else:
            code = 201
            msg = '未找到用户'
            data = []
        result = {"code": code, "msg": msg, "data": data}
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
    return HttpResponse(json.dumps(result), content_type="application/json")

