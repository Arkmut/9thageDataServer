"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
app_name = "9thAgeDataServer"
urlpatterns = [
    path("api/army_list", army_list, name="army_list"),
    path("api/army_list/create_army", create_army, name="create_army"),
    path("api/army_list/get_army", get_army, name="get_army"),
    path("api/army_list/download_army", download_army, name="download_army"),
    path("api/army_list/save_army", save_army, name="save_army"),
    path("api/army_list/set_current_version", set_current_version, name="set_current_version"),
    path("api/army_list/make_public", make_public, name="set_current_version"),
    path("api/army_list/delete_army", delete_army, name="delete_army"),
    path("api/army_list/edit_army_name", edit_army_name, name="edit_army_name"),
    path("api/army_list/is_public_army", is_public_army, name="is_public_army"),
    path("api/army_list/parse_translation", parse_translation, name="parse_translation"),

    path("api/get_item_types", get_item_types, name="get_item_types"),
    path("api/get_rule_types", get_rule_types, name="get_rule_types"),
    path("api/get_spell_types", get_spell_types, name="get_spell_types"),
    path("api/get_spell_durations", get_spell_durations, name="get_spell_durations"),
    path("api/get_unit_types", get_unit_types, name="get_unit_types"),
    path("api/get_unit_heights", get_unit_heights, name="get_unit_heights"),
    path("api/login", custom_login, name="custom_login"),
    path("api/logout", custom_logout, name="custom_logout"),
    path("api/is_logged_in", is_logged_in, name="is_logged_in"),
    path('api/admin/', admin.site.urls),
    path('api/get_token', get_csrf_token)


]

