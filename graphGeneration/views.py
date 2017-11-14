from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def testData (request) :
    if request.method == 'POST' :
        return HttpResponse(request.body)
    return HttpResponse('Please Post.')

def gg (request) :
    #Generate Graph
    #Format:
    #  vv : uid \n username \n
    #  ee : eid \n pntuid \n chduid \n
    return render(request, 'gg.html', {'vv': '1\nmeow3\n2\nmeow1\n3\nmeow2', 'ee': '1\n2\n3\n2\n3\n1\n3\n1\n2'})