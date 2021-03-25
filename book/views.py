import json, logging
from django.http import HttpResponse

from book.models import SiteInfo, BookInfo

logger = logging.getLogger(__name__)

# 管理员-发布新的场地信息
def add_siteinfo(request):
    if request.method == "POST":
        manager_id = request.POST.get('manager_id')
        limit_number = request.POST.get('limit_number')
        title_book = request.POST.get('title_book')
        time_book = request.POST.get('time_book')
        site_book = request.POST.get('site_book')
        zone_book = request.POST.get('zone_book')
        payment_method = request.POST.get('payment_method')
        siteinfo_sign = str(zone_book) + str(site_book) + ' ' + str(time_book)
        logger.info('下面准备发布新的场地信息')
        logger.info(request.POST)
        if_exist = SiteInfo.objects.filter(siteinfo_sign=siteinfo_sign)
        data = {
            'manager_id': request.POST.get('manager_id'),
            'limit_number': request.POST.get('limit_number'),
            'remaining_places': request.POST.get('limit_number'),
            'title_book': request.POST.get('title_book'),
            'time_book': request.POST.get('time_book'),
            'site_book': request.POST.get('site_book'),
            'zone_book': request.POST.get('zone_book'),
            'payment_method': request.POST.get('payment_method'),
            'siteinfo_sign': siteinfo_sign,
        }
        if if_exist.exists():
            code = 201
            msg = '不可以创建重复的场地信息哦'
        else:
            code = 200
            msg = 'successfully'
            siteinfo = SiteInfo()
            siteinfo.limit_number = limit_number
            siteinfo.remaining_places = limit_number
            siteinfo.title_book = title_book
            siteinfo.time_book = time_book
            siteinfo.site_book = site_book
            siteinfo.zone_book = zone_book
            siteinfo.payment_method = payment_method
            siteinfo.siteinfo_sign = siteinfo_sign
            siteinfo.manager_id = manager_id
            try:
                siteinfo.save()
                logger.info('场地信息发布成功')
            except Exception as e:
                msg = '场地信息未发布成功'
                logger.info(e)
                logger.info(msg)
                result = {"code": code, "msg": msg, "data": data}
                return HttpResponse(json.dumps(result), content_type="application/json")
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")

# 用户查询所有的场地信息
def get_all_siteinfo(request):
    if request.method == "GET":
        logger.info('下面查询所有的场地信息')
        all_siteinfo = SiteInfo.objects.all()
        data = []
        if all_siteinfo and len(all_siteinfo) > 0:
            code = 200
            msg = 'successfully'
            for siteinfo in all_siteinfo:
                data_ = {
                    'limit_number': siteinfo.limit_number,
                    'title_book': siteinfo.title_book,
                    'time_book': siteinfo.time_book,
                    'site_book': siteinfo.site_book,
                    'zone_book': siteinfo.zone_book,
                    'payment_method': siteinfo.payment_method,
                    'siteinfo_sign': siteinfo.siteinfo_sign,
                    'remaining_places': siteinfo.remaining_places,
                }
                data.append(data_)
            logger.info(data)
        else:
            code = 201
            msg = '未找到场地信息'
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用GET请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")

# 用户————获取所有未满的场地信息
def get_all_notfull_siteinfo(request):
    if request.method == "GET":
        logger.info('下面查询所有的场地信息')
        all_siteinfo = SiteInfo.objects.all()
        data = []
        if all_siteinfo and len(all_siteinfo) > 0:
            code = 200
            msg = 'successfully'
            for siteinfo in all_siteinfo:
                data_ = {
                    'limit_number': siteinfo.limit_number,
                    'title_book': siteinfo.title_book,
                    'time_book': siteinfo.time_book,
                    'site_book': siteinfo.site_book,
                    'zone_book': siteinfo.zone_book,
                    'payment_method': siteinfo.payment_method,
                    'siteinfo_sign': siteinfo.siteinfo_sign,
                    'remaining_places': siteinfo.remaining_places,
                }
                if int(siteinfo.limit_number)>0:
                    data.append(data_)
            logger.info(data)
        else:
            code = 201
            msg = '未找到场地信息'
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用GET请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")



