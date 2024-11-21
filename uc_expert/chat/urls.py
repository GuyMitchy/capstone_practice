from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='list'),
    path('new/', views.ChatCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ChatDetailView.as_view(), name='detail'),
    path('<int:pk>/send/', views.send_message, name='send_message'),
    path('<int:pk>/delete/', views.ChatDeleteView.as_view(), name='delete'),
]