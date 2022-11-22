from django.shortcuts import render

def contacts(request, *args, **kwargs):
    return render(request, 'contacts/contacts.html',{})
