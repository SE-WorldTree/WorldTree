from django.db import models
from django import forms

class nodeForm (forms.Form) :
    name = forms.CharField(label='姓名', max_length=50, required=False, disabled=True)

    email = forms.EmailField(label='邮箱', max_length=50, required=False)
    nickname = forms.CharField(label='昵称', max_length=50, required=False)
    blog = forms.CharField(label='博客', max_length=50, required=False)
    linkedin = forms.CharField(label='领英', max_length=50, required=False)
    ggsc = forms.CharField(label='谷歌学术', max_length=50, required=False)

class newnodeForm (forms.Form) :
    name = forms.CharField(label='姓名', max_length=50, required=True)

    email = forms.EmailField(label='邮箱', max_length=50, required=False)
    nickname = forms.CharField(label='昵称', max_length=50, required=False)
    blog = forms.CharField(label='博客', max_length=50, required=False)
    linkedin = forms.CharField(label='领英', max_length=50, required=False)
    ggsc = forms.CharField(label='谷歌学术', max_length=50, required=False)
