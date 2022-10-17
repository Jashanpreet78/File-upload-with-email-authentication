from django.shortcuts import render, redirect
from django.http import HttpResponse  
from django.views import generic
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .forms import FileForm,SignUpForm
from .models import File
from django.contrib.auth.forms import User
import PyPDF2,os

from django.core.exceptions import *
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.core.mail import EmailMessage  

from django.contrib.auth import get_user_model




class Home(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'

# uploading the file
@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

# listing
def file_list(request):
    try:
        files = File.objects.filter(user=request.user.id)
        return render(request, 'file_list.html', {
            'files': files
        })
    except ObjectDoesNotExist:
        print('not found')

# upload the file along with showing of list of files
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_form = form.save(commit=False)
            uploaded_file = request.FILES['pdf']
            # breakpoint()
            file_form.file_name = uploaded_file.name
            page_count=open('/home/jashanpreet/Downloads/'+uploaded_file.name,'rb')
            readpdf= PyPDF2.PdfFileReader(page_count)
            file_form.page_count=readpdf.numPages
            # print(totalpages)
            # file_form.file_size = os.path.getsize('/home/jashanpreet/Downloads/'+uploaded_file.name)
            file_form.file_size = uploaded_file.size

            file_form.user = request.user
            file_form.save()
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'upload_file.html', {
        'form': form
    })

# deleting the file view
def delete_file(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('file_list')

# updating the file view
def update_pdf(request,pk):
    if request.method=='POST':
        file=File.objects.get(pk=pk)
        fm=FileForm(request.POST,instance=file)
        if fm.is_valid():
            fm.save()
    else:
        file=File.objects.get(pk=pk)
        fm=FileForm(request.POST,instance=file)
    return render(request,'file_list.html',{'file':file,
        'form':fm})


#view for sign in authentication
def signup(request):
    form=UserCreationForm()
    if request.method== 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect('home')
    
    return render(request,'signup.html',{'form':form})

def user_profile(request):
    return render(request,'registration/edit_profile.html')

# edit_profile
class UserEditView(generic.UpdateView):
    form_class= SignUpForm
    template_name='registration/edit_profile.html'
    success_url=reverse_lazy('home')

    def get_object(self):
        return self.request.user




# signup for email authentication
def signup(request):  
    if request.method == 'POST':  
        form = SignUpForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignUpForm()  
    return render(request, 'signup.html', {'form': form})  


# activation
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  