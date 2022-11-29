# from django.shortcuts import render
from django.views.generic import TemplateView

# def contacts(request, *args, **kwargs):
#     tel = '8-800-708-19-45'
#     email = 'sales@company.com'
#     return render(request, 'contacts/contacts.html',{'tel': tel, 'email': email})

class Contacts(TemplateView):
    template_name = 'contacts/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tel'] = '8-800-708-19-45'
        context['email'] = 'sales@company.com'
        return context
