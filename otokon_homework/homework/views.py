# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic.detail import DetailView
from homework.models import Lecture, Homework, AnswerSheet
from homework.forms import AnswerSheetCreateForm, AnswerSheetUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied


class LectureListView(ListView):
    model = Lecture
    template_name = "homework/lecture_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LectureListView, self).dispatch(
                                                    request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LectureListView, self).get_context_data(**kwargs)
        context["lecture_list"] = Lecture.objects.filter(is_available=True)
        return context


class HomeworkListView(ListView):
    model = Homework
    template_name = "homework/homework_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeworkListView, self).dispatch(
                                                    request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        homeworks = Homework.objects.filter(lecture__slug=self.kwargs.get("lecture"))
        context = super(HomeworkListView, self).get_context_data(**kwargs)
        context["homework_list"] = homeworks.filter(is_available=True)
        return context


class HomeworkDetailView(DetailView):
    model = Homework
    template_name = "homework/homework_detail.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeworkDetailView, self).dispatch(
                                                    request, *args, **kwargs)
    def get_object(self, queryset=None):
        lecture = self.kwargs.get("lecture")
        slug = self.kwargs.get("slug")
        homework = Homework.objects.get(lecture__slug=lecture, slug=slug)
        return homework        

    def get_context_data(self, **kwargs):
        lecture = self.kwargs.get("lecture")
        slug = self.kwargs.get("slug")
        homework = Homework.objects.get(lecture__slug=lecture, slug=slug)
        context = super(HomeworkDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            answers = AnswerSheet.objects.filter(homework=homework, user=self.request.user)
            context["answers"] = answers
        return context


class AnswerSheetCreateView(CreateView):
    model = AnswerSheet
    form_class = AnswerSheetCreateForm
    template_name = "homework/answersheet_create.html"
    success_url = reverse_lazy("homework_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AnswerSheetCreateView, self).dispatch(
                                                    request, *args, **kwargs)

    def form_valid(self, form):
        lecture_slug = self.kwargs.get("lecture")
        instance = form.instance
        instance.user = self.request.user
        lecture = Lecture.objects.get(slug=lecture_slug)
        homework = Homework.objects.filter(lecture=lecture).get(slug=self.kwargs.get("slug"))
        instance.homework = homework
        messages.success(self.request, "Başarıyla oluşturuldu.")
        return super(AnswerSheetCreateView, self).form_valid(form)

    def get_success_url(self):
        lecture = self.kwargs.get("lecture")
        slug = self.kwargs.get("slug")
        return reverse("homework_detail", args=[lecture, slug,])


class AnswerSheetUpdateView(UpdateView):
    model = AnswerSheet
    form_class = AnswerSheetUpdateForm
    template_name = "homework/answersheet_update.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return super(AnswerSheetUpdateView, self).dispatch(
                                                    request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.instance
        instance.user = self.request.user
        instance.homework = self.kwargs.get("homework")
        messages.success(self.request, "Başarıyla güncellendi")
        return super(AnswerSheetUpdateView, self).form_valid(form)

    def get_success_url(self):
        lecture = self.kwargs.get("lecture")
        obj = self.get_object()
        return reverse("homework_detail", args=[lecture, obj.homework.slug,])


class AnswerSheetDeleteView(DeleteView):
    model = AnswerSheet
    template_name = "homework/answersheet_delete.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return super(AnswerSheetDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.info(request, "Başarıyla silindi")
        return super(AnswerSheetDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        lecture = self.kwargs.get("lecture")
        obj = self.get_object()
        return reverse("homework_detail", args=[lecture, obj.homework.slug,])
