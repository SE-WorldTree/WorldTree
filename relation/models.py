from django.db import models


class Vertex (models.Model) :
    """

    """
    isUsr = models.BooleanField()
    usrID = models.IntegerField()
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    def __str__ (self) :
        return self.username + "(" + self.email + ")"

class Edge (models.Model) :
    """

    """
    patid = models.IntegerField()
    chdid = models.IntegerField()
    beginDate = models.DateField()
    endDate = models.DateField()
    def __str__ (self) :
        return str(self.patid) + " -> " + str(self.chdid) + " (" + str(self.beginDate) + " ~> " + str(self.endDate) + ") "
