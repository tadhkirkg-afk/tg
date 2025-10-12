from django.db import models

class TelegramUser(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=(('M', 'Male'), ('F', 'Female')), null=True, blank=True)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.username:
            return self.username
        elif self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return str(self.user_id)

class Wait(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.user.username:
            return self.user.username
        elif self.user.first_name or self.user.last_name:
            return f"{self.user.first_name or ''} {self.user.last_name or ''}".strip()
        return str(self.user.user_id)