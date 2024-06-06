from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import CheckboxSelectMultiple
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing, Logs


class HomeView(TemplateView):
    template_name = 'mailing/home.html'
    extra_context = {
        'title': 'Добро пожаловать в наш сервис рассылок "Почтальон"!',
    }


class ClientListView(LoginRequiredMixin, ListView):
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


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Клиент'})
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:client', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


###########################################################################


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения',
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Сообщение'})
        return context


class MessageCreateView(LoginRequiredMixin,CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:message', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')


######################################################################################


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки',
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Рассылка'})
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)
        form.fields['client'].queryset = Client.objects.filter(user=self.request.user)

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     selected_clients = self.object.client.values_list('pk', flat=True)
    #     context['selected_clients'] = selected_clients
    #     return context

    def get_success_url(self):
        return reverse('mailing:message', args=[self.kwargs.get('pk')])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')


##############################################################################

class LogsListView(LoginRequiredMixin, ListView):
    model = Logs

    extra_context = {
        'title': 'Попытки рассылки',
    }

    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(
    #         user=self.request.user
    #     )
    #     if not self.request.user.is_staff:
    #         queryset = queryset.filter(user=self.request.user)
    #
    #     return queryset


###############################################################################
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'mailing/contacts.html', context)