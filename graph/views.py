from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import node, edge
from .forms import nodeForm, newnodeForm, edgeForm
from users.models import User
from message.views import sendMessage as send, hasMessage, ACMeow_DEBUG
import json


"""
Hprofile (request, id) : {'vf': vf, 'id': id}
HaddNode (request) : GET:{'vf': vf, 'ac': ac} POST:reverse(profile,id) 
HnewNode (request) : GET:{'vf': vf, 'ac': ac} POST:reverse(profile,id)
HeditNode (request, id) : GET:{'vf': vf, 'id': id, 'ac': ac} POST:reverse(profile,id)
HremoveNode (request, id) : ???
HaddEdge (request) : GET:{'ef': ef, 'ac': ac} POST:reverse(adde) 
HremoveEdge (request, id) : ???
"""

# Create your views here.

"""
HnoNode
url: nodenotfound
"""

HnoNode = lambda : HttpResponse('No such person')
HnoEdge = lambda : HttpResponse('No such relation')
#send = lambda uid, eid, op : HttpResponse('Send')

"""
def checkLogin (request, needU = True) :
    if ACMeow_DEBUG() :
        return True
    if not request.user.is_authenticated() :
        return HttpResponseRedirect(reverse('login'))
    if needU and request.user.id < 0 :
        return HttpResponseRedirect(reverse('graph:newNode'))
    return True
"""

def checkArgs (args) :
    #删掉节点数据中的关键变量 (id, name, isusr, uid)
    for word in ['id', 'name', 'isusr', 'uid'] :
        if word in args :
            args.pop(word)


def addNode (uid, name, isusr = False, **kwargs) :
    #新建节点
    checkArgs(kwargs)
    return node.objects.create(uid=uid,name=name,isusr=isusr,**kwargs)

def compName (request) :
    #姓名自动补全 & 查找id
    if request.method == 'GET' :
        prename = request.GET['skeyword']
    else :
        prename = request.POST['skeyword']
    nodes = list(node.objects.filter(name__startswith=prename))
    res = [{'value':it.id, 'label':it.name, 'desc':it.__str__()} for it in nodes]
    return HttpResponse(json.dumps(res))

def queryNode (id = "", name = "", isusr = "", uid = "") :
    #根据给定信息查询满足条件的条目，返回list
    args = {}
    if id != "" :
        args['id__exact'] = id
    if name != "" :
        args['name__exact'] = name
    if isusr != "" :
        args['isusr__exact'] = isusr
    if uid != "" :
        args['uid__exact'] = uid
    return list(node.objects.filter(**args))

def updateNode (id, **kwargs) :
    #更新节点信息
    if len(queryNode(id=id)) == 1 :
        checkArgs(kwargs)
        node.objects.filter(id=id).update(**kwargs)
        return 1
    else :
        return -1

def removeNode (id) :
    #删除节点
    r = node.objects.filter(id=id).count()
    #先删除所有与其相连的边
    edge.objects.filter(pntid=id).delete()
    edge.objects.filter(chdid=id).delete()
    node.objects.filter(id=id).delete()
    return r

def existNode (id) :
    #查询节点是否存在
    return node.objects.filter(id=id).count() == 1

def mergeNode (id1, id2) :
#将两个节点合并
    if node.objects.filter(id=id1).count() == 1 and node.objects.filter(id=id2).count() == 1 :
        #若两个节点都存在：
        #先将两个节点的信息合并
        node.objects.filter(id=id2).update(node.objects.get(id=id1).__args__())
        node.objects.filter(id=id1).update(node.objects.get(id=id2).__args__())
        #将所有与id2相连的边改为与id1相连
        edge.objects.filter(pntid=id2).update(pntid=id1)
        edge.objects.filter(chdid=id2).update(chdid=id1)
        #删除产生的自环
        edge.objects.filter(pntid=id1, chdid=id1).delete() # self loop
        #删除节点id2
        node.objects.filter(id=id2).delete()
        return 1
    else :
        return -1

def addEdge (uid, pntid, chdid, beginDate, endDate) :
    #新建关系
    cnt = 0
    pnt = list(node.objects.filter(id=pntid))
    chd = list(node.objects.filter(id=chdid))
    if len(pnt) == 1 and len(chd) == 1 :
        #当父节点和子节点都唯一时：
        #检查加边权限
        if uid != pnt[0].uid :
            cnt = cnt + 1
        if uid != chd[0].uid :
            cnt = cnt + 1
        #加边，cnt记录还缺少多少授权
        eid = edge.objects.create(pntid=pntid, chdid=chdid, beginDate=beginDate, endDate=endDate, cnt=cnt).id
        #发送请求消息
        if uid != pnt[0].uid :
            send(pnt[0].uid, eid, 1)
        if uid != chd[0].uid :
            send(chd[0].uid, eid, 1)
        print(pntid,chdid)
        return 1
    else :
        return -1

