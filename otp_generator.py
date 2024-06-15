import pyotp

def get_code(secret_key):
    topt = pyotp.TOTP(secret_key, interval=30)
    code = topt.now()
    return code
