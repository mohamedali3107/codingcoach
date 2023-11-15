from django.shortcuts import render

# Create your views here.

def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "dashboard/index.html")