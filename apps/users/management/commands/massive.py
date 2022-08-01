import csv
import os

# Django
from django.core.management.base import BaseCommand

# Models
from apps.users.models import User


class Command(BaseCommand):
    help = "Seed application"

    def handle(self, *args, **options):
        path = os.path.dirname(__file__) + "/../data/data-hitmen.csv"
        if not User.objects.all():
            with open(path) as read_file:
                csv_reader = csv.reader(read_file, delimiter=",")
                for row in csv_reader:
                    pk = int(row[0])
                    boss = int(row[6])
                    data = {
                        "username": row[1],
                        "first_name": row[2],
                        "last_name": row[3],
                        "email": row[4],
                        "is_active": True,
                        "password": row[5],
                    }
                    if pk == 1:
                        data.update({"is_superuser": True})
                    if boss > 0:
                        data.update({"manager_id": boss})
                    User.objects.create_user(**data)
            read_file.close()
        self.stdout.write(self.style.SUCCESS("Successfully init data"))
