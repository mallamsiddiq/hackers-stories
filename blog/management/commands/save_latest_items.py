from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.tasks import dowload_trending

class Command(BaseCommand):
    help = """this custom command will help you seed your database to start with if you're not willing to work with the database provided

    			and if your database is seeded, this command will automatically update your database with the latest news"""

    def handle(self, *args, **kwargs):
        dowload_trending()