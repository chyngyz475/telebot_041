from django.core.management.base import BaseCommand
from telegram.bot import main as telegram_main

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        telegram_main()
