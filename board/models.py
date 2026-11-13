from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Announcement(models.Model):

    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('vehicles', 'Транспорт'),
        ('real_estate', 'Недвижимость'),
        ('services', 'Услуги'),
        ('jobs', 'Работа'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='announcements'
    )

    title = models.CharField(
        max_length=150,
        verbose_name='Название'
    )

    description = models.TextField(
        max_length=5000,
        verbose_name='Описание'
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Категория'
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Цена'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class AnnouncementSubscription(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='announcement_subscriptions'
    )

    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'announcement'],
                name='unique_announcement_subscription'
            )
        ]

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (
            f'{self.user.username} — '
            f'{self.announcement.title}'
        )


class SavedAnnouncement(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_announcements'
    )

    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'announcement'],
                name='unique_saved_announcement'
            )
        ]

        verbose_name = 'Сохранённое объявление'
        verbose_name_plural = 'Сохранённые объявления'

    def __str__(self):
        return (
            f'{self.user.username} — '
            f'{self.announcement.title}'
        )
