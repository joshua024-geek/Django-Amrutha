from django.db import models

class BaseUser(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        abstract = True  # This model won't create a database table

    def __str__(self):
        return self.fullname

class User(BaseUser):
    # Additional fields specific to User can go here
    pass

class Admin(BaseUser):
    # Additional fields specific to Admin can go here
    pass
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    def __str__(self):
        return self.name