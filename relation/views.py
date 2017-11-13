from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from relation.models import Vertex, Edge
import datetime

class VertexForm (forms.Form) :
    #Required VertexForm
    username = forms.CharField(label='姓名', max_length=100)
    email = forms.CharField(label='邮箱', max_length=100)

class VertexFormNr (forms.Form) :
    #VertexForm
    username = forms.CharField(label='姓名', max_length=100, required=False)
    email = forms.CharField(label='邮箱', max_length=100, required=False)

class EdgeForm (forms.Form) :
    pntid = forms.IntegerField(label='导师id')
    chdid = forms.IntegerField(label='学生id')
    beginDate = forms.DateField(label='开始时间', initial=datetime.date.today)
    endDate = forms.DateField(label='结束时间', initial=datetime.date.today)

class StudentIDForm (forms.Form) :
    id = forms.IntegerField(label='id')

def checkLogin (request) :
    email = request.COOKIES.get('email', '')
    return bool(email)

def qv (username = "", email = "", id = "") :
    #query Vertex
    args = {}
    if username :
        args['username__exact'] = username
    if email :
        args['email__exact'] = email
    if id :
        args['id__exact'] = id
    return Vertex.objects.filter(**args)

def qe (pntid = "", chdid = "") :
    #query Edge
    args = {}
    if pntid :
        args['pntid__exact'] = pntid
    if chdid :
        args['chdid__exact'] = chdid
    return Edge.objects.filter(**args)

def addVertex (request) :
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = 1 : success, 0 : Get, -1 : error
    ac = 0
    if request.method == 'POST' :
        ac = -1
        vf = VertexForm(request.POST)
        if vf.is_valid() :
            #Get data
            isUsr = False
            username = vf.cleaned_data['username']
            email = vf.cleaned_data['email']
            #Insert
            Vertex.objects.create(isUsr=isUsr, username=username, email=email)
            #Success
            ac = 1
    vf = VertexForm()
    return render(request, 'addv.html', {'vf': vf, 'ac': ac})

def addEdge (request) :
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = 1 : success, 0 : Get, -1 : error
    ac = 0
    if request.method == 'POST' :
        ac = -1
        ef = EdgeForm(request.POST)
        if ef.is_valid() :
            #Get data
            pntid = ef.cleaned_data['pntid']
            chdid = ef.cleaned_data['chdid']
            beginDate = ef.cleaned_data['beginDate']
            endDate = ef.cleaned_data['endDate']
            #Check exist
            if qv(id = pntid) and qv(id = chdid) :
                #Insert
                Edge.objects.create(pntid=pntid, chdid=chdid, beginDate=beginDate, endDate=endDate)
                ac = 1
    ef = EdgeForm()
    return render(request, 'adde.html', {'ef': ef, 'ac': ac})

def queryID (request) :
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = 1 : success, 0 : Get, -1 : error (not exist)
    ac = 0
    #data : [[username, email, uid]]
    data = []
    if request.method == 'POST' :
        ac = -1
        vf = VertexFormNr(request.POST)
        if vf.is_valid() :
            #Get data
            username = vf.cleaned_data['username']
            email = vf.cleaned_data['email']
            ids = qv (username, email)
            #Check exist
            if len(ids) :
                data = [[id.username, id.email, id.id] for id in ids]
                ac = 1
    vf = VertexFormNr()
    return render(request, 'qid.html', {'vf': vf, 'ac': ac, 'data': data})

def queryEdge (request) :
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = 1 : success, 0 : Get, -1 : error
    ac = 0
    #data = [[[username, email, begindate, enddate]], [[username, email, begindate, enddate]]] ( [pnt,chd] )
    data = []
    if request.method == 'POST' :
        ac = -1
        id = StudentIDForm(request.POST)
        if id.is_valid() :
            stu = qv(id = id.cleaned_data['id'])
            if stu :
                #Pnt
                data = [[[pt.username, pt.email, rel.beginDate, rel.endDate] for rel in qe(chdid = stu[0].id) for pt in qv(id = rel.pntid)]]
                #Chd
                data.append([[ch.username, ch.email, rel.beginDate, rel.endDate] for rel in qe(pntid = stu[0].id) for ch in qv(id = rel.chdid)])
                ac = 1
    pf = StudentIDForm()
    return render(request, 'qe.html', {'pf': pf, 'ac': ac, 'data': data})


def main (request) :
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    return render(request, 'gao.html')