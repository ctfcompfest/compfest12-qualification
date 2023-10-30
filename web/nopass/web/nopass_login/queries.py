from nopass_login.models import Account
from nopass_login.utility import generate_random_string

def get_account(token):
    accounts = Account.objects.raw(f"SELECT * FROM nopass_login_account WHERE token='{token}'")
    for account in accounts:
        return account.username, account.is_admin
    return '', ''

def remove_account(token):
    account = Account.objects.get(token=token)
    account.delete()

def add_account(username):
    account = Account()
    account.token = generate_random_string(32)
    account.username = username
    account.save()

    return account.token