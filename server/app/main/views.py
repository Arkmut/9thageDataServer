from bson.json_util import dumps, loads

import logging
import django
from django.shortcuts import render, redirect
from .models import *
from .utils.object_viewer import *
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, JsonResponse)

logger_view = logging.getLogger(__name__)


def get_csrf_token(request):
    token = django.middleware.csrf.get_token(request)
    return JsonResponse({'token': token})


def army_list(request):
    try:
        armies = get_armybooks()
        res = dumps(armies)
        return HttpResponse(res, content_type="application/json")
    except Exception as e:
        logger_view.error(e)
        return HttpResponse("[]", content_type="application/json")


def create_army(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        logger_view.info(f"add army: {name} {version}")
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=405)
        add_army(name, version)
        return HttpResponse(dumps(get_army(name, version)[0]), content_type="application/json")


def get_army(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        logger_view.info(f"get army: {name} {version}")
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=405)
        return HttpResponse(dumps(mongo_models.get_army(name, version)[0]), content_type="application/json")


def save_army(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        logger_view.info(f"save army: {name} {version}")
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=405)
        mongo_models.save_army(name, version, body["army"])
        return HttpResponse("{}", content_type="application/json")
