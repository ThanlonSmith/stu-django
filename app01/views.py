from django.shortcuts import render, redirect, HttpResponse
import pymysql


def classes(request):
    '''
    查询班级id、班级名称
    :param request:对象相关的数据
    :return:渲染后的模板
    '''
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql语句
    cursor.execute("select id,title from class")
    classes_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'classes.html', {'classes_list': classes_list})


def add_class(request):
    '''
    添加班级信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'add_class.html')
    else:
        class_title = request.POST.get('class_title')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # cursor.execute("insert into class(title) values(%s)", [class_title, ])
        cursor.execute('insert into class(title) values(%s)', class_title)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')


def del_class(request):
    '''
    删除班级信息
    :param request:
    :return:
    '''
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('delete from class where id=%s', nid)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')


def edit_class(request):
    '''
    编辑班级信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('select id,title from class where id=%s', nid)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request, 'edit_class.html', {'result': result})
    else:
        # nid = request.POST.get('nid')  # 放到请求体
        nid = request.GET.get('nid')  # 放到请求头
        title = request.POST.get('title')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('update class set title=%s where id = %s', [title, nid])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')


def students(request):
    '''
    学生列表
    :param request:封装了请求相关的所有信息
    :return:
    '''
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(
        'select student.id,student.name,class.title from  student left join class on student.class_id=class.id')
    student_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'students.html', {'student_list': student_list})


def add_student(request):
    '''
    添加学生信息
    :param request:
    :return:
    '''
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class")
        classe_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request, 'add_student.html', {'class_list': classe_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student(name,class_id) values (%s,%s)", [name, class_id, ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/students/')


def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class")
        class_list = cursor.fetchall()
        print(class_list)
        cursor.execute("select id,name,class_id from student where id=%s", nid)
        current_student_info = cursor.fetchone()
        print(current_student_info)
        cursor.close()
        conn.close()
        return render(request, 'edit_student.html',
                      {'class_list': class_list, 'current_student_info': current_student_info})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update student set name=%s,class_id=%s where id = %s", [name, class_id, nid])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/students/')


def del_student(request):
    '''
    删除学生信息
    :param request:
    :return:
    '''
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('delete from student where id=%s', nid)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/students/')


# def add_class_modal(request):
#     title = request.POST.get('title')
#     conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
#     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#     cursor.execute('insert into class (title) values (%s)', title)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return redirect('/classes/')
def add_class_modal(request):
    title = request.POST.get('title')
    if len(title) > 0:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('insert into class (title) values (%s)', title)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse('ok')
    else:
        return HttpResponse('班级不能为空！')
