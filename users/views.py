from django.shortcuts import render,redirect,HttpResponse
from users.forms import CustomRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from users.forms import EditProfileForm,loginForm,AssignROleForm,CreateGroup,PasswordChangeView,CustomPasswordResetConfirmForm,CustomPasswordChangeForm,CustomPasswordResetForm
from core.views import home_event_data


# from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from events.models import Event 
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import TemplateView,UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
User = get_user_model()
# from users.models import UserProfile
# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def register(request):
    if request.method == "GET":
        form = CustomRegistrationForm()
    elif request.method == "POST":
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()

            return redirect('sign-in') 
    return render(request,'registration/register.html',{'form':form})
def sign_in(request):
    form = loginForm()
    if request.method == "POST":
        form = loginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request,user)
                return redirect ('home')
        
            else:
                return HttpResponse("user is not active!")
        else:
            print('Form errors:',form.errors)

    return render (request,'registration/login.html',{'form':form})
@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')
    return redirect('sign-in')
@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request,'admin/admin_dashboard.html',{'users':users})

def activate_user(request, user_id, token):
    user = get_object_or_404(User, id=user_id) 
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('sign-in')
        # return HttpResponse("Account activated successfully!")
    return HttpResponse("Invalid activation link", status=400)
@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    
    form = AssignROleForm()
    if request.method=='POST':
        form = AssignROleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect ('admin-dashboard')
    return render(request,"admin/assign_role.html",{'form':form})
@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroup()
    if request.method =='POST':
        form = CreateGroup(request.POST)
        if form.is_valid():
            group = form.save()

            return redirect('create-group')
            
    return render(request,'admin/create_group.html',{'form':form})
@user_passes_test(is_admin,login_url='no-permission')
def view_group(request):
    groups = Group.objects.all()
    return render(request,'admin/group_list.html',{'groups':groups})
@method_decorator(login_required, name='dispatch')
class user_profile(TemplateView):
    template_name = 'accounts/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username 
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        context['phone_number'] = user.phone_number
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
class ChangePasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context
 
    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
     model = User
     form_class = EditProfileForm
     template_name = 'accounts/update_profile.html'
     context_object_name='form'

     def get_object(self):
          return self.request.user
    #  def get_form_kwargs(self):
    #       kwargs =  super().get_form_kwargs()
    #       kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
    #       return kwargs

    #  def get_context_data(self, **kwargs):
    #       context = super().get_context_data(**kwargs)
    #       user_profile = UserProfile.objects.get(user=self.request.user)
    #       print("views",user_profile)
    #       context ['form'] = self.form_class(instance = self.object, userprofile = user_profile)

        #   return context
     def form_valid(self,form):
          form.save(commit=True)
          return redirect ('profile')

# class CustomResetPasswordViews(PasswordResetView):
#      template_name = 'registration/reset_password.html'
#      form_class = CustomResetPasswordView
#      success_url = reverse_lazy('sign-in')
#      html_email_template_name = 'registration/reset_email.html'

#      def get_context_data(self, **kwargs):
#          context =  super().get_context_data(**kwargs)
#          context['protocol'] = 'https' if self.request.is_secure() else 'http'
#          context['domain'] = self.request.get_host()
#          return context
#      def form_valid(self, form):
#          messages.success(self.request,'A Reset email sent. Please check your email')
#          return super().form_valid(form)
# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#            form_class = CustomPasswordResetConfirm
#            template_name = 'registration/reset_password.html'
#            success_url = reverse_lazy('sign-in')

#            def form_valid(self, form):
#               messages.success(self.request, 'Password reset successfully')
#               return super().form_valid(form)