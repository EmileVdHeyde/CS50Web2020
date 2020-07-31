

from django.shortcuts import render , redirect 
from . import util
from django import forms 


import re 
import markdown2 as md
import random

#This function shows the index page , by reading the name of md files in the entries folder 
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#This function allows any name to be added in url bar , and when it matches of list it takes user to that page. 
def title(request, name):
    ls=list(util.list_entries())
    if name in ls:
        return render(request, "encyclopedia/title.html",{
        "title_valid": name in ls 
        ,"title": name 
        , "bodyMD": md.markdown(util.get_entry(name))})
    else:
        return render(request, "encyclopedia/title.html",{
        "title_valid": name in ls ,
        "title": name})

#This allows the search text to be parsed and go to the topic page, if not it goes to a search results page
def search(request):
    ls=list(util.list_entries())
    ls_lower=[x.lower() for x in ls]
    name=request.POST.get("q")
    name=name.lower()
    if name in ls_lower:
        return render(request, "encyclopedia/title.html",{
        "title_valid": name in ls_lower 
        ,"title": name 
        , "bodyMD": md.markdown(util.get_entry(name))})
    else:
        entries=list()
        for s in range(0,len(ls)):
            if re.search(name,ls_lower[s]):
                entries.append(ls[s])
        return render (request,"encyclopedia/search.html",{
            "entries": entries
        })


# This item creates the Django Form that is used in add new 
class newentryform(forms.Form): 
    title=forms.CharField(label='title')
  # content=forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    content=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":300}))
    

# This function takes the user to a add new page where they can update a new entry. 
def addnew(request):
    ls=list(util.list_entries())
    ls_lower=[x.lower() for x in ls]
    if request.method == "POST" : 
        title=request.POST.get('title')
        title=title.lower().strip()  #trailing blank correction 
        content=request.POST.get('content')
        if title in ls_lower:
             message='Entry already exists'
             return render(request, "encyclopedia/addnew.html",{"form":newentryform(), 'message':message       
             })
        else:
            util.save_entry(title.capitalize() ,content) #was forcing lower case 
            return redirect('title',name=title.capitalize())

    else:
        return render(request, "encyclopedia/addnew.html",{"form":newentryform()})


#this form only allows editing in teh body 
class editentryform(forms.Form): 
    content=forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":300}))
    

## This function Allows edit of existing page
#it must populate the existing text in the body                     "bodyMD": md.markdown(util.get_entry(name)
#it must populate the existing name in the body (Not allow edit)    "title": name      //can we get it from the button we just pushed
#when clicking submit it must overwrite the file                     util.save_entry(title,content)
#lastly it myst take the user back to title page with the new content  ??? redirect('title',name=title)

def edit(request,name):
    if request.method == "POST":
        content=request.POST.get('content') 
        util.save_entry(name,content)
        return redirect('title',name=name)
    else:
        form=editentryform()
        form.fields['content'].initial=util.get_entry(name)
        return render(request, "encyclopedia/edit.html",{"form":form, "title":name})


#This function selects a random item in the list of page names, and displays that page. 
#do not need to parse the paramater
def randomselect(request):
    ls=list(util.list_entries())
    name=random.choice(ls) 
    return redirect('title',name=name)





