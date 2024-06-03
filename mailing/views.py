from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm
from mailing.models import Client, Message


class HomeView(TemplateView):
    template_name = 'mailing/home.html'
    extra_context = {
        'title': 'Добро пожаловать в наш сервис рассылок "Почтальон"!',
    }


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты',
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Клиент'})
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


###########################################################################


class MessageListView(ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения',
    }


class MessageDetailView(DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Сообщение'})
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')

    # def get_success_url(self):
    #     return reverse('mailing:messages')
