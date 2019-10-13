from django.shortcuts import render, redirect
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
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('delete from class where id=%s', nid)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')


def edit_class(request):
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
