import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'gamerate.settings')

import django
django.setup()

def populate():
    pass

if __name__ == "__main__":
    populate()