from django.shortcuts import render

# Create your views here.
def handler_404(request, exception):
    return render(request, "handler/error404.html", status=404)

def handler_500(request, *args, **argv):
    return render(request, "handler/error500.html", status=500)