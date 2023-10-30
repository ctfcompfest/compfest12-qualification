from django.core.management.base import BaseCommand
from nopass_login.models import Account

class Command(BaseCommand):
    help = 'Clean database'

    def handle(self, *arg, **kwargs):
        cnt = 0
        for account in Account.objects.all():
            if account.is_admin and account.username == "admin":
                continue
            account.delete()
            cnt += 1
        self.stdout.write(f'Successfully delete {cnt} non-admin object(s)')
