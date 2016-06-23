# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from contact.models import Message
from contact.forms import MessageCreateForm, MessageUpdateForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied


class MessageListView(ListView):
    model = Message
    template_name = "contact/message_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        slug_list = Message.objects.filter(send_user=self.request.user).values_list("homework__slug", flat="True").distinct()
        message_list = []
        for slug in slug_list:
            obj = Message.objects.filter(send_user=self.request.user, homework__slug=slug)[0]
            message_list.append(obj)
        context["message_list"] = message_list
        return context


class MessageDetailView(DetailView):
    model = Message
    template_name = "contact/message_detail.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.send_user == self.request.user:
            raise PermissionDenied
        return super(MessageDetailView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Message.objects.filter(slug=slug)[0]
        return obj

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super(MessageDetailView, self).get_context_data(**kwargs)
        questions = Message.objects.filter(homework=obj.homework, send_user=self.request.user)
        answers = Message.objects.filter(homework=obj.homework, to_user=self.request.user)
        content = []
        for i in range(0,questions.count()):
            couple = dict()
            question = questions[i]
            couple["question"] = question
            if answers.count() > i:
                answer = answers[i]
                couple["answer"] = answer
            content.append(couple)
        context["content"] = content
        return context


class MessageCreateView(CreateView):
    model = Message
    template_name = "contact/message_create.html"
    form_class = MessageCreateForm
    success_url = reverse_lazy("message_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.instance
        instance.send_user = self.request.user
        instance.to_user = User.objects.filter(is_superuser=True)[0]
        messages.success(self.request, "Başarıyla oluşturuldu")
        return super(MessageCreateView, self).form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "contact/message_update.html"
    form_class = MessageUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.send_user == self.request.user or obj.is_answered == True:
            raise PermissionDenied
        return super(MessageUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.instance
        instance.send_user = self.request.user
        instance.to_user = User.objects.filter(is_superuser=True)[0]
        messages.info(self.request, "Başarıyla güncellendi")
        return super(MessageUpdateView, self).form_valid(form)

    def get_success_url(self):
        slug = self.kwargs.get("slug")
        return reverse("message_detail", args=(slug,))


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "contact/message_delete.html"
    success_url = reverse_lazy("message_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.send_user == self.request.user or obj.is_answered == True:
            raise PermissionDenied
        return super(MessageDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, "Başarıyla silindi")
        return super(MessageDeleteView, self).delete(request, *args, **kwargs)
