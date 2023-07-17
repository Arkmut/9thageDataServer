import logging

from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

SUB_IMPORT_BALISE = "$INIT_SUB_IMPORTS$"
TITLE_IMPORT_BALISE = "$TITLE_IMPORT$"
BOOK_SUB_IMPORT_BALISE = "$BOOK_SUB_IMPORT$"


class PublicArmy(models.Model):
    name = models.CharField(unique=True, primary_key=True, blank=False)
    version = models.CharField(blank=False)


class Spaces(models.TextChoices):
    MAIN_TITLE = 'MAIN_TITLE',
    NEW_PAGE = 'NEW_PAGE',
    NONE = "NONE"


class LatexTemplate(models.Model):
    name = models.CharField(unique=True)
    lastModified = models.DateField(auto_now=True)
    latex = models.TextField()
    init_sub_imports = models.ManyToManyField('self', related_name="initSubImports", through="SubLatexInitImport",
                                              symmetrical=False, blank=True)
    title = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    book_sub_imports = models.ManyToManyField('self', related_name="bookSubImports", through="SubLatexImports",
                                              symmetrical=False, blank=True)

    def __str__(self):
        return self.name

    def convertToLatex(self, space):
        if space == Spaces.NEW_PAGE:
            return "\\newpage\n"
        elif space == Spaces.MAIN_TITLE:
            return "\\additionalspacebeforemaintitle{}\n"
        return ""

    def getWithSubImports(self):
        subImport = ""
        init_sub_imports = self.init_sub_imports.all()
        init_sub_imports = [(si, SubLatexInitImport.objects.get(owner=self, sublatex=si)) for si in init_sub_imports]
        init_sub_imports.sort(key=lambda x: x[1].order)
        for si, data in init_sub_imports:
            subImport += si.getWithSubImports() + "\n"
            subImport += self.convertToLatex(data.space)

        res = self.latex.replace(SUB_IMPORT_BALISE, subImport)
        if self.title:
            res = res.replace(TITLE_IMPORT_BALISE, self.title.getWithSubImports())
        else:
            res = res.replace(TITLE_IMPORT_BALISE, "")
        subImport = ""
        counter = 0
        book_sub_imports = self.book_sub_imports.all()
        book_sub_imports = [(si, SubLatexImports.objects.get(owner=self, sublatex=si)) for si in book_sub_imports]
        book_sub_imports.sort(key=lambda x: x[1].order)

        for si, data in book_sub_imports:
            subImport += si.getWithSubImports() + "\n"
            subImport += self.convertToLatex(data.space)
            counter += 1
        res = res.replace(BOOK_SUB_IMPORT_BALISE, subImport)

        return res


class SubLatexImports(models.Model):
    owner = models.ForeignKey(LatexTemplate, on_delete=models.DO_NOTHING, related_name='owner2')
    sublatex = models.ForeignKey(LatexTemplate, on_delete=models.DO_NOTHING, related_name='sublatex2')
    space = models.CharField(max_length=100, choices=Spaces.choices, default=Spaces.NONE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "Sub-Imports"

    class Meta:
        ordering = ['order', ]


class SubLatexInitImport(models.Model):
    owner = models.ForeignKey(LatexTemplate, on_delete=models.DO_NOTHING, related_name='owner1')
    sublatex = models.ForeignKey(LatexTemplate, on_delete=models.DO_NOTHING, related_name='sublatex1')
    space = models.CharField(max_length=100, choices=Spaces.choices, default=Spaces.NONE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "Init-Imports"

    class Meta:
        ordering = ['order', ]
