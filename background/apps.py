from django.apps import AppConfig


class BackgroundConfig(AppConfig):
    name = 'background'

    def ready(self):
        from background import job
        job.start()
