class NonRelRouter:
    """
    A router to control if database should use
    primary database or non-relational one.
    """

    nonrel_models = {'ArmyBook'}

    def db_for_read(self, model, **_hints):
        try:
            if model._meta._use_db == 'noSQL':
                return 'noSQL'
        finally:
            return 'default'

    def db_for_write(self, model, **_hints):
        try:
            if model._meta._use_db == 'noSQL':
                return 'noSQL'
        finally:
            return 'default'

    def allow_migrate(self, _db, _app_label, model_name=None, **_hints):
        if _db == 'noSQL' or model_name in self.nonrel_models:
            return False
        return True