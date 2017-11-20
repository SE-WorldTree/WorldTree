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

    def __args__ (self) :
        args = []
        if self.email != "" :
            args['email'] = self.email
        if self.nickname != "" :
            args['nickname'] = self.nickname
        if self.blog != "" :
            args['blog'] = self.blog
        if self.linkedin != "" :
            args['linkedin'] = self.linkedin
        if self.ggsc != "" :
            args['ggsc'] = self.ggsc
        return args

    def __str__ (self) :
        if self.nickname == "" :
            return '[%d] '%self.id + self.name + ' : ' + self.email
        else :
            return '[%d] '%self.id + self.name + '(' + self.nickname + ') : ' + self.email

class edge (models.Model) :
    # id
    pntid = models.IntegerField()
    chdid = models.IntegerField()
    beginDate = models.DateField()
    endDate = models.DateField()

    cnt = models.IntegerField()

    def __str__ (self) :
        if self.cnt == 0 :
            return '[%d] '%self.id + str(self.pntid) + ' ==> ' + str(self.chdid) + ' (' + str(self.beginDate) + ' ==> ' + str(self.endDate) + ')'
        else :
            return '[%d] '%self.id + str(self.pntid) + ' --> ' + str(self.chdid) + ' (' + str(self.beginDate) + ' --> ' + str(self.endDate) + ') (%d)'%self.cnt
