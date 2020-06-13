import pymysql
from django.shortcuts import render, redirect, HttpResponse
from utils import sqlhelper
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def login(request):
    '''
    用户登录
    :param request:
    :return:
    '''
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    if request.method == 'POST':
        if username == 'thanlon' and pwd == '123456':
            obj = redirect('/user/class/')
            obj.set_signed_cookie('ticket', 'thanlon', salt='123456')
            return obj
    else:
        return render(request, 'login.html')


def classes(request):
    """
    查询班级信息
    :param request:
    :return:
    """
    ticket = request.get_signed_cookie('ticket', salt='123456')
    if not ticket:
        return redirect('/login/')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    # print(class_list)
    # [{'id': 1, 'title': '软件工程'}, {'id': 3, 'title': '网络工程'}, {'id': 4, 'title': '计算机科学与技术'}]
    cursor.close()
    conn.close()
    return render(request, 'class.html', {'class_list': class_list})


def add_class(request):
    """
    添加班级信息
    :param request:
    :return:
    """
    # 如果是get请求就返回add_class.html模板就可以
    if request.method == 'GET':
        return render(request, 'add_class.html')
    # 如果是post请求则执行下面的代码
    else:
        # 获取班级的标题
        class_title = request.POST.get('class_title')
        print(class_title)
        # 创建数据库连接对象
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 将班级的名称传到sql语句中
        cursor.execute('insert into class(title) values(%s)', class_title)
        # cursor.execute("insert into class(title) values(%s)", [class_title, ])
        # 提交(查询不需要，其它如添加、修改、更新数据是需要执行commit方法才能将数据插入成功)
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 添加之后就会重定向到/classes/路由，会显示添加后的班级
        return redirect('/user/class/')


def edit_class(request):
    """
    编辑班级信息
    :param request:
    :return:
    """
    # 如果是get请求，这里额外也需要查询下数据库，把原来的信息也展示出来
    if request.method == 'GET':
        # 获取客户端传过来的班级id
        nid = request.GET.get('nid')
        # 创建数据库连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 执行游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行sql语句
        cursor.execute('select id,title from class where id=%s', nid)
        # 获取查询到的所有数据
        result = cursor.fetchone()
        # print(result)
        # {'id': 1, 'title': '软件工程'}
        # 创建游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 返回模板和数据
        return render(request, 'edit_class.html', {'result': result})
    # post请求用来修改班级信息
    else:
        # nid = request.POST.get('nid')  # 放到请求体
        nid = request.GET.get('nid')  # 放到请求头
        title = request.POST.get('title')
        # 创建数据库连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行sql语句
        cursor.execute('update class set title=%s where id = %s', [title, nid])
        # 提交事务
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        return redirect('/user/class/')


def del_class(request):
    # 获取客户端传过来的nid，我们要个根据nid来删除数据
    nid = request.GET.get('nid')
    # 创建连接对象
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql语句
    cursor.execute('delete from class where id=%s', nid)
    # 提交事务
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return redirect('/user/class/')


def student(request):
    '''
    学生信息列表
    :param request:封装了请求相关的所有信息
    :return:返回模板和数据
    '''
    # 创建连接对象
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 查询学生信息列表
    cursor.execute(
        'select student.id,student.name,class_id,class.title from  student left join class on student.class_id=class.id')
    # 获取查询到的所有数据
    student_list = cursor.fetchall()
    paginator = Paginator(student_list, 1)
    current_page = request.GET.get('page')
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e:
        posts = paginator.page(1)
    except EmptyPage as e:
        posts = paginator.page(1)
    # 查询班级信息
    cursor.execute('select id,title from class')
    # 获取查询到的所有班级列表
    class_list = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    # 返回模板和数据
    return render(request, 'student.html', {'student_list': student_list, 'class_list': class_list, 'posts': posts})


