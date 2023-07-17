import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import CheckboxSelectMultiple
from .models import *
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayWidget
from django_better_admin_arrayfield.forms.fields import DynamicArrayField
from django import forms

logger_admin = logging.getLogger(__name__)


class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username"]

class LatexInline1(admin.TabularInline):
    model = SubLatexInitImport
    extra = 1
    fk_name='owner'

class LatexInline2(admin.TabularInline):
    model = SubLatexImports
    extra = 1
    fk_name='owner'



class LatexModelAdmin(admin.ModelAdmin):
    model = LatexTemplate
    exclude = ['lastModified','init_sub_imports','book_sub_imports']
    list_display = ['name']
    inlines = [LatexInline1,LatexInline2]
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name in ["init_sub_imports", "book_sub_imports"]:
            if 'object_id' in request.resolver_match.kwargs:
                # this line below got the proper primary key for our object of interest
                self_id = request.resolver_match.kwargs['object_id']

                # then we did some stuff you don't care about
                instance = LatexTemplate.objects.get(id=self_id)
                if instance:
                    # Exclude self from the many-to-many field
                    queryset = db_field.remote_field.model.objects.exclude(pk=instance.pk)
                    kwargs['queryset'] = queryset
            kwargs["widget"] = FilteredSelectMultiple(db_field.name.replace("_", " "), is_stacked=False)
            kwargs["help_text"] = ""

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["title"]:
            if 'object_id' in request.resolver_match.kwargs:
                # this line below got the proper primary key for our object of interest
                self_id = request.resolver_match.kwargs['object_id']

                # then we did some stuff you don't care about
                instance = LatexTemplate.objects.get(id=self_id)
                if instance:
                    # Exclude self from the many-to-many field
                    queryset = db_field.remote_field.model.objects.exclude(pk=instance.pk)
                    kwargs['queryset'] = queryset

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.unregister(User)
admin.site.register(PublicArmy)
admin.site.register(LatexTemplate, LatexModelAdmin)
