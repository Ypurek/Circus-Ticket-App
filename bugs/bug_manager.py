from .models import BugRegister


def set_property(key, value):
    prop = BugRegister.objects.filter(property=key)
    if len(prop) == 0:
        BugRegister.objects.create(property=key, value=value)
    else:
        prop[0].value = value
        prop[0].save()


def get_property(key):
    prop = BugRegister.objects.filter(property=key)
    if len(prop) != 0:
        return prop[0].value
    else:
        set_property(key, False)
        return False
