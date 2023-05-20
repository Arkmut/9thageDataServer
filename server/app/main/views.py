import logging

from django.shortcuts import render, redirect
from .models import *
from .utils.object_viewer import *
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)

logger_view = logging.getLogger(__name__)


def dashboard(request):
    return render(request, "base.html")


def army_list(request):
    try:
        armies = get_armybooks()
        print(armies)
        return render(request, "main/army_list.html", {"armies": [ObjectViewer(a) for a in armies]})
    finally:
        return render(request, "main/army_list.html", {"armies": []})


def army_edit(request, name, version):
    army = list(get_army(name, version))[0]
    return render(request, "main/army_edit.html", {"army": ObjectViewer(army)})


def create_army(request):
    name = request.GET.get("name", "")
    version = request.GET.get("version", "")
    if name == "" or version == "":
        return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=405)
    add_army(name, version)
    get_army(name, version)
    logger_view.info("BBBBBBBBBBBBBBBBBBBBBB")

    return redirect(f"/army_list/{name}/{version}/")
