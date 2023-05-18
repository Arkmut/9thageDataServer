from djongo import models as mongo_models



class ArmyBook(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    name = mongo_models.TextField(max_length=512)
    version = mongo_models.TextField(max_length=512)
    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)

    class Meta:
        _use_db = 'noSQL'
        ordering = ("-created_at", )