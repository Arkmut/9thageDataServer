from djongo import models


class SpecialRule(models.Model):
    _id = models.ObjectIdField()

    class Meta:
        _use_db = 'noSQL'
        





class Unit(models.Model):
    _id = models.ObjectIdField()

    class Meta:
        _use_db = 'noSQL'
        


class ArmyCategory(models.Model):
    _id = models.ObjectIdField()

    class Meta:
        _use_db = 'noSQL'
        


class SpecialItems(models.Model):
    _id = models.ObjectIdField()

    class Meta:
        _use_db = 'noSQL'
        


class ArmyRules(models.Model):
    _id = models.ObjectIdField()
    rules = models.ArrayField(
        model_container=SpecialRule
    )

    class Meta:
        _use_db = 'noSQL'
        


class ModelRules(models.Model):
    _id = models.ObjectIdField()
    rules = models.ArrayField(
        model_container=SpecialRule
    )

    class Meta:
        _use_db = 'noSQL'
        


class Hereditary(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField(max_length=512)

    class Meta:
        _use_db = 'noSQL'
        


class SpecialItems(models.Model):
    _id = models.ObjectIdField()

    class Meta:
        _use_db = 'noSQL'
        


class ArmyCategories(models.Model):
    _id = models.ObjectIdField()
    categories = models.ArrayField(
        model_container=ArmyCategory
    )

    class Meta:
        _use_db = 'noSQL'
        


class ArmyList(models.Model):
    _id = models.ObjectIdField()
    units = models.ArrayField(
        model_container=Unit
    )

    class Meta:
        _use_db = 'noSQL'
        


class ArmyBook(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField(max_length=512)
    version = models.TextField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    army_rules = models.EmbeddedField(
        model_container=ArmyRules
    )
    model_rules = models.EmbeddedField(
        model_container=ModelRules
    )
    hereditary_spell = models.EmbeddedField(
        model_container=Hereditary
    )
    special_items = models.EmbeddedField(
        model_container=SpecialItems
    )
    army_categories = models.EmbeddedField(
        model_container=ArmyCategories

    )
    army_list = models.EmbeddedField(
        model_container=ArmyList
    )

    class Meta:
        _use_db = 'noSQL'
        ordering = ("-created_at",)
