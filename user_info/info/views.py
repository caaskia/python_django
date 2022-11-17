from django.shortcuts import render

def get_client_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    return render(request, 'info/info.html', {'ip_address': ip})
