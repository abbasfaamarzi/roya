from django.shortcuts import render


def index(request):
    """Demo page exercising several Roya components."""
    return render(request, 'royaapp/index.html')
