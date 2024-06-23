# In your app's admin.py file
from django.contrib import admin

from .models import *

admin.site.register(Wallet)
admin.site.register(Transaction)
