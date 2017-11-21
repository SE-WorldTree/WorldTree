from django.db import models
from django import forms
import datetime

class nodeForm (forms.Form) :
    name = forms.CharField(label='姓名', max_length=50, required=False, disabled=True)

    email = forms.EmailField(label='邮箱', max_length=50, required=True)
    institute = forms.CharField(label='单位', max_length=50, required=True)
    nickname = forms.CharField(label='昵称', max_length=50, required=False)
    blog = forms.CharField(label='博客', max_length=50, required=False)
    linkedin = forms.CharField(label='领英', max_length=50, required=False)
    ggsc = forms.CharField(label='谷歌学术', max_length=50, required=False)

class newnodeForm (forms.Form) :
    name = forms.CharField(label='姓名', max_length=50, required=True)

    email = forms.EmailField(label='邮箱', max_length=50, required=True)
    institute = forms.CharField(label='单位', max_length=50, required=True)
    nickname = forms.CharField(label='昵称', max_length=50, required=False)
    blog = forms.CharField(label='博客', max_length=50, required=False)
    linkedin = forms.CharField(label='领英', max_length=50, required=False)
    ggsc = forms.CharField(label='谷歌学术', max_length=50, required=False)

class edgeForm (forms.Form) :
    pntid = forms.IntegerField(label='导师', required=True)
    chdid = forms.IntegerField(label='学生', required=True)
    beginDate = forms.IntegerField(label='开始年份', required=True, initial=datetime.date.today().year, min_value=1900, max_value=datetime.date.today().year)
    endDate = forms.IntegerField(label='结束年份', required=True, initial=datetime.date.today().year, min_value=1900, max_value=datetime.date.today().year)

    def clean_chdid (self) :
        pntid = self.cleaned_data['pntid']
        chdid = self.cleaned_data['chdid']
        if pntid == chdid :
            raise forms.ValidationError('导师和学生不能为同一人', code='invalid')
        return chdid

    """def clean_beginDate (self) :
        beginDate = self.cleaned_data['beginDate']
        endDate = self.cleaned_data['endDate']
        if beginDate > endDate :
            raise forms.ValidationError('开始年份不得晚于结束年份', code='invalid')
        return beginDate"""

    def clean_endDate (self) :
        beginDate = self.cleaned_data['beginDate']
        endDate = self.cleaned_data['endDate']
        if beginDate > endDate :
            raise forms.ValidationError('结束年份不得早于开始年份', code='invalid')
        return endDate