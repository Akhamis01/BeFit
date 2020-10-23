from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Discussions


urlpatterns = [
    path('', views.index, name='index'),
    path('recipe', views.recipe, name='recipe'),
    path('fitness', views.fitness, name='fitness'),
    path('export/<int:id>', views.export, name='export'),
    path('custom_export', views.custom_export, name='custom_export'),
    path('user_exist', views.user_exist, name='user_exist'),
    path('member_upgrade', views.member_upgrade, name='member_upgrade'),
    path('discussions', Discussions.as_view(), name='discussions'),
    path("createpost/<str:username>", views.create_post, name="createpost"),
    path("create_comment/<str:username>", views.create_comment, name="create_comment"),
    path("spec_post/<id>", views.spec_post, name="spec_post"),
    path("upvote/", views.upvote, name="upvote"),
    path("downvote/", views.downvote, name="downvote"),
    path("delete/", views.delete, name="delete"),
    path("delete_comment/", views.delete_comment, name="delete_comment"),
    path('profile', views.profile, name='profile'),
    path('login', views.login_view, name='login'),
    path("logout", views.logout_view, name='logout'),
    path("register", views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)