def add_student(request):
    """
    添加学生信息
    :param request:
    :return:
    """
    # 如果是get请求
    if request.method == 'GET':
        # 创建连接对象
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行查询的sql语句
        cursor.execute("select id,title from class")
        # 获取查询到的所有数据
        classe_list = cursor.fetchall()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 返回模板和数据
        return render(request, 'add_student.html', {'class_list': classe_list})
    # 如果是post请求
    else:
        # 获取学生的名字
        name = request.POST.get('name')
        # 获取学生的班级id
        class_id = request.POST.get('class_id')
        # 创建连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 将学生的名字和班级的id信息放到sql中
        cursor.execute("insert into student(name,class_id) values (%s,%s)", [name, class_id, ])
        # 执行事务
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 返回模板
        return redirect('/user/student/')


def edit_student(request):
    """
    编辑学生信息
    :param request:
    :return:
    """
    # get请求时
    if request.method == 'GET':
        # 获取传过来的学生id
        nid = request.GET.get('nid')
        # 创建连接对象
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行查询班级信息的sql
        cursor.execute("select id,title from class")
        # 获取所有班级信息
        class_list = cursor.fetchall()
        # 执行查询当前学生编号、名字和班级id的sql
        cursor.execute("select id,name,class_id from student where id=%s", nid)
        # 获取查询到的数据。因为数据只有一条，所以这里使用fetchone()就可以了
        current_student_info = cursor.fetchone()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 返回模板和数据
        return render(request, 'edit_student.html',
                      {'class_list': class_list, 'current_student_info': current_student_info})
        # post请求时
    else:
        # 从url中获取学生的id
        nid = request.GET.get('nid')
        # 从请求体(form表单)中获取当前学生的姓名
        name = request.POST.get('name')
        # 从请求体中获取当前学生的班级id
        class_id = request.POST.get('class_id')
        # 创建练级
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行sql语句
        cursor.execute("update student set name=%s,class_id=%s where id = %s", [name, class_id, nid])
        # 提交事务
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 重定向到学生信息页面
        return redirect('/user/student/')


def del_student(request):
    """
    删除学生信息
    :param request:
    :return:
    """
    # 获取学生编号
    nid = request.GET.get('nid')
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql
    cursor.execute('delete from student where id=%s', nid)
    # 提交事务
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    # 返回模板
    return redirect('/user/student/')


def add_class_modal(request):
    """
    模态对话框的方式添加班级信息
    :param request:
    :return:
    """
    # 从前台ajax提交的json字符串中{'title': $('#title').val()}获取班级名称
    title = request.POST.get('title')
    # 输入的班级名称的长度需要大于0
    # print(title)
    if len(title) > 0:
        # 创建连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行sql
        cursor.execute('insert into class (title) values (%s)', title)
        # 提交事务
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 向前台返回ok
        return HttpResponse('ok')
    else:
        # 如果提交过来的班级名称长度是小于0的,向前台返回不能为空，给前台提示信息
        return HttpResponse('班级不能为空！')


def edit_class_modal(request):
    '''
    模态对话框编辑班级信息
    '''
    # 获取班级编号
    class_id = request.GET.get('class_id')
    # 获取班级名称
    class_title = request.GET.get('class_title')
    # 获取的名称长度要大于0
    if len(class_title) > 0:
        # 创建连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行sql
        cursor.execute('update class set title=%s where id = %s', [class_title, class_id])
        # 提交事务
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        # 向前台返回的data，前台通过这里来判断编辑是否完成
        return HttpResponse('ok')
    else:
        # 返回错误提示信息
        return HttpResponse('班级不能为空！')


def del_class_modal(request):
    """
    模态对话框删除班级信息
    :param request:
    :return:
    """
    # 获取班级编号，需要通过编号删除班级信息
    class_id = request.GET.get('class_id')
    print(class_id)
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 将班级id传到sql豫剧中并执行sql
    cursor.execute('delete from class where id=%s', class_id)
    # 提交事务
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    # 返回操作成功的标识
    return HttpResponse('ok')


