from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def testData (request) :
    if request.method == 'POST' :
        return HttpResponse(request.body)
    return HttpResponse('Please Post.')

def gg (request) :
    #Generate Graph
    return render(request, 'gg.html', {'GGData':' fuckyou!!! '})