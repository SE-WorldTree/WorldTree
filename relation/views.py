from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from relation.models import Vertex, Edge

class VertexForm (forms.Form) :
    isUsr = forms.BooleanField()
    usrID = forms.IntegerField(label='uid')
    username = forms.CharField(label='姓名', max_length=100)
    email = forms.CharField(label='邮箱', max_length=1004)

class EdgeForm (forms.Form) :
    patid = forms.IntegerField(label='patid')
    chdid = forms.IntegerField(label='chdid')
    beginDate = forms.DateField(label='begin')
    endDate = forms.DateField(label='end')

def queryId (username = "", email = "") :
    if username == "" and email == "" :
        return Vertex.objects.filter()
    elif username == "" :
        return Vertex.objects.filter(email__ext = email)
    elif email == "" :
        return Vertex.objects.filter(username__ext = username)
    else :
        return Vertex.objects.filter(username__ext = username, email__ext = email)

def addVertex (request) :
    if request.method == 'POST' :
        vf = VertexForm(request.POST)
        if vf.is_valid() :

            isUsr = vf.cleaned_data['isUsr']
            usrID = vf.cleaned_data['usrID']
            username = vf.cleaned_data['username']
            email = vf.cleaned_data['email']

            Vertex.objects.create(isUsr=isUsr, usrID=usrID, username=username, email=email)
            return HttpResponse('Add vertex success')
    vf = VertexForm()
    return render(request, 'addv.html', {'vf': vf})

def addEdge (request) :
    if request.method == 'POST' :
        ef = EdgeForm(request.POST)
        if ef.is_valid() :

            patid = ef.cleaned_data['patid']
            chdid = ef.cleaned_data['chdid']
            beginDate = ef.cleaned_data['beginDate']
            endDate = ef.cleaned_data['endDate']

            Edge.objects.create(patid=patid, chdid=chdid, beginDate=beginDate, endDate=endDate)
            return HttpResponse('Add edge success')
    ef = EdgeForm()
    return render(request, 'adde.html', {'ef': ef})