def add_student_modal(request):
    """
    模态对话框的方式添加班级信息
    :param request:
    :return:
    """
    ret = {'status': True, 'msg': None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        if len(name) <= 0 or len(class_id) <= 0:
            ret['status'] = False
            ret['msg'] = '学生姓名或班级不能为空'
            return HttpResponse(json.dumps(ret))
        sqlhelper.modify(sql='insert into student(name,class_id) values(%s,%s)', args=[name, class_id])
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)
    return HttpResponse(json.dumps(ret))


def edit_student_modal(request):
    """
    模态框编辑学生信息
    :param request:
    :return:
    """
    ret = {'status': True, 'msg': None}
    try:
        student_id = request.POST.get('student_id')
        class_id = request.POST.get('class_id_edit')
        student_name = request.POST.get('student_name')
        sqlhelper.modify('update student set name=%s,class_id=%s where id=%s',
                         [student_name, class_id, student_id])
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)
    return HttpResponse(json.dumps(ret))


def del_student_modal(request):
    """
    模态框删除学生信息
    :param request:
    :return:
    """
    ret = {'status': True, 'msg': None}
    try:
        student_id = request.GET.get('student_id')
        sqlhelper.modify('delete from student where id=%s', [student_id, ])
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)
    return HttpResponse(json.dumps(ret))


def add_teacher(request):
    """
    添加教师
    :param request:
    :return:
    """
    if request.method == 'GET':
        class_list = sqlhelper.get_list('select id,title from class', [])
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        name = request.POST.get('name')
        obj = sqlhelper.SqlHelper()
        teacher_id = obj.create('insert into teacher(name) values (%s)', [name, ])
        class_ids = request.POST.getlist('class_ids')  # ['1', '8', '9', '10']
        # 多次连接，多次提交
        """
        for class_id in class_ids:
            sqlhelper.modify('insert into teacher2class(teacher_id,class_id) values (%s,%s)', [teacher_id, class_id])        
        """
        # 一次连接，多次提交
        """
        for class_id in class_ids:
            obj.modify('insert into teacher2class(teacher_id,class_id) values (%s,%s)', [teacher_id, class_id])
        obj.close()
        """
        # 一次连接，一次提交
        data_list = []  # [(9, '8'), (9, '9'), (9, '10')]
        for class_id in class_ids:
            data_list.append((teacher_id, class_id))
        obj.multiple_modify('insert into teacher2class(teacher_id,class_id) values (%s,%s)', data_list)
        obj.close()
        return redirect('/user/teacher/')


def teacher(request):
    """
    查询教师和任课班级信息
    :param request:
    :return:
    """
    obj = sqlhelper.SqlHelper()
    teacher_list = obj.get_list(
        'select teacher.id as tid,teacher.name,class.title from teacher left join teacher2class on teacher.id = teacher2class.teacher_id left join class on teacher2class.class_id = class.id ;',
        [])
    """
    print(teacher_list)
    [
    {'tid': 1, 'name': '李娇', 'title': '网络工程'}, 
    {'tid': 1, 'name': '李娇', 'title': '计算机科学与技术'},
    {'tid': 1, 'name': '李娇', 'title': '软件技术'},
    {'tid': 1, 'name': '李娇', 'title': '软件工程'},
    {'tid': 2, 'name': '李晓', 'title': '网络工程'},
    {'tid': 2, 'name': '李晓', 'title': '软件工程'}
    ]
    """

    result = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid] = {'tid': row['tid'], 'name': row['name'], 'titles': [row['title'], ]}
    """
    print(ret)
    {
        1: {'tid': 1, 'name': '李娇', 'titles': ['网络工程', '计算机科学与技术', '软件技术', '软件工程']}, 
        2: {'tid': 2, 'name': '李晓', 'titles': ['网络工程', '软件工程']}
    }
    """
    return render(request, 'teacher.html', {'teacher_list': result.values(), })


