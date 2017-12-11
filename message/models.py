from django.db import models

# Create your models here.

class message (models.Model) :
    uid = models.IntegerField()
    op = models.IntegerField()
    eid = models.IntegerField()

    def __str__ (self) :
        return "%d,%d,%d"%(self.uid,self.op,self.eid)