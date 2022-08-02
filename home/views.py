from django.shortcuts import get_object_or_404, render,redirect
from .models import Task

# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CreateClass

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.

class CustomerLogin(LoginView):
    
    template_name = 'home/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class Register(FormView):
    template_name = 'home/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url =  reverse_lazy('home')


    def form_valid(self, form):
        user = form.save()
        #passing the user in without loging in
        if user is not None:
            login(self.request, user)
        return super(Register).form_valid(form)

#redirecting a registered user to the home restricting not to register again
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(Register, self).get( *args, **kwargs)




class Home(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'home/index.html'
    context_object_name = 'tasks'
#RESTRICTING USER TO VIEW ANOTHER USERS DETAILS
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        #outputing the count
        context['cont'] = context['tasks'].filter(complete=False).count()

        #search
        search_input = self.request.GET.get('search') or ''  # '' means without searching for anything its going to return nothing
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains = search_input)
        
        context['search_input'] = search_input
        return context
        

# def home(request):
#     tasks = Task.objects.all()
#     context = {
#         'tasks':tasks
#     }
#     return render(request, 'home/index.html', context)


class Detail(LoginRequiredMixin, DetailView):
    model =Task
    template_name = 'home/details.html'
    context_object_name = 'task'


# def detail(request,id):
#     task = get_object_or_404(Task, id=id)
#     context = {
#         'task':task
#     }
#     return render(request, 'home/details.html', context)


class Create(LoginRequiredMixin, CreateView):
    model =Task
    template_name = 'home/createform.html'
    form_class = CreateClass
    success_url =  reverse_lazy('home')

    #passing in the user authmaticaly
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Create, self).form_valid(form)


# def create(request):
#     form = CreateClass(request.POST or None)

#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect ('home')
#     context = {
#         "form":form
#     }
#     return render(request, 'home/createform.html', context)

class Update(LoginRequiredMixin, UpdateView):
    model = Task
    # form_class = CreateClass
    fields = ['title', 'desciption', 'complete']
    template_name = 'home/update.html'
    success_url = reverse_lazy('home')

    #passing in the user authmaticaly
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Update, self).form_valid(form)

class Delete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'home/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('home')
