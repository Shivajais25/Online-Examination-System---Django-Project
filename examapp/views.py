from django.core.paginator import Paginator     #here we import library to access pagination in test module
from django.shortcuts import render, redirect, get_object_or_404
from examapp.models import Candidate ,Subject , Question     #model/table name
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout   #built-in authentication module
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required  #here we are importing decorators 
from .models import UserProfile, Result
# Create your views here.
 #Here is the code which is default page of our website
def home(request):
    return render(request, "examapp/Home.html")

#register page view 
def register(request):                 
    if request.method=="POST":
        uname=request.POST.get("username")
        eid=request.POST.get("email")
        pwd=request.POST.get("password")

        #below authorization and authentication is performed

        user=User.objects.filter(email=eid)
        if user.exists():               # this block of code executed when user enter eid and it is already registered
            messages.error(request, "User Already Exists Please Use Another Name")
            return redirect("/register")
        else:                          #this block of code executed when if block condition become false
            usr=User(username=uname, email=eid, password=pwd )
            usr.set_password(pwd)      #set_password used to make user password secure and safe
            usr.save()                 #this is used to save data in DB
            messages.info(request, "Successfully Registered With Us To Continue Login Here")
            return redirect("/login/")
    return render(request, "examapp/Register.html")

    #.................

 #Here is the code which is login page to authenticate users

def login(request):  
    if request.method=="POST":
        uname=request.POST.get("username")
        pwd=request.POST.get("password")
        user=User.objects.filter(username=uname)
        if not user.exists():
            messages.error(request, "Wrong Username/Username not found")
            return redirect("/login/")
        user=authenticate(username=uname, password=pwd)
        if user is None:
            messages.error(request, "Wrong Password")
            return redirect("/login/")
        else:
            auth_login(request, user)
            return redirect("/dashboard/")        #home page ki location dena hoga

    return render(request, "examapp/Login.html")

#logout page view
def logout(request):
    auth_logout(request)
    return redirect('/login/')


#dashboard page view``
def dashboard(request):
    return render(request, "examapp/Dashboard.html")

#below is the subject_list view which shows the list of subjects whose test is available
def exam(request):
    subjects=Subject.objects.all()
    return render(request, "examapp/Subject_list.html", {'subjects': subjects})

def start_exam(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject).order_by('id')

    if request.method == 'POST':
        answers = {}
        for question in questions:
            selected_key = request.POST.get(f'q{question.id}')
            if selected_key:
                selected_text = getattr(question, selected_key, None)
                answers[str(question.id)] = selected_text
        request.session['answers'] = answers
        return redirect('submit_exam', subject_id=subject.id)

    return render(request, 'examapp/start_exam.html', {
        'subject': subject,
        'questions': questions
    })


def submit_exam(request, subject_id):
    
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)

    answers = request.session.get('answers', {})
   
    score = 0
    total = questions.count()
    result_details = []

    for question in questions:
        user_ans = answers.get(str(question.id))
        correct_ans = getattr(question, 'correct_option', None)  # safe way
        is_correct = user_ans == correct_ans
        if is_correct:
            score += 1
        result_details.append({
            'question': question,
            'selected': user_ans,
            'correct': correct_ans,
            'is_correct': is_correct
        })

    percentage = round((score / total) * 100, 2) if total > 0 else 0
    request.session.pop('answers', None)

    #  SAVE RESULT TO DATABASE
    if request.user.is_authenticated:
        Result.objects.create(
            user=request.user,
            subject=subject,
            score=score,
            total_questions=total
        )

    return render(request, 'examapp/result.html', {
        'subject': subject,
        'score': score,
        'total': total,
        'percentage': percentage,
        'result_details': result_details,
    })


#to make profile module responsive
@login_required     #to access profile module login is required
def profile_view(request):
    # ✔ Create user profile if it doesn't exist
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserForm(instance=request.user)
        p_form = ProfileForm(instance=profile)
    
    return render(request, 'examapp/profile.html', {'u_form': u_form, 'p_form': p_form})


#below is the view of about_us url

def about_us(request):
    return render(request, 'examapp/about_us.html')

#below is the view of result url 
@login_required
def result_list(request):
    user_results = Result.objects.filter(user=request.user).order_by('date')  # latest first
    return render(request, 'examapp/result_list.html', {'results': user_results})

#below is the view of contact url
def contact(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phn=request.POST.get("phn")
        message = request.POST.get('message')

        if name and email and message:
            # Yahan pe database save nahi kar rahe
            # Sirf thank you message dikhana hai
            success = True

    return render(request, 'examapp/contact.html', {'success': success})
