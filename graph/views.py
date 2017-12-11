from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import node, edge
from .forms import nodeForm, newnodeForm, edgeForm
from users.models import User
from message.views import sendMessage as send, hasMessage, ACMeow_DEBUG


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
send
HnoNode
checkLogin
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
        return HttpResponseRedirect(reverse('users:login'))
    if needU and request.user.id < 0 :
        return HttpResponseRedirect(reverse('graph:newNode'))
    return True
"""

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

def existNode (id) :
    return node.objects.filter(id=id).count() == 1

def mergeNode (id1, id2) :
    if node.objects.filter(id=id1).count() == 1 and node.objects.filter(id=id2).count() == 1 :
        node.objects.filter(id=id2).update(node.objects.get(id=id1).__args__())
        node.objects.filter(id=id1).update(node.objects.get(id=id2).__args__())
        edge.objects.filter(pntid=id2).update(pntid=id1)
        edge.objects.filter(chdid=id2).update(chdid=id1)
        edge.objects.filter(pntid=id1, chdid=id1).delete() # self loop
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
            send(pnt[0].uid, eid, 1)
        if uid != chd[0].uid :
            send(chd[0].uid, eid, 1)
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
        if cnt == 0 :
            edge.objects.filter(id=id).delete()
        else :
            edge.objects.filter(id=id).update(cnt=cnt-1)
        return 1
    else :
        return -1

def removeEdge (id) :
    ft = edge.objects.filter(id=id)
    r = ft.count()
    ft.delete()
    return r



def Hprofile (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
        if hasMessage(request.user.id) :
            return HttpResponseRedirect(reverse('message:getMessage'))
    r = queryNode(id=id)
    if len(r) != 1 :
        return HnoNode()
    r[0].__dict__.pop('id')
    vf = nodeForm(initial=r[0].__dict__)

    pntedge = queryEdge(chdid = id)
    pnt = [queryNode(id=eg.pntid)[0] for eg in pntedge]
    chdedge = queryEdge(pntid = id)
    chd = [queryNode(id=eg.chdid)[0] for eg in chdedge]
    broedge = [eg for pntid in [i.id for i in pnt] for eg in queryEdge(pntid = pntid)]
    bro = [queryNode(id=eg.chdid)[0] for eg in broedge]

    # json

    return render(request, 'profile.html', {'vf': vf, 'id': id})

def HaddNode (request) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
        if hasMessage(request.user.id) :
            return HttpResponseRedirect(reverse('message:getMessage'))
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

def HnewNode (request) :
    if not ACMeow_DEBUG() and not request.user.is_authenticated() :
        return HttpResponseRedirect(reverse('users:login'))
    ac = 0
    if request.method == 'POST' :
        ac = -1
        nf = newnodeForm(request.POST)
        if nf.is_valid() :
            ac = 1
            nf = nf.cleaned_data
            id = addNode(uid=request.user.id, isusr=True, **nf).id
            User.objects.filter(id = request.user.id).update(node_id = id)
            return HttpResponseRedirect(reverse('graph:profile', args=[id]))
    vf = newnodeForm()
    return render(request, 'addv.html', {'vf':vf, 'ac':ac})

def HeditNode (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
        if hasMessage(request.user.id) :
            return HttpResponseRedirect(reverse('message:getMessage'))
    nd = queryNode(id=id)
    if len(nd) != 1 :
        return HnoNode()
    if not ACMeow_DEBUG() and request.user.id != nd[0].uid :
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
    #print(nd[0].__dict__)
    vf = nodeForm(initial=nd[0].__dict__)
    return render(request, 'edit.html', {'vf':vf, 'id':id, 'ac': ac})

def HremoveNode (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
        if hasMessage(request.user.id) :
            return HttpResponseRedirect(reverse('message:getMessage'))
    ac = -1
    nd = queryNode(id=id)
    if len(nd) != 1 :
        return HnoNode()
    if (not ACMeow_DEBUG() and request.user.id != nd[0].uid) or nd[0].isusr :
        return HttpResponseRedirect(reverse('graph:profile', args=[id]))
    removeNode(id)
    return HttpResponseRedirect(reverse('index'))

def HaddEdge (request) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
        if hasMessage(request.user.id) :
            return HttpResponseRedirect(reverse('message:getMessage'))
    ac = 0
    if request.method == 'POST' :
        ac = -1
        ef = edgeForm(request.POST)
        if ef.is_valid() :
            ef = ef.cleaned_data
            if ef['pntid'] != ef['chdid'] and existNode(ef['pntid']) and existNode(ef['chdid']) :
                ac = 1
                addEdge(request.user.id, **ef)
                return HttpResponseRedirect(reverse('graph:adde'))
    ef = edgeForm()
    return render(request, 'adde.html', {'ef': ef, 'ac': ac})

def HremoveEdge (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
        if hasMessage(request.user.id) :
            return HttpResponseRedirect(reverse('message:getMessage'))
    ac = -1
    eg = queryEdge(id=id)
    if len(eg) != 1 :
        return HnoEdge()
    eg = eg[0]
    if ACMeow_DEBUG() or eg.pndid == request.user.id or eg.chdid == request.user.id :
        removeEdge(id=id)
    else :
        send(eg.pntid, id, -1)
        send(eg.chdid, id, -1)
    ac = 1
    return HttpResponseRedirect(reverse('index'))

def tmp (request) :
    queryNode(id=24)[0].name='fuck'
    res = '<br/>'.join(str(i) for i in queryNode())+'<br/> <br/>'+'<br/>'.join(str(i) for i in queryEdge(visit=False))
    #res = "%d %s %s"%(request.user.node_id, str(request.user.node_id<0),str(ACMeow_DEBUG))
    res.replace('\n', '<br>')
    return HttpResponse(res)

