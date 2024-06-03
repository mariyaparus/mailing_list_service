from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
