from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
import uuid
from django.db.models.signals import post_save


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    email = models.EmailField(null=False)
    username = models.CharField(max_length=20, unique=True, null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return f"<User:{self.id}> {self.username}"


class SearchHistory(models.Model):
    user = models.OneToOneField(User, related_name='history', on_delete=models.CASCADE)

    def __str__(self):
        return f"<SearchHistory> for {self.user.username}"

@receiver(post_save, sender=User)
def create_search_history(sender, instance, created, **kwargs):
    if created:
        SearchHistory.objects.create(user=instance)


class SearchItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    city = models.CharField(max_length=24, null=False)
    search_date = models.DateTimeField(auto_now=True)
    history = models.ForeignKey(SearchHistory, related_name="searches", on_delete=models.CASCADE)

    class Meta:
        ordering = ['search_date']

    def __str__(self):
        return f"<SearchItem> {self.city}"