from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Job, Category


class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Handle search
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        # Handle category filter
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'


class MyJobListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Job
    template_name = 'jobs/job_my_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.is_agency
    
    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    template_name = 'jobs/job_form.html'
    fields = ['title', 'description', 'category', 'location', 'salary', 'gender', 'responsibilities']
    success_url = reverse_lazy('jobs:job_my_list')
    
    def test_func(self):
        return self.request.user.is_agency
    
    def form_valid(self, form):
        form.instance.recruiter = self.request.user
        messages.success(self.request, 'Job created successfully!')
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'jobs/job_form.html'
    fields = ['title', 'description', 'category', 'location', 'salary', 'gender', 'responsibilities']
    
    def test_func(self):
        job = self.get_object()
        return self.request.user.is_agency and self.request.user == job.recruiter
    
    def get_success_url(self):
        return reverse_lazy('jobs:job_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('jobs:job_my_list')
    
    def test_func(self):
        job = self.get_object()
        return self.request.user.is_agency and self.request.user == job.recruiter
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Job deleted successfully!')
        return super().delete(request, *args, **kwargs)
