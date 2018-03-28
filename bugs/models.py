from django.db import models


class BugRegister(models.Model):
    name = models.CharField(unique=True, null=False, max_length=50)
    isActive = models.BooleanField(default=False, null=False)
    description = models.CharField(default='', max_length=500)

    def __str__(self):
        return f'{self.name} - {self.isActive}'
