from django.contrib import admin
from in_good_hands import models as good_hands_model

admin.site.register(good_hands_model.Category)
admin.site.register(good_hands_model.Institution)
admin.site.register(good_hands_model.Donation)
