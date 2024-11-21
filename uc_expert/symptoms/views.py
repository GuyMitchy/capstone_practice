from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Symptom
from .forms import SymptomForm

class SymptomListView(LoginRequiredMixin, ListView):
    model = Symptom
    template_name = 'symptoms/symptom_list.html'
    context_object_name = 'symptoms'
    
    def get_queryset(self):
        return Symptom.objects.filter(user=self.request.user).order_by('-date')

class SymptomCreateView(LoginRequiredMixin, CreateView):
    model = Symptom
    form_class = SymptomForm
    template_name = 'symptoms/symptom_form.html'
    success_url = reverse_lazy('symptoms:list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SymptomUpdateView(LoginRequiredMixin, UpdateView):
    model = Symptom
    form_class = SymptomForm
    template_name = 'symptoms/symptom_form.html'
    success_url = reverse_lazy('symptoms:list')
    
    def get_queryset(self):
        return Symptom.objects.filter(user=self.request.user)

class SymptomDeleteView(LoginRequiredMixin, DeleteView):
    model = Symptom
    template_name = 'symptoms/symptom_confirm_delete.html'
    success_url = reverse_lazy('symptoms:list')
    
    def get_queryset(self):
        return Symptom.objects.filter(user=self.request.user)