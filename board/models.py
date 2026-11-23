from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothes', 'Одежда'),
        ('furniture', 'Мебель'),
        ('transport', 'Транспорт'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def subscriptions_count(self):
        return AnnouncementSubscription.objects.filter(announcement=self).count()

    @property
    def saved_count(self):
        return SavedAnnouncement.objects.filter(announcement=self).count()


class AnnouncementSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')

    def __str__(self):
        return self.user.username + ' - ' + self.announcement.title


class SavedAnnouncement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'announcement')

    def __str__(self):
        return self.user.username + ' - ' + self.announcement.title