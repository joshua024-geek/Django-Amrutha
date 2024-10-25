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
