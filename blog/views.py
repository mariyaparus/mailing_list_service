from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'text', 'blog_img',)
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Создание материала'})
        return context


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'text', 'blog_img', 'is_published',)

    def form_valid(self, form):
        """
        Динамически формировать slug
        """
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        """
        После успешного редактирования перенаправляет на просмотр материала
        """
        return reverse('blog:article', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Редактирование статьи'})
        return context


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        """
        Выводить только опубликованные материалы
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Блог'})
        return context


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """
        Счетчик просмотров
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        blog_item = Blog.objects.get(pk=self.kwargs.get('pk'))
        context_data['blog_pk'] = blog_item.pk,
        context_data['title'] = f'Статья - {blog_item.title}'

        return context_data


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Удаление статьи'})
        return context
