
def check_user_company(user):
    if hasattr(user, 'company'):
        return True
    return False
