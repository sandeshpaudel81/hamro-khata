from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from .models import Profile, Party, Transaction
from .forms import RegisterForm, UserForm, ProfileForm, PartyForm, TransactionForm
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'


@login_required(login_url='/login/')
def home(request):
    parties = Party.objects.filter(user=request.user)
    toPay = 0
    toGet = 0
    for party in parties:
        amt = party.amount()
        if amt < 0:
            toPay += amt
        else:
            toGet += amt
    total = toGet + toPay
    context = {'toPay': toPay, 'toGet': toGet, 'total': total, 'parties': parties}
    return render(request, 'home.html', context)


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'update_profile.html'

    def post(self, request):

        post_data = request.POST or None
        post_files = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, post_files, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('home'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PartyCreateView(LoginRequiredMixin, CreateView):
    form_class = PartyForm
    success_url = reverse_lazy('home')
    template_name = "add-party.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PartyCreateView, self).form_valid(form)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    success_url = reverse_lazy('home')
    template_name = "add-transaction.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TransactionCreateView, self).form_valid(form)

@login_required(login_url='/login/')
def party_statement(request, id):
    party = Party.objects.get(id=id)
    trans = Transaction.objects.filter(user=request.user, party=party)
    context = {'transactions': trans, 'party': party}
    return render(request, 'party-statement.html', context)