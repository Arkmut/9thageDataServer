import json
import logging

from django.core.management.base import BaseCommand

from ...models import mongo_models, army_check

logger_command = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Loads data into the database'

    def add_arguments(self, parser):
        parser.add_argument('--army', type=str, help='path to the army file')

    def handle(self, *args, **options):
        armyPath = options["army"]
        f = open(armyPath)
        army = json.load(f)
        f.close()
        validation = army_check(army)
        if validation is not None:
            logger_command.error("Failed validation")
        mongo_models.save_army(army['name'], army['version'], army)
