from django.shortcuts import render, get_object_or_404
from .models import Profile, Job
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import JobForm, UserForm


# home page
def index(request):
    all_jobs = Job.objects.all()
    context = {
        'all_jobs': all_jobs,
    }
    return render(request, 'turk/index.html', context)


# profile page
def detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    return render(request, 'turk/detail.html',  {'profile': profile})


def job_description(request, profile_id, job_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    job = Job.objects.get(pk=job_id)
    context = {
        'profile': profile,
        'job': job,
    }
    return render(request, 'turk/job_description.html', context)


def create_job(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    form = JobForm()
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'turk/create_job.html', context)
    # profile = get_object_or_404(Profile, pk=profile_id)
    # return render(request, 'turk/create_job.html', {'profile': profile})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {"form": form}
    return render(request, 'turk/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_jobs = Job.objects.all()
                context = {
                    'all_jobs': all_jobs,
                }
                return render(request, 'turk/index.html', context)
            else:
                return render(request, 'turk/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'turk/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'turk/login.html')


class UserFormView(View):
    form_class = UserForm
    template_name = 'turk/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username'] # 'username' = field
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_active = False
            user.save()

            # request User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    all_jobs = Job.objects.all()
                    context = {
                        'all_jobs': all_jobs,
                    }
                    return render(request, 'turk/index.html', context)

        return render(request, self.template_name, {'form': form})

