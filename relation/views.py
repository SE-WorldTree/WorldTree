from django.shortcuts import render
from django import forms
from django.http import HttpResponse
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
    # no used ###
    return True

def qv (username = "", email = "", id = "") :
    args = {}
    if username :
        args['username__exact'] = username
    if email :
        args['email__exact'] = email
    if id :
        args['id__exact'] = id
    return Vertex.objects.filter(**args)

def qe (pntid = "", chdid = "") :
    args = {}
    if pntid :
        args['pntid__exact'] = pntid
    if chdid :
        args['chdid__exact'] = chdid
    return Edge.objects.filter(**args)

def addVertex (request) :
    if not checkLogin(request) :
        return HttpResponse('Operation denied. Please login first.')
    if request.method == 'POST' :
        vf = VertexForm(request.POST)
        if vf.is_valid() :

            isUsr = False #vf.cleaned_data['isUsr']
            username = vf.cleaned_data['username']
            email = vf.cleaned_data['email']

            Vertex.objects.create(isUsr=isUsr, username=username, email=email)
            return HttpResponse('Add vertex success')
    vf = VertexForm()
    return render(request, 'addv.html', {'vf': vf})

def addEdge (request) :
    if not checkLogin(request) :
        return HttpResponse('Operation denied. Please login first.')
    if request.method == 'POST' :
        ef = EdgeForm(request.POST)
        if ef.is_valid() :

            pntid = ef.cleaned_data['pntid']
            chdid = ef.cleaned_data['chdid']
            beginDate = ef.cleaned_data['beginDate']
            endDate = ef.cleaned_data['endDate']

            if qv(id = pntid) and qv(id = chdid) :
                Edge.objects.create(pntid=pntid, chdid=chdid, beginDate=beginDate, endDate=endDate)
                return HttpResponse('Add edge success')
            else :
                return HttpResponse('No such person')
    ef = EdgeForm()
    return render(request, 'adde.html', {'ef': ef})

def queryID (request) :
    if not checkLogin(request) :
        return HttpResponse('Operation denied. Please login first.')
    if request.method == 'POST' :
        vf = VertexFormNr(request.POST)
        if vf.is_valid() :

            username = vf.cleaned_data['username']
            email = vf.cleaned_data['email']
            ids = qv (username, email)
            if len(ids) < 1 :
                return HttpResponse('No such person')
            else : # Unique result : Return a table
                res = '<table> \n' + '\n'.join('<tr> <td> Username = %s </td> <td> Email = %s </td> <td> UserID = %d </td> </tr>'%(id.username, id.email, id.id) for id in ids) + '</table> \n'
                return HttpResponse(res)
    vf = VertexFormNr()
    return render(request, 'qid.html', {'vf': vf})

def queryEdge (request) :
    if not checkLogin(request) :
        return HttpResponse('Operation denied. Please login first.')
    if request.method == 'POST' :
        id = StudentIDForm(request.POST)
        if id.is_valid() :
            stu = qv(id = id.cleaned_data['id'])
            if stu :
                respnt = '<table> \n' + '\n'.join('<tr> <td> Username = %s </td> <td> Email = %s </td> <td> BeginDate = %s </td> <td> EndDate = %s </td> </tr>'%(pt.username, pt.email, rel.beginDate, rel.endDate) for rel in qe(chdid = stu[0].id) for pt in qv(id = rel.pntid)) + '</table>'
                reschd = '<table> \n' + '\n'.join('<tr> <td> Username = %s </td> <td> Email = %s </td> <td> BeginDate = %s </td> <td> EndDate = %s </td> </tr>'%(pt.username, pt.email, rel.beginDate, rel.endDate) for rel in qe(pntid = stu[0].id) for pt in qv(id = rel.chdid)) + '</table>'
                res = '导师：<br>' + respnt + '<br>学生：<br>' + reschd
                return HttpResponse(res)
        return HttpResponse('No such person')
    pf = StudentIDForm()
    return render(request, 'qe.html', {'pf': pf})




def main (request) :
    if not checkLogin(request) :
        return HttpResponse('Operation denied. Please login first.')
    return render(request, 'gao.html')