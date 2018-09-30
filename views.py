from django.shortcuts import render
from .queryproc import *

#This file will input response from html and will connect our python programs
#schedule the home page
def index(request):
     return render(request, 'personal/index1.html')

#schedule the search details page
def search(request, tosearch):

    query = request.GET.get('tosearch',None)    #tosearch is the textbox field name in html
    try:
        newq = call_func(query)
        return render(request, 'personal/index2.html', {'newq':newq})
    except (TypeError,ValueError):
        pass

#Schedule our relevance feedback page
def relevance(request, reldoc, reldoc1):

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['editbox1']
    else:
        docname = request.GET.get('reldoc')     #reldoc is the texbox field name in html
        new_reldoc = relevance_feedback(docname)

    return render(request, 'personal/index3.html', {'new_reldoc':new_reldoc})
