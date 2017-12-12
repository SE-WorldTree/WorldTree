from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import message
import graph.views

# Create your views here.

def ACMeow_DEBUG () :
    return False

def sendMessage (uid, eid, op) :
    message.objects.create(uid=uid, eid=eid, op=op)

def hasMessage (uid) :
    return message.objects.filter(uid=uid).count() > 0

def Hmessage (request) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    ac = 0
    if request.method == 'POST' :
        pass
    ms = list(message.objects.filter(uid = request.user.id))
    r = []
    print(len(ms))
    for m in ms :
        e = graph.views.queryEdge(id=m.eid, visit=False)
        if len(e) < 1 :
            continue
        e = e[0]
        args = {}
        if m.op == 1 :
            args['ms'] = '让 %s 成为 %s 的导师 (%d -> %d)'%(graph.views.queryNode(id=e.pntid)[0].name, graph.views.queryNode(id=e.chdid)[0].name, e.beginDate, e.endDate)
        else :
            args['ms'] = '取消 %s 作为 %s 的导师 (%d -> %d)'%(graph.views.queryNode(id=e.pntid)[0].name, graph.views.queryNode(id=e.chdid)[0].name, e.beginDate, e.endDate)
        args['acl'] = reverse('message:acm',args=[m.id])#+'?id='+str(m.id)
        args['wal'] = reverse('message:wam',args=[m.id])#+'?id='+str(m.id)
        r.append(args.copy())
    return render(request, 'message.html', {'data': r})

def HacMessage (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    ms = message.objects.filter(id = id, uid = request.user.id)
    if ms.count() == 1 :
        if ms[0].op == 1 :
            graph.views.updateEdge(ms[0].eid)
        else :
            graph.views.removeEdge(ms[0].eid)
        ms.delete()
    return HttpResponseRedirect(reverse('message:message'))

def HwaMessage (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    message.objects.filter(id=id, uid=request.user.id).delete()
    return HttpResponseRedirect(reverse('message:message'))