def queryEdge (id = "", pntid = "", chdid = "", visit = True) :
    #查询关系
    args = {}
    if id != "" :
        args['id__exact'] = id
    if pntid != "" :
        args['pntid__exact'] = pntid
    if chdid != "" :
        args['chdid__exact'] = chdid
    if visit :
        args['cnt__exact'] = 0
    return list(edge.objects.filter(**args))

def updateEdge (id) :
    #更新关系信息。只有cnt可以更新，更新为cnt-1。该方法用于处理用户同意关系的请求
    if edge.objects.filter(id=id).count() == 1 :
        cnt = edge.objects.get(id=id).cnt
        if cnt == 0 :
            edge.objects.filter(id=id).delete()
        else :
            edge.objects.filter(id=id).update(cnt=cnt-1)
        return 1
    else :
        return -1

def removeEdge (id) :
    #删边
    ft = edge.objects.filter(id=id)
    r = ft.count()
    ft.delete()
    return r



def graph (id) :
    #绘制关系图（后端
    #获取id
    #if request.method == 'POST' :
    #    id = request.POST['id']
    #else :
    #    id = request.GET['id']
    #获取所有节点和边
    You = queryNode(id=id)[0] #你
    pntedge = list(set(queryEdge(chdid = id))) #你与父节点之间的边
    pnt = list(set([queryNode(id=eg.pntid)[0] for eg in pntedge])) #父节点
    chdedge = list(set(queryEdge(pntid = id))) #你与子节点之间的边
    chd = list(set([queryNode(id=eg.chdid)[0] for eg in chdedge])) #子节点
    broedge = list(set([eg for pntid in [i.id for i in pnt] for eg in queryEdge(pntid = pntid)])) #父节点与兄弟节点之间的边
    bro = list(set([queryNode(id=eg.chdid)[0] for eg in broedge])) #兄弟节点

    urlFormat = lambda id : str(reverse('users:profile'))+'?id='+str(id)

    #节点格式：
    def YouFormat (You) :
        #你
        return {'name': You.name,
                'url': urlFormat(You.id),
                'symbolSize': '80',
                'value': '<br/>'.join(You.__value__()),
                'label': {'normal': {'show': 'true',
                                     'textStyle': {'color': 'white',
                                                   'fontSize': 16}}},
                'itemStyle': {'normal': {'color': "#1B4869"}}}
    def PntFormat (You) :
        #父节点
        return {'name': You.name,
                'url': urlFormat(You.id),
                'symbolSize': '60',
                'value': '<br/>'.join(You.__value__()),
                'itemStyle': {'normal': {'color': "#1593A2"}}}
    def ChdFormat (You) :
        #子节点
        return {'name': You.name,
                'url': urlFormat(You.id),
                'symbolSize': '40',
                'value': '<br/>'.join(You.__value__()),
                'itemStyle': {'normal': {'color': "#FF8B00"}}}
    def BroFormat (You) :
        #兄弟节点
        return {'name': You.name,
                'url': urlFormat(You.id),
                'symbolSize': '50',
                'value': '\n'.join(You.__value__()),
                'itemStyle': {'normal': {'color': "#ACF0F1"}}}

    ren = dict() #节点在图中的id
    data = [YouFormat(You)] #图中节点
    ren[You.id] = 0
    #加入所有父节点
    for it in pnt :
        if not it.id in ren.keys() :
            ren[it.id] = len(data)
            data.append(PntFormat(it))
    #加入所有子节点
    for it in chd :
        if not it.id in ren.keys() :
            ren[it.id] = len(data)
            data.append(ChdFormat(it))
    #加入所有兄弟节点
    for it in bro :
        if not it.id in ren.keys() :
            ren[it.id] = len(data)
            data.append(BroFormat(it))

    #边格式：
    #父节点边
    def PntEdge (eg) :
        return {'source': ren[You.id],
                'target': ren[eg.pntid],
                'value': '导师 (%04d-%04d)'%(eg.beginDate,eg.endDate)}
    #子节点边
    def ChdEdge (eg) :
        return {'source': ren[You.id],
                'target': ren[eg.chdid],
                'value': '学生 (%04d-%04d)'%(eg.beginDate,eg.endDate)}
    #兄弟节点边
    def BroEdge (eg) :
        return {'source': ren[You.id],
                'target': ren[eg.chdid],
                'value': '同学'}

    links = [] #边集
    #父节点边
    for eg in pntedge :
        links.append(PntEdge(eg))
    #子节点边
    for eg in chdedge :
        links.append(ChdEdge(eg))
    #兄弟节点边
    for eg in broedge :
        links.append(BroEdge(eg))

    return {'data': json.dumps(data), 'links': json.dumps(links), 'name': You.name}

