from django.urls import path
from . import views

urlpatterns = [
    # Доступна за адресою: http://127.0.0.1:8000/
    path('', views.GroupInfoView.as_view(), name='group_info'),

    # Доступні за адресами: http://127.0.0.1:8000/register/ тощо
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Доступні за адресами: http://127.0.0.1:8000/blog/ тощо
    path('blog/', views.PostListView.as_view(), name='post_list'),
    path('blog/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('blog/<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment'),

    path('blog/new/', views.PostCreateView.as_view(), name='post_create'),
    path('blog/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('blog/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]