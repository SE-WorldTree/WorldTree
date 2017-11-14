from django.shortcuts import render
from django.http import HttpResponse
import relation.views as rel_views
from django.http import HttpResponseRedirect

# Create your views here.

def gg (request) :
    #Generate Graph
    #Login check
    if not rel_views.checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #Format:
    #  vv : uid \n username \n
    #  ee : eid \n pntuid \n chduid \n
    vv = '\n'.join('\n'.join([str(it.id), it.username]) for it in rel_views.qv())
    ee = '\n'.join('\n'.join([str(rel.id), str(rel.pntid), str(rel.chdid)]) for rel in rel_views.qe())
    return render(request, 'gg.html', {'vv': vv, 'ee': ee})

def ggwp (request) :
    #Generate Graph from someone
    #Login check
    if not rel_views.checkLogin(request) :
        return HttpResponseRedirect('/login/')
    #Format:
    vid = request.GET.get('id')
    #  vv : uid \n username \n
    #  ee : eid \n pntuid \n chduid \n
    vv = '\n'.join('\n'.join([str(it.id), it.username]) for it in rel_views.qv() if str(it.id) == vid or rel_views.qe(chdid = it.id, pntid = vid) or rel_views.qe(chdid = vid, pntid = it.id))
    ee = ['\n'.join([str(rel.id), str(rel.pntid), str(rel.chdid)]) for rel in rel_views.qe(pntid = vid)] + ['\n'.join([str(rel.id), str(rel.pntid), str(rel.chdid)]) for rel in rel_views.qe(chdid = vid)]
    ee = '\n'.join(ee)
    return render(request, 'gg.html', {'vv': vv, 'ee': ee})