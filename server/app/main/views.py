from bson.json_util import dumps, loads

import logging
import django
from django.shortcuts import render, redirect

from .latex_exporter.army_book_exporter import export_armybook
from .models import *
from .models.sql_models import PublicArmy
from .utils.object_viewer import *
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, JsonResponse, FileResponse)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Max

logger_view = logging.getLogger(__name__)

GLOBAL_TRANSLATION_NAME = "global_translation"


def get_csrf_token(request):
    token = django.middleware.csrf.get_token(request)
    return JsonResponse({'token': token})


def army_list(request):
    try:
        userKnown = request.user.is_authenticated
        publicArmies = {}
        for ar in PublicArmy.objects.all():
            logger_view.info(f"ar: {ar}")
            publicArmies[ar.name] = ar.version
        armies = get_armybooks(userKnown, publicArmies)
        if not userKnown:
            valid_armies = []
            logger_view.info("public", publicArmies)
            for a in armies:
                logger_view.info("a", a['name'], a['version'])
                if a['name'] in publicArmies and a['version'] == publicArmies[a['name']]:
                    valid_armies.append(a)
            armies = valid_armies

        res = dumps({"armies": armies, "publicArmies": publicArmies})
        return HttpResponse(res, content_type="application/json")
    except Exception as e:
        logger_view.error(e)
        return HttpResponse("{'armies':[],'publicArmies':{}}", content_type="application/json")


@login_required(login_url='/login/')
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
        return HttpResponse(dumps(mongo_models.get_army(name, version)[0]), content_type="application/json")


def get_army(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        userKnown = request.user.is_authenticated
        if not userKnown:
            armies = PublicArmy.objects.filter(name=name, version=version)
            if len(armies) == 0:
                return HttpResponseBadRequest(f"You need to be logged in to see this", status=401)
        logger_view.info(f"get army: {name} {version}")
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=405)
        return HttpResponse(dumps(mongo_models.get_army(name, version)[0]), content_type="application/json")


@login_required(login_url='/login/')
def save_army(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        armies = PublicArmy.objects.filter(name=name, version=version)
        if len(armies) > 0:
            return HttpResponseBadRequest(f"You can't modify a public army", status=401)
        logger_view.info(f"save army: {name} {version}")
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=405)
        army = body["army"]
        validation = army_check(army)
        if validation is not None:
            return HttpResponse(dumps(validation), content_type="application/json")
        mongo_models.save_army(name, version, army)
        return HttpResponse("{}", content_type="application/json")

@login_required(login_url='/login/')
def edit_army_name(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return HttpResponseBadRequest(f"Only the admin can rename a book", status=401)
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        oldName = body["oldName"]
        oldVersion = body["oldVersion"]
        version = body["version"]
        if name == "" or version == "" or oldName=="":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version} or old name is empty {oldName} or old version is empty {oldVersion}", status=500)
        armies = PublicArmy.objects.filter(name=oldName, version=oldVersion)
        public_army = len(armies) > 0
        if public_army:
            return HttpResponseBadRequest(f"can't rename a public army", status=500)
        listTemplate = list(LatexTemplate.objects.filter(name=oldName))
        for l in listTemplate:
            l.name = name
            l.save()
        mongo_models.edit_army_name(oldName,oldVersion, version, name)
        return HttpResponse("{}", content_type="application/json")
@login_required(login_url='/login/')
def set_current_version(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return HttpResponseBadRequest(f"Only the admin can select a version", status=401)
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=500)
        PublicArmy.objects.update_or_create(name=name, defaults={"version": version})
        return HttpResponse("{}", content_type="application/json")

@login_required(login_url='/login/')
def make_public(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return HttpResponseBadRequest(f"Only the admin can make an army public", status=401)
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=500)
        PublicArmy.objects.create(name=name, version= version)
        return HttpResponse("{}", content_type="application/json")
def is_public_army(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=500)
        armies = PublicArmy.objects.filter(name=name, version=version)
        public_army = len(armies) > 0
        return HttpResponse(dumps({"public_army": public_army}), content_type="application/json")


@login_required(login_url='/login/')
def delete_army(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return HttpResponseBadRequest(f"Only the admin can delete an army", status=401)
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=500)
        try:
            PublicArmy.objects.get(name=name).delete()
        except:
            pass
        mongo_models.delete_army(name, version)
        return HttpResponse("{}", content_type="application/json")


@login_required(login_url='/login/')
def parse_translation(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        latex = body["latex"]
        if latex == "":
            return HttpResponseBadRequest(f"latex is empty {latex}", status=500)
        mongo_models.parse_translation(latex)
        return HttpResponse(dumps(mongo_models.parse_translation(latex)), content_type="application/json")


def download_army(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        name = body["name"]
        version = body["version"]
        if name == "" or version == "":
            return HttpResponseBadRequest(f"name is empty: {name} or version is empty {version}", status=500)
        userKnown = request.user.is_authenticated
        if not userKnown:
            armies = PublicArmy.objects.filter(name=name, version=version)
            if len(armies) == 0:
                return HttpResponseBadRequest(f"You need to be logged in to see this", status=401)
        # TODO language
        language = "en"
        global_translation = mongo_models.get_army(GLOBAL_TRANSLATION_NAME,
                                                   PublicArmy.objects.filter(name=GLOBAL_TRANSLATION_NAME).aggregate(
                                                       Max('version'))[
                                                       'version__max'])
        logger_view.info(
            f"name: {name}, {PublicArmy.objects.filter(name=GLOBAL_TRANSLATION_NAME).aggregate(Max('version'))['version__max']}")
        global_translation = global_translation[0]['loc'] if len(global_translation) > 0 else {}
        (pdf, log, completed_process), filename,latex = export_armybook(name, language, global_translation,
                                                                  mongo_models.get_army(name, version)[0],
                                                                  LatexTemplate.objects.filter(name=name)[0])
        response = HttpResponse(pdf, content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + filename
        return response


def get_item_types(request):
    if request.method == 'POST':
        return HttpResponse(dumps(mongo_models.ITEM_TYPES), content_type="application/json")


def get_spell_types(request):
    if request.method == 'POST':
        return HttpResponse(dumps(mongo_models.SPELL_TYPES), content_type="application/json")


def get_spell_durations(request):
    if request.method == 'POST':
        return HttpResponse(dumps(mongo_models.SPELL_DURATIONS), content_type="application/json")


def get_unit_types(request):
    if request.method == 'POST':
        return HttpResponse(dumps(mongo_models.UNIT_TYPES), content_type="application/json")


def get_unit_heights(request):
    if request.method == 'POST':
        return HttpResponse(dumps(mongo_models.UNIT_HEIGHTS), content_type="application/json")


def get_rule_types(request):
    if request.method == 'POST':
        return HttpResponse(dumps(mongo_models.RULE_TYPES), content_type="application/json")


def custom_logout(request):
    logout(request)
    return HttpResponse("{}", content_type="application/json")


def custom_login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        username = body["username"]
        password = body["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("{}", content_type="application/json")
        else:
            return HttpResponseBadRequest(f"Login failed", status=401)


def is_logged_in(request):
    return HttpResponse(dumps({'loggedIn': request.user.is_authenticated}))
