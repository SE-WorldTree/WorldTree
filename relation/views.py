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
    if username == None or email == None or id == None :
        return None
    args = {}
    if username :
        args['username__exact'] = username
    if email :
        args['email__exact'] = email
    if id :
        args['id__exact'] = id
    return Vertex.objects.filter(**args)

def qe (pntid = "", chdid = "", id = "") :
    #query Edge
    if pntid == None or chdid == None or id == None :
        return None
    args = {}
    if pntid :
        args['pntid__exact'] = pntid
    if chdid :
        args['chdid__exact'] = chdid
    if id :
        args['id__exact'] = id
    return Edge.objects.filter(**args)

def addVertex (request) :
    #Add vertex
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
            if username and email :
                #Insert
                Vertex.objects.create(isUsr=isUsr, username=username, email=email)
                #Success
                ac = 1
    vf = VertexForm()
    return render(request, 'addv.html', {'vf': vf, 'ac': ac})

def addEdge (request) :
    #Add edge
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
            if pntid and chdid and beginDate and endDate :
                #Check exist
                if qv(id = pntid) and qv(id = chdid) :
                    #Insert
                    Edge.objects.create(pntid=pntid, chdid=chdid, beginDate=beginDate, endDate=endDate)
                    ac = 1
    ef = EdgeForm()
    return render(request, 'adde.html', {'ef': ef, 'ac': ac})

def queryID (request) :
    #Get vertex :: data = [vertex]
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = 1 : success, 0 : Get, -1 : error (not exist)
    ac = 0
    data = []
    if request.method == 'POST' :
        ac = -1
        vf = VertexFormNr(request.POST)
        if vf.is_valid() :
            #Get data
            username = vf.cleaned_data['username']
            email = vf.cleaned_data['email']
            data = qv (username, email)
            #Check exist
            if len(data) :
                ac = 1
    vf = VertexFormNr()
    return render(request, 'qid.html', {'vf': vf, 'ac': ac, 'data': data})

def queryEdge (request) :
    #Get edge :: data = [ [ (pnt, rel) ] , [ (chd, rel) ] ]
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = 1 : success, 0 : Get, -1 : error
    ac = 0
    data = []
    if request.method == 'POST' :
        ac = -1
        id = StudentIDForm(request.POST)
        if id.is_valid() :
            stu = qv(id = id.cleaned_data['id'])
            if stu :
                #Pnt
                data = [[(pt, rel) for rel in qe(chdid = stu[0].id) for pt in qv(id = rel.pntid)]]
                #Chd
                data.append([(ch, rel) for rel in qe(pntid = stu[0].id) for ch in qv(id = rel.chdid)])
                ac = 1
    pf = StudentIDForm()
    return render(request, 'qe.html', {'pf': pf, 'ac': ac, 'data': data})

def vertexDetail (request) :
    #Get vertex detail (graph generation) :: data = vertex
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = -1 : no suck person, 0 : not a query, 1 : success
    ac = -1
    res = []
    if request.method == 'GET' :
        id = request.GET.get('id')
        if id != None :
            res = qv(id = id)
            if res :
                ac = 1
    elif request.method == 'POST' :
        id = request.POST.get('id')
        if id != None :
            res = qv(id = id)
            if res :
                ac = 1
    return render(request, 'vertexDetail.html', {'ac': ac, 'data': res[0]})

def edgeDetail (request) :
    #Get edge detail (graph generation) :: data = (edge, pnt, chd)
    #Login check
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #ac = -1 : no suck edge, 0 : not a query, 1 : success
    ac = -1
    res = []
    pntdata = []
    chddata = []
    if request.method == 'GET' :
        id = request.GET.get('id')
        if id != None :
            res = qe(id = id)
            if res :
                ac = 1
    elif request.method == 'POST' :
        id = request.POST.get('id')
        if id != None :
            res = qe(id = id)
            if res :
                ac = 1
    if ac == 1 :
        pntdata = qv(id = res[0].pntid)
        chddata = qv(id = res[0].chdid)
        if pntdata and chddata :
            ac = 1
        else :
            ac = -1
    return render(request, 'edgeDetail.html', {'ac': ac, 'data': (res[0], pntdata[0], chddata[0])})

def main (request) :
    if not checkLogin(request) :
        return HttpResponseRedirect('/login/')
    return render(request, 'gao.html')