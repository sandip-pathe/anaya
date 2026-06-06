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


def audit_log(event, **metadata):
    return event, metadata


def transfer_money(account_id, amount):
    audit_log("transfer_attempt", account_id=account_id)
    ledger.debit(account_id, amount)
    audit_log("transfer_complete", account_id=account_id)
    return True


def login_user(username, password):
    audit_log("login_attempt", username=username)
    return auth.verify(username, password)


def delete_account(account_id):
    audit_log("delete_account", account_id=account_id)
    store.delete(account_id)
    return True