def edit_teacher(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        obj = sqlhelper.SqlHelper()
        # 当前教师的信息
        teacher_info = obj.get_one('select id,name from teacher where id = %s', [nid, ])
        # 当前教师的任教班级的id信息
        class_id_list = obj.get_list('select class_id from teacher2class where teacher_id=%s', [nid, ])
        # 所有的班级信息
        class_list = obj.get_list('select id,title from class', [])
        """
        print(teacher_list) # {'id': 2, 'name': '李晓'}
        print(class_list) # [{'id': 1, 'title': '软件工程'}, {'id': 8, 'title': '软件技术'}, {'id': 9, 'title': '计算机科学与技术'}, {'id': 10, 'title': '网络工程'}]
        print(class_id_list) # [{'class_id': 1}, {'class_id': 10}]
        """
        obj.close()
        temp = []
        for item in class_id_list:
            temp.append(item['class_id'])
        """
        print(temp)  # [1, 10]
        """
        return render(request, 'edit_teacher.html',
                      {'class_list': class_list, 'teacher_info': teacher_info, 'class_id_list': temp})
    else:
        # 获取post请求的url上的参数
        nid = request.GET.get('nid')
        print(nid)
        name = request.POST.get('name')
        class_ids = request.POST.getlist('class_ids')  # ['1', '8', '9', '10']
        obj = sqlhelper.SqlHelper()
        obj.modify('update teacher set name = %s where id = %s', [name, nid])
        obj.modify('delete from teacher2class where teacher_id = %s', [nid])
        data_list = []  # [('1', '1'), ('1', '8'), ('1', '9'), ('1', '10')]
        """
        for class_id in class_ids:
            temp = (nid, class_id,)
            data_list.append(temp)
        """
        # 使用lambda表达式
        func = lambda nid, class_id: data_list.append((nid, class_id))
        for class_id in class_ids:
            func(nid, class_id)
        obj.multiple_modify('insert into teacher2class(teacher_id,class_id) values (%s,%s)', data_list)
        return redirect('/user/teacher/')


def add_teacher_modal(request):
    """
    AJAX的方式添加教师信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        obj = sqlhelper.SqlHelper()
        class_list = obj.get_list('select id,title from class', [])
        import time
        # 这里是用来模拟用户网站压力比较大的情况下
        time.sleep(0.2)
        obj.close()
        return HttpResponse(json.dumps(class_list))
    if request.method == 'POST':
        ret = {'status': True, 'msg': None}
        # 一般ajax请求要加上try
        try:
            name = request.POST.get('name')
            class_ids = request.POST.getlist('class_ids')  # ['1', '8', '9', '10']
            # print(name,class_ids) #奈何 ['9', '10']
            obj = sqlhelper.SqlHelper()
            teacher_id = obj.create('insert into teacher(name) values (%s) ', [name, ])
            data_list = []
            func = lambda item: data_list.append((teacher_id, item))
            for item in class_ids:
                func(item)
            # print(data_list)  # [(8, '8'), (8, '10')]
            obj.multiple_modify('insert teacher2class(teacher_id,class_id) values(%s,%s)', data_list)
            obj.close()
        except Exception as e:
            ret['status'] = False
            ret['msg'] = '处理失败!'
        return HttpResponse(json.dumps(ret))


def del_teacher_modal(request):
    """
    AJAX的方式删除教师信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        ret = {'status': True, 'msg': None}
        try:
            obj = sqlhelper.SqlHelper()
            tid = request.GET.get('teacher_id')
            obj.modify('delete from teacher where id =%s', [tid])
            obj.modify('delete from teacher2class where teacher_id = %s', [tid])
            obj.close()
        except Exception as e:
            ret['status'] = False
            ret['msg'] = "删除失败！"
        return HttpResponse(json.dumps(ret))
