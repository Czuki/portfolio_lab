from django.db import models
from django.contrib.auth.models import User

INSTITUTION_TYPE_CHOICES =(
    ("1", "Fundacja"),
    ("2", "Organizacja Pozarządowa"),
    ("3", "Zbiórka Lokalna"),
)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(max_length=1, choices=INSTITUTION_TYPE_CHOICES, default='1')
    categories = models.ForeignKey('Category', on_delete=models.CASCADE)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # hug falcon
    def total_donations(self):
        """
        Returns all-time total amount of donated containers and number of supported institutions
        """
        containers_count = 0
        institutions = list()
        donations = Donation.objects.all()
        # sum() aggregate() annotate()
        for donation in donations:
            containers_count += donation.quantity
            institutions.append(donation.institution)

        institutions_count = len(set(institutions))

        return containers_count, institutions_count
