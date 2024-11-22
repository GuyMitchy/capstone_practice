from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):  # This seems to be for the widget on the home page im not using anymore
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Add any additional context for authenticated users
            context['recent_symptoms'] = self.request.user.symptom_set.all()[:5]
        return context