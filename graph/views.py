from django.shortcuts import render
from .models import node, edge
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import nodeForm, newnodeForm

# Create your views here.

DEBUG = True

"""
send
HnoNode
checkLogin
url: nodenotfound
"""

def send (*wargs) :
    pass

def checkLogin (request) :
    if DEBUG :
        return True
    else :
        return request.user.is_authenticated()

def checkArgs (args) :
    for word in ['id', 'name', 'isusr', 'uid'] :
        if word in args :
            args.pop(word)

def addNode (uid, name, isusr = False, **kwargs) :
    checkArgs(kwargs)
    return node.objects.create(uid=uid,name=name,isusr=isusr,**kwargs)

def queryNode (id = "", name = "", isusr = "", uid = "") :
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
    if len(queryNode(id=id)) == 1 :
        checkArgs(kwargs)
        node.objects.filter(id=id).update(**kwargs)
        return 1
    else :
        return -1

def removeNode (id) :
    r = node.objects.filter(id=id).count()
    edge.objects.filter(pntid=id).delete()
    edge.objects.filter(chdid=id).delete()
    node.objects.filter(id=id).delete()
    return r

def mergeNode (id1, id2) :
    if node.objects.filter(id=id1).count() == 1 and node.objects.filter(id=id2).count() == 1 :
        node.objects.filter(id=id2).update(node.objects.get(id=id1).__args__())
        node.objects.filter(id=id1).update(node.objects.get(id=id2).__args__())
        edge.objects.filter(pntid=id2).update(pntid=id1)
        edge.objects.filter(chdid=id2).update(chdid=id1)
        node.objects.filter(id=id2).delete()
        return 1
    else :
        return -1

def addEdge (uid, pntid, chdid, beginDate, endDate) :
    cnt = 0
    pnt = list(node.objects.filter(id=pntid))
    chd = list(node.objects.filter(id=chdid))
    if len(pnt) == 1 and len(chd) == 1 :
        if uid != pnt[0].uid :
            cnt = cnt + 1
        if uid != chd[0].uid :
            cnt = cnt + 1
        eid = edge.objects.create(pntid=pntid, chdid=chdid, beginDate=beginDate, endDate=endDate, cnt=cnt).id
        if uid != pnt[0].uid :
            send(pnt[0].uid, eid)
        if uid != chd[0].uid :
            send(chd[0].uid, eid)
        return 1
    else :
        return -1

def queryEdge (id = "", pntid = "", chdid = "", visit = True) :
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
    if edge.objects.filter(id=id).count() == 1 :
        cnt = edge.objects.get(id=id).cnt
        node.objects.filter(id=id).update(cnt=cnt-1)
        return 1
    else :
        return -1

def removeEdge (id) :
    ft = edge.objects.filter(id=id)
    r = ft.count()
    ft.delete()
    return r


def HnoNode() :
    return HttpResponse('No such person!')

def Hprofile (request, id) :
    if not checkLogin(request) :
        return HttpResponseRedirect(reverse('users:login'))
    r = queryNode(id=id)
    if len(r) != 1 :
        return HnoNode()
    r[0].__dict__.pop('id')
    vf = nodeForm(initial=r[0].__dict__)
    return render(request, 'profile.html', {'vf': vf, 'id': id})

def HaddNode (request) :
    if not checkLogin(request) :
        return HttpResponseRedirect(reverse('users:login'))
    ac = 0
    if request.method == 'POST' :
        ac = -1
        nf = newnodeForm(request.POST)
        if nf.is_valid() :
            ac = 1
            nf = nf.cleaned_data
            id = addNode(uid=request.user.id, **nf).id
            return HttpResponseRedirect(reverse('graph:profile', args=[id]))
    vf = newnodeForm()
    return render(request, 'addv.html', {'vf':vf, 'ac':ac})

def HeditNode (request, id) :
    if not checkLogin(request) :
        return HttpResponseRedirect(reverse('users:login'))
    nd = queryNode(id=id)
    if len(nd) != 1 :
        return HnoNode()
    if not DEBUG and request.user.id != nd[0].uid :
        ac = -1
        return HttpResponseRedirect(reverse('graph:profile', args=[id]))
    ac = 0
    if request.method == 'POST' :
        ac = -1
        nf = nodeForm(request.POST)
        if nf.is_valid() :
            ac = 1
            nf = nf.cleaned_data
            checkArgs(nf)
            updateNode(id, **nf)
            return HttpResponseRedirect(reverse('graph:profile', args=[id]))
    print(nd[0].__dict__)
    vf = nodeForm(initial=nd[0].__dict__)
    return render(request, 'edit.html', {'vf':vf, 'id':id})



def tmp (request) :
    addNode(1,'p1')
    addNode(1,'p2')
    return HttpResponse('<br/>'.join(str(i) for i in queryNode()))