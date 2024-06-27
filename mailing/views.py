from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import CheckboxSelectMultiple
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailing.forms import ClientForm, MessageForm, MailingForm, MailingModeratorForm
from mailing.models import Client, Message, Mailing, Logs


class HomeView(TemplateView):
    template_name = 'mailing/base.html'
    # extra_context = {
    #     'title': 'Добро пожаловать в наш сервис рассылок "Почтальон"!',
    # }
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = Mailing.objects.all().count()
        context_data['active_mailing_count'] = Mailing.objects.filter(
            status=Mailing.STATUS_STARTED).count()
        context_data['count_unique_mailing_client'] = Client.objects.all().count()
        context_data['blog_list'] = Blog.objects.all().order_by('?')[:3]
        context_data.update({'title': 'Добро пожаловать в наш сервис рассылок "Почтальон"!'})
        return context_data


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

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['mailing_count'] = Mailing.objects.all().count()
    #     context_data['active_mailing_count'] = Mailing.objects.filter(
    #         status=Mailing.STATUS_STARTED).count()
    #     context_data['count_unique_mailing_client'] = Client.objects.all().count()
    #     context_data.update({'title': 'Рассылки'})
    #     return context_data
    extra_context = {
        'title': 'Рассылки',
    }
    # permission_required = 'mailing.view_malling'
    #
    # def handle_no_permission(self):
    #     return redirect('mailing:mailing_list')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_clients = self.object.client.values_list('pk', flat=True)
        context['selected_clients'] = selected_clients
        return context

    def get_success_url(self):
        return reverse('mailing:message', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return MailingForm
        if user.has_perm('mailing.set_status'):
            return MailingModeratorForm
        raise PermissionDenied


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