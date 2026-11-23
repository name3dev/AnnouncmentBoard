from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q

from .models import Announcement, AnnouncementSubscription, SavedAnnouncement
from .forms import AnnouncementForm


def render_page(request, page, context=None):
    if context is None:
        context = {}

    context['page'] = page

    return render(request, 'base.html', context)


def action_redirect(request):
    next_url = request.POST.get('next')

    if next_url and next_url.startswith('/') and not next_url.startswith('//'):
        return redirect(next_url)

    return redirect('home')


def home(request):
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')

    search = request.GET.get('q', '')
    category = request.GET.get('category', '')

    if search:
        announcements = announcements.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if category:
        announcements = announcements.filter(category=category)

    context = {
        'announcements': announcements,
        'search': search,
        'selected_category': category,
    }

    return render_page(request, 'home', context)


def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
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

    context = {
        'announcement': announcement,
        'is_subscribed': is_subscribed,
        'is_saved': is_saved,
    }

    return render_page(request, 'detail', context)


@login_required
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.save()

            messages.success(request, 'Объявление создано.')
            return redirect('announcement_detail', announcement_id=announcement.id)
    else:
        form = AnnouncementForm()

    return render_page(request, 'form', {'form': form})


@login_required
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        user=request.user
    )

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)

        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено.')
            return redirect('announcement_detail', announcement_id=announcement.id)
    else:
        form = AnnouncementForm(instance=announcement)

    return render_page(request, 'form', {
        'form': form,
        'announcement': announcement,
    })


@login_required
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        user=request.user
    )

    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Объявление удалено.')
        return redirect('my_announcements')

    return render_page(request, 'detail', {
        'announcement': announcement,
        'confirm_delete': True,
    })


@login_required
def my_announcements(request):
    announcements = Announcement.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render_page(request, 'my', {
        'announcements': announcements,
    })


@login_required
def subscriptions(request):
    subscriptions_list = AnnouncementSubscription.objects.filter(
        user=request.user
    ).select_related('announcement')

    announcements = []

    for subscription in subscriptions_list:
        if subscription.announcement.is_active:
            announcements.append(subscription.announcement)

    return render_page(request, 'subscriptions', {
        'announcements': announcements,
    })


@login_required
def saved_announcements(request):
    saved_list = SavedAnnouncement.objects.filter(
        user=request.user
    ).select_related('announcement')

    announcements = []

    for saved in saved_list:
        if saved.announcement.is_active:
            announcements.append(saved.announcement)

    return render_page(request, 'saved', {
        'announcements': announcements,
    })


@login_required
def subscribe_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        is_active=True
    )

    subscription = AnnouncementSubscription.objects.filter(
        user=request.user,
        announcement=announcement
    )

    if subscription.exists():
        subscription.delete()
        messages.success(request, 'Вы отписались от объявления.')
    else:
        AnnouncementSubscription.objects.create(
            user=request.user,
            announcement=announcement
        )
        messages.success(request, 'Вы подписались на объявление.')

    return action_redirect(request)


@login_required
def save_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id,
        is_active=True
    )

    saved = SavedAnnouncement.objects.filter(
        user=request.user,
        announcement=announcement
    )

    if saved.exists():
        saved.delete()
        messages.success(request, 'Объявление удалено из сохранённых.')
    else:
        SavedAnnouncement.objects.create(
            user=request.user,
            announcement=announcement
        )
        messages.success(request, 'Объявление сохранено.')

    return action_redirect(request)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render_page(request, 'register', {
        'form': form,
    })
@login_required
def unsubscribe_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    subscription = AnnouncementSubscription.objects.filter(
        user=request.user,
        announcement=announcement
    )

    subscription.delete()

    messages.success(request, 'Вы отписались от объявления.')

    return action_redirect(request)
@login_required
def unsave_announcement(request, announcement_id):
    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    saved = SavedAnnouncement.objects.filter(
        user=request.user,
        announcement=announcement
    )

    saved.delete()

    messages.success(request, 'Объявление удалено из избранного.')

    return action_redirect(request)