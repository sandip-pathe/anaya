class Ledger:
    def debit(self, account_id, amount):
        return account_id, amount


class Auth:
    def verify(self, username, password):
        return username == password


class Store:
    def delete(self, account_id):
        return account_id


ledger = Ledger()
auth = Auth()
store = Store()


def transfer_money(account_id, amount):
    ledger.debit(account_id, amount)
    return True


def login_user(username, password):
    return auth.verify(username, password)


def delete_account(account_id):
    store.delete(account_id)
    return True
