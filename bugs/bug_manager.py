from .models import BugRegister


def set_property(key, value):
    prop = BugRegister.objects.filter(name=key)
    if len(prop) == 0:
        BugRegister.objects.create(name=key, isActive=value)
    else:
        prop[0].isActive = value
        prop[0].save()


def get_property(key):
    prop = BugRegister.objects.filter(name=key)
    if len(prop) != 0:
        return prop[0].isActive
    else:
        set_property(key, False)
        return False
