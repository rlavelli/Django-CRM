from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from agents.mixins import OrganizerAndLoginRequiredMixin
from .models import Lead
from .forms import LeadModelForm, CustomUserCreationForm

# Create your views here.

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = 'landing.html'

# def landing_page(request):
#     return render(request, 'landing.html')

class LeadListView(LoginRequiredMixin,ListView):
    template_name = 'leads/lead_list.html'    
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter the agent loggedin
            queryset = queryset.filter(agent__user=user)
        return queryset

# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         'leads': leads
#     }
#     return render(request, 'leads/lead_list.html', context=context)

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter the agent loggedin
            queryset = queryset.filter(agent__user=user)
        return queryset

# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         'lead': lead
#     }
#     return render(request, 'leads/lead_detail.html', context=context)

class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # Send Email Test
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        # continue with usual beheaviour
        return super(LeadCreateView, self).form_valid(form)

# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')
#     context = {
#         'form': form
#     }
#     return render(request, 'leads/lead_create.html', context=context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)
#     if request.method == "POST":
#         form = LeadModelForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')

#     context = {
#         'form': form,
#         'lead': lead
#     }
#     return render(request, 'leads/lead_update.html', context=context)

class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()

#     return redirect('/leads')
