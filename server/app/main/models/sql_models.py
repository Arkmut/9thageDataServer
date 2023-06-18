from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    name = models.CharField(unique=True, primary_key=True)
    lastModified = models.DateField(auto_now=True)
    latex = models.TextField()
    init_sub_imports = models.ManyToManyField('self', related_name="initSubImports", symmetrical=False, blank=True)
    title = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    book_sub_imports = models.ManyToManyField('self', related_name="bookSubImports", symmetrical=False, blank=True)
    book_sub_imports_spaces = ArrayField(
        models.CharField(max_length=100, choices=Spaces.choices, default=Spaces.NONE), blank=True, null=True)

    def convertToLatex(self, space):
        if space == Spaces.NEW_PAGE:
            return "\\newpage\n"
        elif space == Spaces.MAIN_TITLE:
            return "\\additionalspacebeforemaintitle{}\n"
        return ""

    def getWithSubImports(self):
        subImport = ""
        for si in self.init_sub_imports.all():
            subImport += si.getWithSubImports() + "\n"
        res = self.latex.replace(SUB_IMPORT_BALISE, subImport)
        if self.title:
            res = res.replace(TITLE_IMPORT_BALISE, self.title.getWithSubImports())
        else:
            res = res.replace(TITLE_IMPORT_BALISE, "")
        subImport = ""
        counter = 0
        listSpaces = self.book_sub_imports_spaces
        for si in self.book_sub_imports.all():
            subImport += si.getWithSubImports() + "\n"
            if counter < len(listSpaces):
                subImport += self.convertToLatex(listSpaces[counter])
            else:
                subImport += self.convertToLatex(Spaces.NONE)
            counter += 1
        res = res.replace(BOOK_SUB_IMPORT_BALISE, subImport)

        return res
