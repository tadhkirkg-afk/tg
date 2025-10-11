from django.db import models

class TelegramUser(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=(('M', 'Male'), ('F', 'Female')))
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username if self.username else {'first_name': self.first_name, 'last_name': self.last_name}

