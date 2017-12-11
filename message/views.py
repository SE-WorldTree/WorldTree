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
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    ac = 0
    if request.method == 'POST' :
        pass
    ms = list(message.objects.filter(uid = request.user.id))
    return render(request, 'message.html', {'message': ms, 'ac': ac})

def HacMessage (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    ms = message.objects.filter(id = id, uid = request.user.id)
    if ms.count() == 1 :
        graph.views.updateEdge(ms[0].eid)
        ms.delete()
    return HttpResponseRedirect(reverse('message:message'))

def HwaMessage (request, id) :
    if not ACMeow_DEBUG() :
        if not request.user.is_authenticated() :
            return HttpResponseRedirect(reverse('users:login'))
        if request.user.node_id < 0 :
            return HttpResponseRedirect(reverse('graph:newNode'))
    message.objects.filter(id=id, uid=request.user.id).delete()
    return HttpResponseRedirect(reverse('message:message'))