# 用户预约场地
def book_siteinfo(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_avatarurl = request.POST.get('user_avatarurl')
        nickname = request.POST.get('nickname')
        siteinfo_sign = request.POST.get('siteinfo_sign')
        logger.info('下面准备预约场地')
        logger.info(request.POST)
        if_exist = SiteInfo.objects.filter(siteinfo_sign=siteinfo_sign)
        data = []
        if if_exist.exists():
            # 查看剩余名额——>按照还未使用的来计算
            siteinfo = if_exist[0]
            remaining_number = int(siteinfo.limit_number)
            if remaining_number > 0:
                # 保存预约信息
                if_book = BookInfo.objects.filter(siteinfo_sign=siteinfo_sign,user_nickname=nickname)
                if if_book and len(if_book) > 0:
                    code = 203
                    msg = '您已经提交过申请了，请等待审核'
                else:
                    code = 200
                    msg = '预约场地已提交申请'
                    bookinfo = BookInfo()
                    bookinfo.user_id = user_id
                    bookinfo.user_avatarurl = user_avatarurl
                    bookinfo.user_nickname = nickname
                    bookinfo.siteinfo_sign = siteinfo_sign
                    bookinfo.bookinfo_status = '1'
                    bookinfo.bookinfo_sign = nickname + siteinfo_sign
                    data = {
                        'user_id': request.POST.get('user_id'),
                        'nickname': request.POST.get('nickname'),
                        'siteinfo_sign': request.POST.get('siteinfo_sign'),
                        'limit_number': siteinfo.limit_number,
                    }
                    try:
                        bookinfo.save()
                        logger.info('预约场地已提交申请')
                    except Exception as e:
                        logger.info(e)
                        logger.info('提交申请失败')
                        code = 204
                        msg = '提交申请失败'
                        result = {"code": code, "msg": msg, "data": data}
                        return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                code = 201
                msg = '该场地名额已满'
        else:
            code = 202
            msg = '未找到要预约的场地'
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")

# 用户————查询总预约次数——不论是否成功
def all_booked(request):
    if request.method == "POST":
        user_nickname = request.POST.get('user_nickname')
        logger.info('下面查询用户总预约的次数')
        logger.info(request.POST)
        all_bookinfo = BookInfo.objects.filter(user_nickname=user_nickname)
        data = []
        code = 200
        if all_bookinfo and len(all_bookinfo) > 0:
            for bookinfo in all_bookinfo:
                data_ = {
                    'bookinfo_sign': bookinfo.bookinfo_sign,
                    'siteinfo_sign': bookinfo.siteinfo_sign,
                    'user_nickname': bookinfo.user_nickname,
                    'user_id': bookinfo.user_id,
                    'user_avatar': bookinfo.user_avatar,
                    'bookinfo_status': bookinfo.bookinfo_status,
                }
                data.append(data_)
        msg = str(len(data))
        # 这里不需要说明未找到时候的请求，因为查询不到说明没有信息，返回空列表，表示预约成功次数为0
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")


# 管理员————查看所有的申请信息
def all_new_bookinfo(request):
    if request.method == "GET":
        logger.info('下面查询所有待处理的预约申请')
        logger.info(request.POST)
        all_bookinfo = BookInfo.objects.filter(bookinfo_status='1')
        data = []
        if all_bookinfo.exists():
            code = 200
            msg = 'successfully'
            for bookinfo in all_bookinfo:
                siteinfo = SiteInfo.objects.filter(siteinfo_sign=bookinfo.siteinfo_sign).first()
                data_ = {
                    'bookinfo_sign': bookinfo.bookinfo_sign,
                    'siteinfo_sign': bookinfo.siteinfo_sign,
                    'user_nickname': bookinfo.user_nickname,
                    'user_id': bookinfo.user_id,
                    'user_avatar': bookinfo.user_avatar,
                    'bookinfo_status': bookinfo.bookinfo_status,
                    'book_title': siteinfo.title_book,
                    'remaining_places': siteinfo.remaining_places
                }
                data.append(data_)
        else:
            code = 201
            msg = '未找到新的预约信息'
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用GET请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")

# 管理员————通过或拒绝一个申请
def change_bookinfo_status(request):
    if request.method == "POST":
        bookinfo_sign = request.POST.get('bookinfo_sign')
        # 想修改的状态
        next_status = request.POST.get('next_status')
        logger.info('以下为POST请求的所有参数')
        logger.info(request.POST)
        if_exist = BookInfo.objects.filter(bookinfo_sign=bookinfo_sign)
        if if_exist.exists():
            logger.info('找到了正在申请的信息')
            bookinfo = if_exist[0]
            if (int(next_status) == 2):
                siteinfo = SiteInfo.objects.filter(siteinfo_sign=bookinfo.siteinfo_sign).first()
                if(siteinfo.remaining_places > 0):
                    siteinfo.remaining_places = siteinfo.remaining_places - 1
                    siteinfo.save()
                    bookinfo.bookinfo_status = next_status
                    bookinfo.save()
                    code = 200
                    msg = '通过成功，下面是更新之后预约申请的信息'
                else:
                    code = 201
                    msg = '失败，已满，下面是更新之后预约申请的信息'
            else:
                code = 200
                msg = '拒绝成功，下面是更新之后预约申请的信息'
            data = {
                'bookinfo_sign': bookinfo.bookinfo_sign,
                'siteinfo_sign': bookinfo.siteinfo_sign,
                'user_nickname': bookinfo.user_nickname,
                'user_id': bookinfo.user_id,
                'user_avatar': bookinfo.user_avatar,
                'bookinfo_status': next_status,
            }
            result = {"code": code, "msg": msg, "data": data}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            code = 202
            msg = '没找到要修改的预约信息'
            data = {}
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")


# 用户————查看自己预约成功的总次数
def all_pass(request):
    if request.method == "POST":
        user_nickname = request.POST.get('user_nickname')
        logger.info('下面查询用户预约成功的次数')
        logger.info(request.POST)
        all_bookinfo = BookInfo.objects.filter(user_nickname=user_nickname, bookinfo_status='2')
        data = []
        code = 200
        if all_bookinfo.exists():
            for bookinfo in all_bookinfo:
                data_ = {
                    'bookinfo_sign': bookinfo.bookinfo_sign,
                    'siteinfo_sign': bookinfo.siteinfo_sign,
                    'user_nickname': bookinfo.user_nickname,
                    'user_id': bookinfo.user_id,
                    'user_avatar': bookinfo.user_avatar,
                    'bookinfo_status': bookinfo.bookinfo_status,
                }
                data.append(data_)
        msg = str(len(data))
        # 这里不需要说明未找到时候的请求，因为查询不到说明没有信息，返回空列表，表示预约成功次数为0
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")


# 用户————查看某个场地的详细信息
def get_siteinfo_getdetail(request):
    if request.method == "POST":
        siteinfo_sign = request.POST.get('siteinfo_sign')
        if_exist = SiteInfo.objects.filter(siteinfo_sign=siteinfo_sign)
        if if_exist.exists():
            # 查看剩余名额——>按照还未使用的来计算
            siteinfo = if_exist[0]
            code = 200
            msg = 'successfully'
            # 保存预约信息
            data = {
                'limit_number': siteinfo.limit_number,
                'title_book': siteinfo.title_book,
                'time_book': siteinfo.time_book,
                'site_book': siteinfo.site_book,
                'zone_book': siteinfo.zone_book,
                'payment_method': siteinfo.payment_method,
                'siteinfo_sign': siteinfo.siteinfo_sign,
                'remaining_places': siteinfo.remaining_places
            }
        else:
            code = 202
            msg = '未找到要预约的场地'
            data = []
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")


# 管理员————查看所有自己发布的场地信息
def get_all_my_siteinfo(request):
    if request.method == "POST":
        logger.info('下面查询所有的场地信息')
        manager_id = request.POST.get('manager_id')
        all_siteinfo = SiteInfo.objects.filter(manager_id=manager_id)
        data = []
        if all_siteinfo.exists():
            code = 200
            msg = 'successfully'
            for siteinfo in all_siteinfo:
                data_ = {
                    'limit_number': siteinfo.limit_number,
                    'title_book': siteinfo.title_book,
                    'time_book': siteinfo.time_book,
                    'site_book': siteinfo.site_book,
                    'zone_book': siteinfo.zone_book,
                    'payment_method': siteinfo.payment_method,
                    'siteinfo_sign': siteinfo.siteinfo_sign,
                    'remaining_places': siteinfo.remaining_places
                }
                if int(siteinfo.limit_number)>0:
                    data.append(data_)
            logger.info(data)
        else:
            code = 201
            msg = '未找到场地信息'
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")


# 用户————查看自己预约过的场地信息
def get_my_bookinfo(request):
    if request.method == "POST":
        user_nickname = request.POST.get('user_nickname')
        if_exist = BookInfo.objects.filter(user_nickname=user_nickname)
        if if_exist.exists():
            code = 200
            msg = 'successfully'
            data = []
            for bookinfo in if_exist:
                siteinfo = SiteInfo.objects.filter(siteinfo_sign=bookinfo.siteinfo_sign).first()
                status = ''
                if bookinfo.bookinfo_status == '1':
                    status = '预约中'
                elif bookinfo.bookinfo_status == '2':
                    status = '已参加'
                elif bookinfo.bookinfo_status == '3':
                    status = '已被拒绝'
                # 保存预约信息
                data_ = {
                    'limit_number': siteinfo.limit_number,
                    'title_book': siteinfo.title_book,
                    'time_book': siteinfo.time_book,
                    'site_book': siteinfo.site_book,
                    'zone_book': siteinfo.zone_book,
                    'payment_method': siteinfo.payment_method,
                    'siteinfo_sign': siteinfo.siteinfo_sign,
                    'remaining_places': siteinfo.remaining_places,
                    'status': status
                }
                data.append(data_)
        else:
            code = 202
            msg = '未找到要预约的场地'
            data = []
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")


# 用户————查看自己在某个场地预约成功的总次数
def all_pass_bysite(request):
    if request.method == "POST":
        user_nickname = request.POST.get('user_nickname')
        siteinfo = request.POST.get('siteinfo')
        siteinfo = str(siteinfo).split(' ')[0]
        logger.info('下面查询用户在这个场地预约成功的次数')
        logger.info(request.POST)
        all_bookinfo = BookInfo.objects.filter(user_nickname=user_nickname, bookinfo_status='2')
        data = []
        code = 200
        if all_bookinfo.exists():
            for bookinfo in all_bookinfo:
                if bookinfo.siteinfo_sign.split(' ')[0] == siteinfo:
                    data_ = {
                        'bookinfo_sign': bookinfo.bookinfo_sign,
                        'siteinfo_sign': bookinfo.siteinfo_sign,
                        'user_nickname': bookinfo.user_nickname,
                        'user_id': bookinfo.user_id,
                        'user_avatar': bookinfo.user_avatar,
                        'bookinfo_status': bookinfo.bookinfo_status,
                    }
                    data.append(data_)
        msg = str(len(data))
        # 这里不需要说明未找到时候的请求，因为查询不到说明没有信息，返回空列表，表示预约成功次数为0
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用POST请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")

# 用户————查看所有具体场地的历史发布信息次数
def count_bysite(request):
    if request.method == "GET":
        all_siteinfo_ = SiteInfo.objects.all()
        sitelist = []
        data = []
        code = 200
        msg = 'success'
        if all_siteinfo_.exists():
            for siteinfo in all_siteinfo_:
                detaillocation = siteinfo.zone_book + siteinfo.site_book
                sitelist.append(detaillocation)
        sitelist = list(set(sitelist))
        for sitelocation in sitelist:
            number = 0
            all_siteinfo = SiteInfo.objects.all()
            for siteinfo in all_siteinfo:
                if siteinfo.zone_book+siteinfo.site_book == sitelocation:
                    number += 1
            data_ = {
                'number': number,
                'location': sitelocation,
            }
            data.append(data_)
        # 这里不需要说明未找到时候的请求，因为查询不到说明没有信息，返回空列表，表示预约成功次数为0
        result = {"code": code, "msg": msg, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {"code": 500, "msg": 'failed', "data": '请使用GET请求'}
        return HttpResponse(json.dumps(result), content_type="application/json")
