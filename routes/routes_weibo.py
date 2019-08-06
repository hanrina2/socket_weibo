from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):

    # if 'id' in request.query:
    #   user_id = int(request.query['id'])
    #   u = User.one(id=user_id)
    # else:
    #   u = current_user(request)

    weibos = Weibo.all()
    return html_response('weibo_index.html', weibos=weibos)


def add(request):
    u = current_user(request)
    form = request.form()
    Weibo.add(form, u.id)
    # 处理好新的数据，重定向到首页，可以看到新增数据
    return redirect('/weibo/index')


def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    # 删除该微博下的所有对应评论
    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        c.delete(c.id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query['id'])
    w = Weibo.one(id=weibo_id)
    return html_response('weibo_edit.html', weibo=w)


def update(request):
    form = request.form()
    Weibo.update(**form)
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    form = request.form()
    Weibo.comment_add(form, u.id)
    return redirect('/weibo/index')


def comment_delete(request):
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    return redirect('/weibo/index')


def comment_edit(request):
    comment_id = int(request.query['id'])
    c = Comment.one(id=comment_id)
    log('comment_edit', c)
    return html_response('comment_edit.html', comment=c)


def comment_update(request):
    form = request.form()
    Comment.update(**form)

    return redirect('/weibo/index')

# 判断用户登录权限
def weibo_owner_required(route_function):

    def f(request):
        log('weibo_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.one(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f

# 判断是否是同一个weibo用户的权限
def comment_owner_required(route_function):
    def f(request):
        log('comment_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.form()['id']
        c = Comment.one(id=int(comment_id))

        if c.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f

# 判断是否是同一个weibo用户或者评论用户的权限
def comment_owner_or_weibo_owner_required(route_function):
    def f(request):
        log('comment_owner_or_weibo_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.form()['id']
        c = Comment.one(id=int(comment_id))
        w = Weibo.one(id=c.weibo_id)

        if u.id == c.user_id or u.id == w.user_id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def route_dict():
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        '/weibo/index': login_required(index),
        '/comment/add': login_required(comment_add),
        '/comment/delete': login_required(comment_owner_or_weibo_owner_required(comment_delete)),
        '/comment/edit': login_required(comment_owner_required(comment_edit)),
        '/comment/update': login_required(comment_owner_required(comment_update)),
    }
    return d
