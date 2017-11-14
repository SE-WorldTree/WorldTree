from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def testData (request) :
    if request.method == 'POST' :
        return HttpResponse(request.body)
    return HttpResponse('Please Post.')

def gg (request) :
    #Generate Graph
    return render(request, 'gg.html', {'vv': '1\nmeow1\n2\nmeow2\n3\nmeow3', 'ee': '1\n1\n2\n2\n2\n3\n3\n3\n1'})