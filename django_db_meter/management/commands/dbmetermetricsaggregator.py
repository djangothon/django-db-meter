from django.core.management.base import BaseCommand

from django_db_meter.workers import run_metrics_consumer 

class Command(BaseCommand):
    command_help = "Consumes django db metric events"

    def handle(self, *args, **options):
        run_metrics_consumer()

