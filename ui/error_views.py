from django.shortcuts import render


def error400_view(request):
    return render(request, 'error_pages/error400.html', status=400)


def error403_view(request):
    return render(request, 'error_pages/error403.html', status=403)


def error404_view(request):
    return render(request, 'error_pages/error404.html', status=404)


def error500_view(request):
    return render(request, 'error_pages/error500.html', status=500)