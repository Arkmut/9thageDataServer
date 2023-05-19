from django.shortcuts import render
from .models import *


def dashboard(request):
    return render(request, "base.html")


def army_list(request):
    try:
        armies = ArmyBook.objects.all()
        return render(request, "main/army_list.html", {"armies": armies})
    finally:
        return render(request, "main/army_list.html", {"armies": []})