def Hprofile (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    r = queryNode(id=id)
    if len(r) != 1 :
        return HnoNode()
    r[0].__dict__.pop('id')
    vf = nodeForm(initial=r[0].__dict__)

    """
    pntedge = queryEdge(chdid = id)
    pnt = [queryNode(id=eg.pntid)[0] for eg in pntedge]
    chdedge = queryEdge(pntid = id)
    chd = [queryNode(id=eg.chdid)[0] for eg in chdedge]
    broedge = [eg for pntid in [i.id for i in pnt] for eg in queryEdge(pntid = pntid)]
    bro = [queryNode(id=eg.chdid)[0] for eg in broedge]
    """
    # json

    return render(request, 'users/profile.html', {'vf': vf, 'id': id})

def HaddNode (request) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    ac = -1
    if request.method == 'POST' :
        fuck = request.POST
    else : #GET
        fuck = request.GET
    if fuck['user_name'] != None and fuck['user_name'] != '':
        nf = {'name': fuck['user_name'],
              'email': fuck['user_email'],
              'nickname': fuck['user_nickname'],
              'blog': fuck['user_blog'],
              'linkedin': fuck['user_linked'],
              'ggsc': fuck['user_ggsc'],
              'institute': fuck['user_ins'],
              }
        addNode(uid=request.user.id, **nf)
        ac = 1
    print(ac)
    return HttpResponse(json.dumps({'ac': ac}))

def HnewNode (request) :
    if not ACMeow_DEBUG() and not request.user.is_authenticated() :
        return HttpResponseRedirect(reverse('login'))
    ac = 0
    if request.method == 'POST' :
        ac = -1
        nf = newnodeForm(request.POST)
        print(request.POST)
        if nf.is_valid() :
            nf = nf.cleaned_data
            id = addNode(uid=request.user.id, isusr=True, **nf).id
            User.objects.filter(id = request.user.id).update(node_id = id)
            ac = 1
            return HttpResponseRedirect(reverse('index'))
    vf = newnodeForm()
    return render(request, 'addv.html', {'vf':vf, 'ac':ac})

def HeditNode (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    nd = queryNode(id=id)
    if len(nd) != 1 :
        return HnoNode()
    if not ACMeow_DEBUG() and request.user.id != nd[0].uid :
        ac = -1
        return HttpResponseRedirect(reverse('users:profile', args=[id]))
    ac = 0
    if request.method == 'POST' :
        ac = -1
        nf = nodeForm(request.POST)
        if nf.is_valid() :
            ac = 1
            nf = nf.cleaned_data
            checkArgs(nf)
            updateNode(id, **nf)
            return HttpResponseRedirect(reverse('users:profile', args=[id]))
    #print(nd[0].__dict__)
    vf = nodeForm(initial=nd[0].__dict__)
    return render(request, 'edit.html', {'vf':vf, 'id':id, 'ac': ac})

def HremoveNode (request) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    ac = -1
    if request.method == 'POST' :
        id = request.POST['del_id']
    else :
        id = request.GET['del_id']
    nd = queryNode(id=id)
    if len(nd) == 1 :
        if ACMeow_DEBUG() or (request.user.id == nd[0].uid and not nd[0].isusr) :
            removeNode(id)
            ac = 1
    return HttpResponse(json.dumps({'ac': ac}))

def HaddEdge (request) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    ac = 0
    if request.method == 'POST' :
        ac = -1
        post = request.POST
        ef = {'pntid': int(request.POST['teacher_id']),
              'chdid': int(request.POST['student_id']),
              'beginDate': int(request.POST['start_year']),
              'endDate': int(request.POST['end_year'])}
        if ef['pntid'] != ef['chdid'] and existNode(ef['pntid']) and existNode(ef['chdid']) and ef['beginDate'] <= ef['endDate']:
            addEdge(request.user.id, **ef)
            ac = 1
    return HttpResponse(json.dumps({'ac': ac}))

def HremoveEdge (request) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))

    if request.method == 'POST' :
        data = request.POST
    else :
        data = request.GET
    del_s_id = data['del_s_id']
    del_t_id = data['del_t_id']
    ac = -1
    egs = queryEdge(pntid=del_s_id, chdid=del_t_id, visit=False)
    for eg in egs :
        if ACMeow_DEBUG() or eg.pndid == request.user.id or eg.chdid == request.user.id :
            removeEdge(id=id)
            ac = 1
        elif eg.cnt == 0 :
            send(eg.pntid, id, -1)
            send(eg.chdid, id, -1)
            ac = 0
    return HttpResponse(json.dumps({'ac': ac}))


def tmp (request) :
    res = '<br/>'.join(str(i.id)+str(i) for i in queryNode())+'<br/> <br/>'+'<br/>'.join(str(i) for i in queryEdge(visit=False))
    #res = "%d %s %s"%(request.user.node_id, str(request.user.node_id<0),str(ACMeow_DEBUG))
    res.replace('\n', '<br>')
    User.objects.filter(id=request.user.id).update(node_id=109)
    return HttpResponse(res)

def showgraph (request) :
    return render(request, 'users/tree.html', graph(request.GET['id']))

def tree (request) :
    return render(request, 'users/tree.html', {'id': request.GET['id']})