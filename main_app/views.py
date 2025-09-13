from django.http import HttpResponse

def hello_world_view(request):
    return HttpResponse("<h1>Hello World! Agar aap yeh dekh paa rahe hain, to server theek hai.</h1>")
