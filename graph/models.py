from django.db import models

# Create your models here.

class node (models.Model) :
    # id
    name = models.CharField(max_length=50)
    isusr = models.BooleanField()
    uid = models.IntegerField()

    email = models.EmailField(max_length=50)
    nickname = models.CharField(max_length=50)
    blog = models.CharField(max_length=50)
    linkedin = models.CharField(max_length=50)
    ggsc = models.CharField(max_length=50)
    institute = models.CharField(max_length=50)


    def __args__ (self) :
        args = {}
        if self.email != "" :
            args['email'] = str(self.email)
        if self.nickname != "" :
            args['nickname'] = self.nickname
        if self.blog != "" :
            args['blog'] = self.blog
        if self.linkedin != "" :
            args['linkedin'] = self.linkedin
        if self.ggsc != "" :
            args['ggsc'] = self.ggsc
        if self.institute != "" :
            args['institute'] = self.institute
        return args

    def __cn_args__ (self) :
        args = {}
        if self.email != "" :
            args['邮箱'] = str(self.email)
        if False and self.nickname != "" :
            args['昵称'] = self.nickname
        if self.blog != "" :
            args['博客'] = self.blog
        if self.linkedin != "" :
            args['领英'] = self.linkedin
        if self.ggsc != "" :
            args['谷歌学术'] = self.ggsc
        if self.institute != "" :
            args['单位'] = self.institute
        return args

    def __value__ (self) :
        res = []
        if self.nickname == "" :
            res.append('%s'%self.name)
        else :
            res.append('%s(%s)'%(self.name,self.nickname))
        for a,b in self.__cn_args__().items() :
            if a != 'nickname' :
                res.append('%s : %s'%(a,b))
        return res

    def __str__ (self) :
        if self.nickname == "" :
            nk = ""
        else :
            nk = '(%s)'%self.nickname
        return self.name + nk + ' : %s, %s, %s, %s, %s'%(self.institute, self.email, self.blog, self.linkedin, self.ggsc)

class edge (models.Model) :
    # id
    pntid = models.IntegerField()
    chdid = models.IntegerField()
    beginDate = models.IntegerField()
    endDate = models.IntegerField()

    cnt = models.IntegerField()

    def __str__ (self) :
        if self.cnt == 0 :
            return '[%d] '%self.id + str(self.pntid) + ' ==> ' + str(self.chdid) + ' (' + str(self.beginDate) + ' ==> ' + str(self.endDate) + ')'
        else :
            return '[%d] '%self.id + str(self.pntid) + ' --> ' + str(self.chdid) + ' (' + str(self.beginDate) + ' --> ' + str(self.endDate) + ') (%d)'%self.cnt
