
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.db.models import Q, Count
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Announcement, AnnouncementSubscription, SavedAnnouncement
from .forms import AnnouncementForm


def render_page(request, page, **context):
    return render(request, 'base.html', {
        'page': page,
        **context
    })


def action_redirect(request, announcement):
    next_url = request.POST.get('next', '')

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        return redirect(next_url)

    return redirect('announcement_detail', announcement_id=announcement.id)


# Главная страница и поиск
def home(request):
    announcements = Announcement.objects.filter(
        is_active=True
    ).select_related('user').annotate(
        subscriptions_count=Count('subscriptions', distinct=True)
    )

    # Получаем текст поиска и выбранную категорию
    search_query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    # Поиск по названию или описанию
    if search_query:
        announcements = announcements.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Фильтр по категории
    if category:
        announcements = announcements.filter(category=category)

    # Получаем ID сохранённых объявлений
    saved_ids = []

    if request.user.is_authenticated:
        saved_ids = SavedAnnouncement.objects.filter(
            user=request.user
        ).values_list('announcement_id', flat=True)

    return render_page(
        request,
        'home',
        announcements=announcements,
        search_query=search_query,
        selected_category=category,
        categories=Announcement.CATEGORY_CHOICES,
        saved_ids=saved_ids
    )


# Страница отдельного объявления
def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(
        Announcement.objects.select_related('user').annotate(
            subscriptions_count=Count('subscriptions', distinct=True),
            saved_count=Count('saved_by', distinct=True)
        ),
        id=announcement_id,
        is_active=True
    )

    is_subscribed = False
    is_saved = False

    if request.user.is_authenticated:
        is_subscribed = AnnouncementSubscription.objects.filter(
            user=request.user,
            announcement=announcement
        ).exists()

        is_saved = SavedAnnouncement.objects.filter(
            user=request.user,
            announcement=announcement
        ).exists()

    return render_page(
        request,
        'detail',
        announcement=announcement,
        is_subscribed=is_subscribed,
        is_saved=is_saved
    )


# Создание объявления
@login_required
def create_announcement(request):
    form = AnnouncementForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        announcement = form.save(commit=False)
        announcement.user = request.user
        announcement.save()

        messages.success(request, 'Объявление опубликовано!')

        return redirect(
            'announcement_detail',
            announcement_id=announcement.id
        )

    return render_page(
        request,
        'form',
        form=form,
        page_title='Создать объявление',
        button_text='Опубликовать'
    )


# Редактирование объявления
@login_required
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        user=request.user
    )

    form = AnnouncementForm(
        request.POST or None,
        instance=announcement
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Объявление обновлено!')

        return redirect(
            'announcement_detail',
            announcement_id=announcement.id
        )

    return render_page(
        request,
        'form',
        form=form,
        page_title='Редактировать объявление',
        button_text='Сохранить изменения'
    )


# Удаление объявления
@login_required
@require_POST
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        user=request.user
    )

    announcement.delete()
    messages.success(request, 'Объявление удалено.')

    return redirect('my_announcements')


# Мои объявления
@login_required
def my_announcements(request):
    announcements = Announcement.objects.filter(
        user=request.user
    ).annotate(
        subscriptions_count=Count('subscriptions', distinct=True)
    )

    return render_page(
        request,
        'my',
        announcements=announcements
    )


# Объявления, на которые подписан пользователь
@login_required
def subscriptions(request):
    announcements = Announcement.objects.filter(
        subscriptions__user=request.user,
        is_active=True
    ).select_related('user').distinct()

    return render_page(
        request,
        'subscriptions',
        announcements=announcements
    )


# Сохранённые объявления
@login_required
def saved_announcements(request):
    announcements = Announcement.objects.filter(
        saved_by__user=request.user,
        is_active=True
    ).select_related('user').distinct()

    return render_page(
        request,
        'saved',
        announcements=announcements
    )


# Подписка на объявление
@login_required
@require_POST
def subscribe_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        is_active=True
    )

    if announcement.user != request.user:
        AnnouncementSubscription.objects.get_or_create(
            user=request.user,
            announcement=announcement
        )

    return action_redirect(request, announcement)


# Отписка от объявления
@login_required
@require_POST
def unsubscribe_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    AnnouncementSubscription.objects.filter(
        user=request.user,
        announcement=announcement
    ).delete()

    return action_redirect(request, announcement)


# Сохранение объявления
@login_required
@require_POST
def save_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        is_active=True
    )

    if announcement.user != request.user:
        SavedAnnouncement.objects.get_or_create(
            user=request.user,
            announcement=announcement
        )

    return action_redirect(request, announcement)


# Удаление из сохранённых
@login_required
@require_POST
def unsave_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    SavedAnnouncement.objects.filter(
        user=request.user,
        announcement=announcement
    ).delete()

    return action_redirect(request, announcement)


# Регистрация
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)

        messages.success(request, 'Аккаунт успешно создан!')

        return redirect('home')

    return render_page(
        request,
        'register',
        form=form
    )
