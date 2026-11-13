
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='base.html',
            extra_context={'page': 'login'},
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),

    path('create/', views.create_announcement, name='create_announcement'),

    path('my/', views.my_announcements, name='my_announcements'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('saved/', views.saved_announcements, name='saved'),

    path(
        'announcement/<int:announcement_id>/',
        views.announcement_detail,
        name='announcement_detail'
    ),

    path(
        'announcement/<int:announcement_id>/edit/',
        views.edit_announcement,
        name='edit_announcement'
    ),

    path(
        'announcement/<int:announcement_id>/delete/',
        views.delete_announcement,
        name='delete_announcement'
    ),

    path(
        'announcement/<int:announcement_id>/subscribe/',
        views.subscribe_announcement,
        name='subscribe_announcement'
    ),

    path(
        'announcement/<int:announcement_id>/unsubscribe/',
        views.unsubscribe_announcement,
        name='unsubscribe_announcement'
    ),

    path(
        'announcement/<int:announcement_id>/save/',
        views.save_announcement,
        name='save_announcement'
    ),

    path(
        'announcement/<int:announcement_id>/unsave/',
        views.unsave_announcement,
        name='unsave_announcement'
    ),
]
