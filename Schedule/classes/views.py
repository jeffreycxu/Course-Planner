from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from classes.forms import HomeForm, DeleteNewForm, SignUpForm

# Create your views here.
from django.http import HttpResponse
from .models import Course #MUST IMPORT IF YOU WANT TO USE THE MODEL
from classes.models import Post
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, logout as auth_logout, login as auth_login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from .models import New
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url


class HomeView(TemplateView):
    template_name = "classes/index.html"
    def get(self,request):
         courses = Course.objects.all()
         classes = Post.objects.all()
         print(classes)
         context = {
            "title": "Your Schedule",
            "courses": courses,
            "classes": classes,
            'form': HomeForm(),
            'user': request.user
         }
         return render(request, self.template_name, context)

    def post(self, request):
        form = HomeForm(request.POST) # fill it with the data inputed
        print("hi")
        if form.is_valid():
            form.save(commit = False)
            class_name = form.cleaned_data['class_name']
            credit = form.cleaned_data['credits']
            Post.objects.create(
                class_name= class_name,
                credits=credit,
                student=request.user  # <- and here
            )
            return redirect("homepage") #so it loads the get method again
            args = {
                "classes": class_name,
                "credit": credit, 
                'form': HomeForm()  #still need the form to be rendered
            }
        else:
            classes = Post.objects.all()
            args = {
              "classes": classes,
              'form': HomeForm()  
            }
        return render(request, self.template_name, args)

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'classes/reg_form.html', {'form': form})

def delete(request, **kwargs):
    str = request.GET.get('class_name', None)
    course = get_object_or_404(Post, class_name = str[1:])
    course.delete()
    return redirect("homepage")

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    courses = Course.objects.all()
    context = {
        "title": "Your Schedule",
        "courses": courses
    }
    return render(request, 'classes/index.html', context)

def details(title):
    courses = Course.objects.all()


def validate_course(request):
    class_name = request.GET.get('class_name', None)
    data = {
        'is_taken': Post.objects.filter(class_name__iexact=class_name).exists()
    }
    return JsonResponse(data)


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/classes'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = '/'
        if not is_safe_url(url=redirect_to, allowed_hosts = self.request.get_host(), require_https=False):
            redirect_to = self.success_url
        return redirect_to
