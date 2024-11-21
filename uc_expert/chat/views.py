from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Conversation, Message
from knowledge.rag_setup import UCExpertRAG

rag_system = UCExpertRAG()

class ChatListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'chat/chat_list.html'
    context_object_name = 'conversations'
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by('-updated_at')

class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Conversation
    template_name = 'chat/chat_form.html'
    fields = ['title']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('chat:detail', kwargs={'pk': self.object.pk})

class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'chat/chat_detail.html'
    context_object_name = 'conversation'
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.message_set.all().order_by('created_at')
        return context

class ChatDeleteView(LoginRequiredMixin, DeleteView):
    model = Conversation
    template_name = 'chat/chat_confirm_delete.html'
    success_url = reverse_lazy('chat:list')
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

@login_required
def send_message(request, pk):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, pk=pk, user=request.user)
        user_message = request.POST.get('message')
        
        # Get recent symptoms for context
        recent_symptoms = request.user.symptom_set.order_by('-date')[:5]
        symptom_context = "\n".join(
            [f"Symptom: {s.description} (Severity: {s.severity})" 
            for s in recent_symptoms]
        )
        
        # Save user message
        Message.objects.create(
            conversation=conversation,
            content=user_message,
            is_bot=False
        )
        
        # Get AI response using RAG
        try:
            ai_response = rag_system.get_response(user_message, context=symptom_context)
            
            # Save AI response
            Message.objects.create(
                conversation=conversation,
                content=ai_response,
                is_bot=True
            )
            
            # Update conversation timestamp
            conversation.save()  # This updates the updated_at field
            
            return JsonResponse({
                'status': 'success',
                'message': ai_response
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)