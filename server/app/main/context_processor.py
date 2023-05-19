import os

def export_vars(request):
    data = {}
    data['DEBUG'] = os.environ.get("DEBUG")
    return data