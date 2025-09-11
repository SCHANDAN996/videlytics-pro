from django.shortcuts import render

# Create your views here.
def home_view(request):
    # 'index.html' template ko render karega
    return render(request, 'index.html')
