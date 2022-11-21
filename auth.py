import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# Generate unique token from pin.  This adds a marginal amount of security.
def get_token():
    pin = os.getenv('PIN')
    if not pin:
        print('You need add a PIN value in .env file or setup in the environment variables')
        exit()
    token = hashlib.sha224(pin.encode('utf-8'))
    return token.hexdigest()

if __name__ == '__main__':
    # Display your pin token
    print(get_token())
