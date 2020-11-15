import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edu_linq.settings.develop")
django.setup()

# Create your tests here.

from course.models import Course

c = Course.objects.get(is_del=False, is_show=True, pk=29)
print(c.real_expire_price(7))
