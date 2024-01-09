# django
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import ListView, DetailView, UpdateView, CreateView

# models
from .models import *

# forms
from .forms import *

# python library
from datetime import datetime, timedelta
import os
import re
import zipfile
import shutil

# custom
from fillow import emlExtracter
from fillow.msgToEml import load
from .gpt import *
from .translation import *
from .spam_detection import *

# 분류된 이메일 현황 받기
def get_most_category(id):
    # 이 부분은 DB에서 불러오기
    
    unread_emails = Email.objects.filter(read=False, user_id=id)
    labels = ["결재승인", "휴가", "진행업무", "회의", "보고", "스크랩", "공지", "감사인사", "기타"]
    email_counts = []
    total = 0
    
    for label in labels:
        count = len(unread_emails.filter(category=label))
        total += count
        email_counts.append(count)
    
    # 그래프 색상
    color = [
        "#fc2e53",
		"#ffbf00",
		"#09bd3c",
		"#128a7e",
		"#369fc2",
		"#ffa7d7",
		"#6238fc",
		"#d653c1",
		"#c8c8c8",
    ]
    
    zip_ = zip(labels, email_counts, color)
    
    result = {
        "email_count": {
            "total" : total,
            "data": {
                "labels": labels,
                "count": email_counts,
                "zip": list(zip_),
            }
        }
    }
    return result




# 일정 불러오기
def get_schedule(request):
    # DB에서 일정 불러오기
    json_raw = request.user.additionalinform.schedule
   
    # json 파싱
    schedule_list = json.loads(json_raw.replace("\'", "\""))
   
    return schedule_list


def get_7_deadline(request):
    schedule = get_schedule(request)
    result = []
    
    today = datetime.now()
    
    for s in schedule[:]:
        deadline = s.get('end')
        if deadline:
            deadline = datetime.strptime(deadline, '%Y-%m-%d')
            
            diff = (deadline - today).days + 1
            
            if not s.get('category'):
                s['category'] = '사용자일정'

            if diff > 0 and diff < 7:
                s['diff'] = diff
                s['diff_percent'] = 100 - diff / 7 * 100
                result.append(s)
        
    result.sort(key=lambda x: x['diff'])
    return result[:]

# 할일현황 raw 데이터 불러오기
def deadlinein7_tasks(schedule_list):
   
    result = {i: 0 for i in range(8)}# Default to 0 for each key
    today = datetime.now()

    for schedule in schedule_list:
        deadline_str = schedule.get('end')
        if deadline_str:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            diff = (deadline - today).days + 1

            # Include emails with deadlines within the next 7 days
            if 0 <= diff <= 7:
                result[diff] += 1

    # 일자별로 수정
    todo_in_7 = result.copy()

    return todo_in_7

def get_recent_email(id):
    unread_emails = Email.objects.filter(read=False, user_id=id)
    sorted_data = unread_emails.order_by('-email_date')
    
    return {
        'email_recent':
        sorted_data[:5]
    }

# DB에 변경된 일정 반영하기
def save_schedule(schedule_json, user):
    inform = user.additionalinform
    inform.schedule = json.dumps(schedule_json['schedule'])
    inform.save()
    return


def home(request):
    context={
        "page_title":"홈",
    }
    return render(request,'fillow/home/home.html',context)




def index(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    if request.user.is_authenticated:
        # 로그인이 된 상태에서 해당 유저의 id가 fillow_additionalinform 테이블의 user_ptr_id에 존재하는지 확인
        if not AdditionalInform.objects.filter(user_id=request.user.id).exists():
            # 존재하지 않는다면 additionalinform 웹페이지로 리다이렉트
            return redirect('fillow:additional_info')
    
    most = get_most_category(request.user.id)
    recent = get_recent_email(request.user.id)
    deadline = get_7_deadline(request)
    schedule_list = get_schedule(request)
    tasks = deadlinein7_tasks(schedule_list)
    tasks_sum = sum(tasks.values())

    print(tasks_sum)
    context={
        "page_title":"",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
        "deadline":deadline,
        "tasks" : tasks,
        "tasks_sum": tasks_sum,
    }
    
    context.update(most)
    context.update(recent)
        
    return render(request,'fillow/index.html', context)





def fillow_additionalinform(request):
    if request.method == "POST":
        form = AdditionalInformForm(request.POST)
        if form.is_valid():
            # 로그인된 사용자의 추가 정보를 저장
            additional_inform = form.save(commit=False)
            additional_inform.user = request.user
            additional_inform.phone = form.cleaned_data['phone']
            additional_inform.save()
            return redirect("fillow:index")
    else:
        form = AdditionalInformForm()
    
    return render(request, 'fillow/pages/page-additionalinform.html', {'form': form})





def check_password_(request):
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    if request.session.get('setting_checked'):
        return redirect('fillow:profile')
    
    if request.method == 'POST':
        form = PasswordConfirmationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user  # 현재 로그인된 사용자를 가져옵니다.
            if check_password(password, user.password):
                request.session['setting_checked'] = True
                return redirect('fillow:profile')
            else:
                # 비밀번호가 일치하지 않는 경우
                msg = '비밀번호가 일치하지 않습니다'
                return render(request, 'fillow/apps/profile/check-password.html', {'form': form, 'msg': msg})
    else:
        form = PasswordConfirmationForm()
    return render(request, 'fillow/apps/profile/check-password.html', {'form': form})





def app_profile(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    if not request.session.get('setting_checked'):
        raise PermissionDenied
        
    user_id = request.user.id
    inform = AdditionalInform.objects.get(user_id=user_id)
    user = User.objects.get(id=user_id)
    
    if request.method=="POST":
        action = request.POST.get("btn-post")
        if action=="edit":
            inform.introduce = request.POST.get("about")
            inform.department = request.POST.get("dept")
            inform.phone = request.POST.get("phone")
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            
            user.save()
            inform.save()
        
        elif action=="password":
            password = request.POST.get("password")
            password_confirm = request.POST.get("password_confirm")
            
            try:
                validate_password(password)
                
                if password != password_confirm:
                    raise ValidationError('비밀번호가 일치하지 않습니다.')
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
            except ValidationError as e:
                context={
                    "page_title":"프로필",
                    "company":inform.company,
                    "dept":inform.department,
                    "phone":inform.phone,
                    "introduce":inform.introduce,
                    "img":inform.image,
                    "masking_name":request.user.first_name[1:],
                    "msg": e,
                }
                return render(request, 'fillow/apps/profile/profile.html', context)
            
        elif request.FILES['image']:
            img = request.FILES['image']
            inform.image = img
            inform.save()
            
        return redirect("fillow:profile")
    
    
    context={
        "page_title":"프로필",
        "company":inform.company,
        "dept":inform.department,
        "phone":inform.phone,
        "introduce":inform.introduce,
        "img":inform.image,
        "masking_name":request.user.first_name[1:],
    }
    
    return render(request,'fillow/apps/profile/profile.html',context)


def email_compose(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
        
    email_compose_tpl = EmailComposeTpl.objects.filter(user=request.user).last()
    
    context={
        "page_title":"이메일 전송",
        "email_compose_tpl": email_compose_tpl,
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    if request.method == "POST":
        form = EmailComposeForm(request.POST)
        if form.is_valid():
            user = request.user
            email_to = form.cleaned_data.get('email_to', '')
            email_cc = form.cleaned_data.get('email_cc', '')
            email_subject = form.cleaned_data.get('email_subject', '')
            email_file = form.cleaned_data.get('email_file', '')
            email_text_content = form.cleaned_data.get('email_text_content', '')
            EmailCompose.objects.create(email_to = email_to, email_cc=email_cc, email_subject=email_subject, 
                                        email_file=email_file, email_text_content=email_text_content, user = user)
                
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Save the reply email
            compose_email = Email.objects.create(
                email_from = user.email,
                email_to=email_to,
                email_cc=email_cc,
                email_subject=email_subject,
                email_file=email_file,
                email_text_content=email_text_content,
                email_date = current_date,
                user=user,
                sent = True,
                read = True,
            )
            return redirect("fillow:email-sent")

        else:
            print(form.errors)
            
    else:
        form = EmailComposeForm()
    
    return render(request,'fillow/apps/email/email-compose.html',context)

    

def email_reply(request, pk):
    # Retrieve the Email object
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    original_email = get_object_or_404(Email, pk=pk)
    email_compose_tpl = EmailComposeTpl.objects.filter(user=request.user).last()
    
    context={
        "page_title":"이메일 전송",
        "email_compose_tpl": email_compose_tpl,
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    
    if request.user == original_email.user:
        if request.method == "POST":
            form = EmailComposeForm(request.POST)
            if form.is_valid():
                # Create a new email as a reply
                user = request.user
                email_to = form.cleaned_data.get('email_to', '')
                email_cc = form.cleaned_data.get('email_cc', '')
                email_subject = form.cleaned_data.get('email_subject', 'Re: ' + original_email.email_subject)
                email_file = form.cleaned_data.get('email_file', '')
                email_text_content = form.cleaned_data.get('email_text_content', '')
                EmailCompose.objects.create(email_to = email_to, email_cc=email_cc, email_subject=email_subject, 
                                        email_file=email_file, email_text_content=email_text_content, user = user)
                
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Save the reply email
                reply_email = Email.objects.create(
                    email_from = user.email,
                    email_to=email_to,
                    email_cc=email_cc,
                    email_subject=email_subject,
                    email_file=email_file,
                    email_text_content=email_text_content,
                    email_date = current_date,
                    user=user,
                    sent = True,
                    read = True,
                    category = original_email.category,
                    company_yn = original_email.company_yn,
                    department_yn = original_email.department_yn,
                    #reply_to=original_email  # Reference to the original email
                )

                # Update the 'reply_yn' attribute of the original email to True
                original_email.reply_yn = True
                original_email.reply_date = current_date
                original_email.save()
                # update_schedule
                temp = upload_schedule(request.user, original_email)
                # edit
                save_schedule({'schedule': temp}, request.user)
                # Add a success message (optional)
                messages.success(request, 'Reply sent successfully.')

                return redirect('fillow:email_list')
            else:
                print(form.errors)
        else:
            form = EmailComposeForm(initial={
                'email_to': original_email.email_from,
                'email_subject': 'Re: ' + original_email.email_subject,
                'email_text_content': original_email.email_text_content,
            })

        return render(request, 'fillow/apps/email/email-reply.html', {'context': context, 'original_email': original_email})
    else:
        messages.error(request, 'You do not have permission to reply to this email.')
        return redirect('fillow:email_list')  


def email_compose_tpl(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    context={
        "page_title":"전송 템플릿",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    if request.method == "POST":
        form = EmailComposeTplForm(request.POST)
        if form.is_valid():
            user = request.user
            texts = form.cleaned_data.get('texts', '')
            EmailComposeTpl.objects.create(texts = texts, user = user)
                        
            return redirect("fillow:email-compose-tpl")

    else:
        form = EmailComposeTplForm()
    
    
    return render(request,'fillow/apps/email/email-compose-tpl.html',context)



def email_inbox(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    context={
        "page_title":"받은 이메일",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    return render(request,'fillow/apps/email/email-inbox.html',context)


def email_read(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    context={
        "page_title":"내용 보기",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    return render(request,'fillow/apps/email/email-read.html',context)


def email_sent(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    context={
        "page_title":"보낸 이메일",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    return render(request,'fillow/apps/email/email-sent.html',context)


def faq(request):
    context={
        "page_title":"FAQ",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    return render(request,'fillow/apps/cs/faq.html',context)


def qna(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
        
    user_id = request.user.id
    user_staff = request.user.is_staff
    
    if user_staff:
        Qnas = Qna.objects.all().order_by("-edit_date")
    else:
        Qnas = Qna.objects.filter(user_id=user_id).order_by('-edit_date') 

    if request.method == "POST":
        action = request.POST.get('btn_action')
        if action == "close":
            return redirect("fillow:qna")
        
        title = request.POST.get("title1")
        question = request.POST.get("question")
        edit_date = datetime.now()
        
        # field 비워져있을 때
        if not question or not title:
            return redirect("fillow:qna")
        
        Qna.objects.create(question = question, title = title, user_id = user_id, edit_date = edit_date)
        
        return redirect("fillow:qna")
    else:
        action = request.GET.get('btn-search')
        if action=="reset":
            title=""
            status=0
            form = QnaSearchForm()
        else:
            prev_title = request.GET.get('title')
            prev_status = request.GET.get('status')
            # print(prev_title, prev_status)
            
            if not prev_title and not prev_status:
                # 제목, 상태에 아무 것도 없을 때 or 처음 QnA 사이트 들어왔을 때
                form = QnaSearchForm()
                prev_title, prev_status = "", 0
            else:
                # 제목, 상태에 뭔가 넣었었을 때
                if not prev_title:
                    prev_title=""
                if not prev_status:
                    prev_status=0
                else:
                    if prev_status=="0":
                        prev_status=0
                    elif prev_status=="1":
                        prev_status=1
                    else:
                        prev_status=2
                
                form = QnaSearchForm(initial={'title': prev_title, 'status': prev_status})
            
                
            title, status = prev_title, prev_status
            
            if title=="" and not status:
                Qnas = Qnas
            elif title=="" and status:
                if status==1:
                    Qnas = Qnas.filter(
                        Q(answer="")
                    )
                else:
                    Qnas = Qnas.filter(
                        ~Q(answer="")
                    )
            elif title!="" and not status:
                Qnas = Qnas.filter(
                    Q(title__icontains=title)
                )
            elif title!="" and status:
                if status==1:
                    Qnas = Qnas.filter(
                        Q(answer="") & Q(title__icontains=title)
                    )
                else:
                    Qnas = Qnas.filter(
                        ~Q(answer="") & Q(title__icontains=title)
                    )
            
    paginator = Paginator(Qnas, 10)

    page_num = request.GET.get('page')
    qnas_page = paginator.get_page(page_num)
    
    
    context={
        "page_title":"Q&A",
        "form": form,
        "Qnas":qnas_page,
        "title":title,
        "status":status,
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    return render(request,'fillow/apps/cs/qna.html',context)
    


def qna_details(request, id):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    qna = get_object_or_404(Qna, id=id)
    
    # url로 직접 접근 하는 거 막기 - 404 띄우기
    if not request.user.is_staff and qna.user_id != request.user.id:
        return redirect("fillow:page-error-404")
    
    context={
        "page_title":"Q&A",
        "qna":qna,
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    if request.method == "POST":
        qna.delete()
        return redirect("fillow:qna")
    
    
    return render(request, 'fillow/apps/cs/qna_details.html',context)

def qna_details2(request, id):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    qna = get_object_or_404(Qna, id=id)
    
    # url로 직접 접근 하는 거 막기 - 404 띄우기
    if not request.user.is_staff and qna.user_id != request.user.id:
        return redirect("fillow:page-error-404")
    
    context={
        "page_title":"Q&A",
        "qna":qna,
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    if request.method == "POST":
        action = request.POST.get("btn-act")
        if action=="edit":
            qna.title = request.POST.get("title1")
            qna.question = request.POST.get("question")
            qna.edit_date = datetime.now()
            qna.save()
            return redirect("fillow:qna-details", id=id)
        else:
            qna.answer = request.POST.get("answer")
            qna.edit_date = datetime.now()
            qna.save()
            return redirect("fillow:qna-details", id=id)
    
    return render(request, 'fillow/apps/cs/qna_details2.html',context)


# 일정 불러오기
def get_schedule(request):
    
    # DB에서 일정 불러오기
    json_raw = request.user.additionalinform.schedule
    
    # json 파싱
    schedule_list = json.loads(json_raw.replace("\'", "\""))
    
    return schedule_list

# 배정, 비배정 일정 분리하기
def sep_schedule(schedule_list):
    # 달력에 배정 된 일정
    in_calendar = []
    # 배정되지 않은 일정
    not_in_calendar = []
    
    # 받아온 일정 리스트에서 end 속성이 없는(배정이 되지 않은) 일정 분리
    for schedule in schedule_list:
        if (schedule.get('end')):
            in_calendar.append(schedule)
        else:
            not_in_calendar.append(schedule)
    
    return in_calendar[:], not_in_calendar[:]


def schedule(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    

    context={
        "page_title":"일정 관리",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    
    if request.method == "POST":
        # JSON으로 수정된 일정 데이터 받아옴
        received_data = json.loads(request.body.decode('utf-8'))
        
        # DB에 변경사항 올리는 함수
        save_schedule(received_data, request.user)
    
    schedule_list = get_schedule(request)
    
    in_calendar, not_in_calendar = sep_schedule(schedule_list)
        
    context['in_calendar'] = in_calendar
    context['not_in_calendar'] = not_in_calendar
    
    return render(request,'fillow/apps/schedule/schedule.html',context)




def page_register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        additional_form = AdditionalInformForm(request.POST)
        if user_form.is_valid() and additional_form.is_valid():
            # 이메일 중복되는 경우 안되게 가입 안되게 만들기
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                context={
                    'user_form': user_form, 
                    'additional_form': additional_form,
                    'msg': "이미 존재하는 이메일입니다."
                }
                return render(request, "fillow/pages/page-register.html", context)
            
            user = user_form.save()
            additional_inform = additional_form.save(commit=False)
            additional_inform.user = user
            additional_inform.phone = additional_form.cleaned_data['phone']
            additional_inform.save()
        else:
            context={
                'user_form': user_form, 
                'additional_form': additional_form,
                'errors': user_form.errors,
            }
            return render(request, "fillow/pages/page-register.html", context)

        return redirect("fillow:page-register-complete")
    else:
        user_form = UserForm()
        additional_form = AdditionalInformForm()
    return render(request, 'fillow/pages/page-register.html', {'user_form': user_form, 'additional_form': additional_form})





def check_username(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username').strip()
        user_exists = User.objects.filter(username=username).exists()

        return JsonResponse({'available': not user_exists})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def check_email(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email').strip()
        email_exists = User.objects.filter(email=email).exists()

        return JsonResponse({'available': not email_exists})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def page_register_complete(request):
    return render(request, 'fillow/pages/page-register-complete.html')




def page_reset_done(request):
    return render(request, 'fillow/pages/page-reset-done.html')


def page_forgot_password(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except:
                return render(request,'fillow/pages/page-forgot-password.html', {'form': form, 'error': '해당 이메일로 가입된 계정이 없습니다.'})
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = f'http://hyeopjaesea.com/reset/{uid}/{token}'
            with open('static/fillow/email/email_template.htm', 'r') as file:
                html_text = file.read()
            html_text = html_text.replace(r"{{placeholder}}", reset_link)
            
            send_mail(
                subject='HyeopJaeSea 비밀번호 재설정',
                message='',
                from_email='hyeopjaesea@gmail.com',
                recipient_list=[email],
                fail_silently=False,
                html_message=html_text,
            )
            
            return redirect('fillow:page-reset-done')
    else:
        form = CustomPasswordResetForm()
    return render(request,'fillow/pages/page-forgot-password.html', {'form': form})


def page_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        
            if default_token_generator.check_token(user, token):
                password = request.POST['password']
                password_confirm = request.POST['password_confirm']
                
                validate_password(password)
                    
                if password != password_confirm:
                    raise ValidationError('비밀번호가 일치하지 않습니다.')
                user.set_password(password)
                user.save()
                
                return redirect('fillow:page-reset-complete')
        except ValidationError as e:
            return render(request, 'fillow/pages/page-reset-confirm.html', {'msg': e})
        except ValueError:
            raise PermissionDenied
    return render(request, 'fillow/pages/page-reset-confirm.html')


def page_reset_complete(request):
    return render(request, 'fillow/pages/page-reset-complete.html')

def page_error_400(request):
    return render(request,'400.html')
    
def page_error_403(request):
    return render(request,'403.html')

def page_error_404(request):
    return render(request,'404.html')

def page_error_500(request):
    return render(request,'500.html')

def page_error_503(request):
    return render(request,'503.html')



def extract_zip(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for filename in zip_ref.namelist():
            # 파일 이름 인코딩 변환
            correct_filename = filename.encode('cp437').decode('cp949', 'ignore')
            
            # 변환한 파일 이름으로 새 파일 경로 생성
            extracted_path = os.path.join(extract_path, correct_filename)

            # 파일의 디렉토리가 존재하지 않으면 생성
            os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
            
            # 파일 추출
            with zip_ref.open(filename) as source, open(extracted_path, "wb") as target:
                shutil.copyfileobj(source, target)
        
def process_msg_file(eml_name, user):
    headers = ['file_name','Subject','Date','From','To','Cc','text_content']
   
    result = emlExtracter.prcessing_dir(headers, eml_name)
    print(eml_name,headers)
    # print("asd",result)
    # print("asd",result['text_content'])
    if detect_spam(translate(result['text_content'])) == "spam":
        # 휴지통으로 보내기
        
        spam=True
        email_date_tuple = result.get('Date', '')
        email_date_str = ''.join(map(str, email_date_tuple))
    
        # Remove all spaces from the date string
        email_date_str = re.sub(r'\s+', '', email_date_str)
    
        # Parse the date
        email_date = datetime.strptime(email_date_str, '%a,%d%b%Y%H:%M:%S%z')
        category = "스팸"
        from_company = None
        from_dept = None
        from_name = None
        reply_req_yn = False
        reply_end_date = None
        company_yn = False
        department_yn = False
        meeting_date=None
        
        email_instance = Email(
        user=user,
        email_file_name=result.get('file_name', ''),
        email_subject=result.get('Subject', ''),
    
        email_date=email_date,
        email_from=result.get('From', ''),
        email_to=result.get('To', ''),
        email_cc=result.get('Cc', ''),  
        email_text_content=result.get('text_content', ''),
        category = category,
        from_company = from_company,
        from_dept = from_dept,
        from_name = from_name,
        reply_req_yn = reply_req_yn,
        reply_start_date = result.get('Date',''),
        reply_end_date = reply_end_date,
        company_yn = company_yn,
        department_yn = department_yn,
        meeting_date=meeting_date,
        read=True,
        spam=spam,
        )
        
        email_instance.save()
    else:
        
        gpt_result = process_file(result['text_content'])
    
        reply_req_yn = gpt_result.get('회신요청여부','')
        reply_req_yn = True if reply_req_yn == 'Y' else False
    
        user_additional_info = AdditionalInform.objects.filter(user=user).last()
    
        from_company = gpt_result.get('회사', '')
        user_company = user_additional_info.company
        company_yn = True if from_company == user_company else False
    
        from_dept = gpt_result.get('부서', '')
        user_dept = user_additional_info.department
        dept_yn = True if from_dept == user_dept else False
        email_date_tuple = result.get('Date', '')
        email_date_str = ''.join(map(str, email_date_tuple))
    
        # Remove all spaces from the date string
        email_date_str = re.sub(r'\s+', '', email_date_str)
    
        # Parse the date
        email_date = datetime.strptime(email_date_str, '%a,%d%b%Y%H:%M:%S%z')
    
        meeting_date=gpt_result.get('회의날짜', '')
        current_year = datetime.now().year
        current_month = datetime.now().month
        month_match = re.search(r'(\d+)월', meeting_date)
        if month_match and '년' not in meeting_date:
            meeting_month = int(month_match.group(1))
            # 현재 월보다 작은 경우, 연도를 다음 해로 설정합니다.
            if meeting_month < current_month:
                meeting_date = f"{current_year + 1}년 {meeting_date}"
            else:
                # 그렇지 않으면 현재 연도를 사용합니다.
                meeting_date = f"{current_year}년 {meeting_date}"
        reply_end_date = gpt_result.get('회신마감일자','')
        month_match = re.search(r'(\d+)월', reply_end_date)
        if month_match and '년' not in reply_end_date:
            meeting_month = int(month_match.group(1))
            # 현재 월보다 작은 경우, 연도를 다음 해로 설정합니다.
            if meeting_month < current_month:
                reply_end_date = f"{current_year + 1}년 {reply_end_date}"
            else:
                # 그렇지 않으면 현재 연도를 사용합니다.
                reply_end_date = f"{current_year}년 {reply_end_date}"
        spam=False
 
        email_instance = Email(
        user=user,
        email_file_name=result.get('file_name', ''),
        email_subject=result.get('Subject', ''),
    
        email_date=email_date,
        email_from=result.get('From', ''),
        email_to=result.get('To', ''),
        email_cc=result.get('Cc', ''),  
        email_text_content=result.get('text_content', ''),
        category = gpt_result.get('카테고리',''),
        from_company = from_company,
        from_dept = from_dept,
        from_name = gpt_result.get('이름',''),
        reply_req_yn = reply_req_yn,
        reply_start_date = result.get('Date',''),
        reply_end_date = reply_end_date,
        company_yn = company_yn,
        department_yn = dept_yn,
        meeting_date=meeting_date,
        spam=spam,
        )
        
        email_instance.save()
    if reply_req_yn == True or meeting_date != "없음":
        # 새로운 스케줄을 리스트에 추가
        schedule_list = upload_schedule(user,email_instance)
 
        # Python 객체를 JSON 문자열로 변환하여 저장
        user.additionalinform.schedule = json.dumps(schedule_list)
 
        # 변경 사항을 데이터베이스에 저장
        user.additionalinform.save()

def upload_schedule(user,email):
   
    # JSON 문자열을 Python 객체로 변환
    json_raw = user.additionalinform.schedule
    schedule_list = json.loads(json_raw)
    # DB에서 일정 불러오기
    for event in schedule_list:
        if event.get('pk') == email.id:
            schedule_list.remove(event)
            return schedule_list
    temp=[]
    if email.reply_req_yn==True and email.reply_yn == False:
        dic={
            'pk': email.id,
            'title': email.category + " / " + email.from_name,
            'start': datetime.strptime(email.reply_start_date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d'),
            'end': None if email.reply_end_date == "없음" else datetime.strptime(email.reply_end_date, '%Y년 %m월 %d일').strftime('%Y-%m-%d'),
            'category': email.category,
        }
        temp.append(dic)

    if email.meeting_date != "없음" and email.reply_yn == False and email.spam == False:
        dic={
            'pk': email.id,
            'title': "회의 / " + email.from_name,
            'start': datetime.strptime(email.meeting_date, '%Y년 %m월 %d일').strftime('%Y-%m-%d'),
            'end': (datetime.strptime(email.meeting_date, '%Y년 %m월 %d일') + timedelta(days=1)).strftime('%Y-%m-%d'),
            'category': '회의',
        }
        temp.append(dic)
    schedule_list+=temp
    return schedule_list


def upload_file(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    is_uploaded = False
 
    if request.method == 'POST':
        is_uploaded = True
        form = DocumentForm(request.POST, request.FILES)
 
        if form.is_valid():
            for uploaded_file in request.FILES.getlist('uploaded_file'):
                new_doc = Document(uploaded_file=uploaded_file)
                new_doc.save()
                recent_document = Document.objects.latest('id')
                file_path = recent_document.uploaded_file.path
                # file_path = new_doc.uploaded_file.path
                file_extension = uploaded_file.name.split('.')[-1].lower()
               
                extract_path = os.path.join('media', 'extracted')
               
                if file_extension == 'zip':
                    os.makedirs(extract_path, exist_ok=True)
                    extract_zip(file_path, extract_path)
 
                    for file_name in os.listdir(extract_path):
                        file_path = os.path.join(extract_path, file_name)
                        # eml_name = file_path.split('.msg')[0] + '.eml'
                        file_extension = file_name.split('.')[-1].lower()
                        eml_name = file_path if file_extension == 'eml' else file_path.split('.msg')[0] + '.eml'
                       
                        if file_extension == 'msg':
                            with open(eml_name, "wb") as f:
                                contents = load(open(file_path, "rb"))
                                f.write(contents.as_bytes())
                           
                        process_msg_file(eml_name, request.user)
 
                elif file_extension in ['msg', 'eml']:
                    eml_name = file_path if file_extension == 'eml' else file_path.split('.msg')[0] + '.eml'
                   
                    if file_extension == 'msg':
                        with open(eml_name, "wb") as f:
                            contents = load(uploaded_file)
                            f.write(contents.as_bytes())
                           
                    process_msg_file(eml_name, request.user)
               
                # 압축 해제된 폴더 삭제
                if os.path.exists(extract_path) and os.path.isdir(extract_path):
                    shutil.rmtree(extract_path)
            form = DocumentForm()
 
 
    else:
        form = DocumentForm()
 
    context = {
        'form': form,
        "img": AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name": request.user.first_name[1:],
        "page_title": "이메일 업로드",
        "is_uploaded": is_uploaded,
    }
    return render(request, 'fillow/apps/email/upload.html', context)





class EmailListView(ListView):
    model = Email
    template_name = 'fillow/apps/email/email-inbox.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(spam=False)
        queryset = queryset.filter(sent=False)
        queryset = queryset.filter(trash=False)
        queryset = queryset.filter(user=self.request.user).order_by('-email_date')
        search_query = self.request.GET.get('search_query', '')
        category_filter = self.request.GET.get('category', '')
        internal_filter = self.request.GET.get('internal', '')
        internal_filter_d = self.request.GET.get('internal_d', '')
        
        if search_query:
            queryset = queryset.filter(Q(email_subject__icontains=search_query) | Q(from_name__icontains=search_query))
        
        
        if category_filter:
            queryset = queryset.filter(category=category_filter)
                
        if internal_filter in ['0', '1']:
            internal_filter = int(internal_filter)
            queryset = queryset.filter(company_yn=internal_filter)
            
        if internal_filter_d in ['0', '1']:
            internal_filter_d = int(internal_filter_d)
            queryset = queryset.filter(department_yn=internal_filter_d)
        recipient_filter = self.request.GET.get('recipient', '')
        if recipient_filter in ['to', 'cc']:
            user_email = self.request.user.email
            if recipient_filter == 'to':
                queryset = queryset.filter(email_to=user_email)
            elif recipient_filter == 'cc':
                queryset = queryset.filter(email_cc__contains=user_email)


        self.paginator = Paginator(queryset, 10)  # 페이지당 20개 이메일 표시
        page_number = self.request.GET.get('page')
        self.page_obj = self.paginator.get_page(page_number)
        return self.page_obj.object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_email_count = Email.objects.filter(
            user=self.request.user, read=False
        ).count()
        context['unread_email_count'] = unread_email_count
        context['page_title'] = '받은 이메일'
        context['img'] = AdditionalInform.objects.get(user_id=self.request.user.id).image
        return context

    def render_to_response(self, context, **response_kwargs):
        context.update({
            'paginator': self.paginator,
            'page_obj': self.page_obj,
        })
        return super().render_to_response(context, **response_kwargs)
    
class SpamEmailListView(ListView):
    model = Email
    template_name = 'fillow/apps/email/email-inbox-spam.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(spam=True)
        queryset = queryset.filter(sent=False)
        queryset = queryset.filter(trash=False)
        queryset = queryset.filter(user=self.request.user).order_by('-email_date')
        search_query = self.request.GET.get('search_query', '')
        category_filter = self.request.GET.get('category', '')
        internal_filter = self.request.GET.get('internal', '')
        internal_filter_d = self.request.GET.get('internal_d', '')
        
        if search_query:
            queryset = queryset.filter(Q(email_subject__icontains=search_query) | Q(from_name__icontains=search_query))
        
        
        if category_filter:
            queryset = queryset.filter(category=category_filter)
                
        if internal_filter in ['0', '1']:
            internal_filter = int(internal_filter)
            queryset = queryset.filter(company_yn=internal_filter)
            
        if internal_filter_d in ['0', '1']:
            internal_filter_d = int(internal_filter_d)
            queryset = queryset.filter(department_yn=internal_filter_d)
        recipient_filter = self.request.GET.get('recipient', '')
        if recipient_filter in ['to', 'cc']:
            user_email = self.request.user.email
            if recipient_filter == 'to':
                queryset = queryset.filter(email_to=user_email)
            elif recipient_filter == 'cc':
                queryset = queryset.filter(email_cc__contains=user_email)


        self.paginator = Paginator(queryset, 10)  # 페이지당 20개 이메일 표시
        page_number = self.request.GET.get('page')
        self.page_obj = self.paginator.get_page(page_number)
        return self.page_obj.object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_email_count = Email.objects.filter(
            user=self.request.user, read=False
        ).count()
        context['unread_email_count'] = unread_email_count
        context['page_title'] = '받은 이메일'
        context['img'] = AdditionalInform.objects.get(user_id=self.request.user.id).image
        return context

    def render_to_response(self, context, **response_kwargs):
        context.update({
            'paginator': self.paginator,
            'page_obj': self.page_obj,
        })
        return super().render_to_response(context, **response_kwargs)
    
class SentEmailListView(ListView):
    model = Email
    template_name = 'fillow/apps/email/email-inbox-sent.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sent=True)
        queryset = queryset.filter(trash=False)
        queryset = queryset.filter(user=self.request.user).order_by('-email_date')
        search_query = self.request.GET.get('search_query', '')
        category_filter = self.request.GET.get('category', '')
        internal_filter = self.request.GET.get('internal', '')
        internal_filter_d = self.request.GET.get('internal_d', '')
        
        if search_query:
            queryset = queryset.filter(Q(email_subject__icontains=search_query) | Q(from_name__icontains=search_query))
        
        
        if category_filter:
            queryset = queryset.filter(category=category_filter)
                
        if internal_filter in ['0', '1']:
            internal_filter = int(internal_filter)
            queryset = queryset.filter(company_yn=internal_filter)
            
        if internal_filter_d in ['0', '1']:
            internal_filter_d = int(internal_filter_d)
            queryset = queryset.filter(department_yn=internal_filter_d)
        recipient_filter = self.request.GET.get('recipient', '')
        if recipient_filter in ['to', 'cc']:
            user_email = self.request.user.email
            if recipient_filter == 'to':
                queryset = queryset.filter(email_to=user_email)
            elif recipient_filter == 'cc':
                queryset = queryset.filter(email_cc__contains=user_email)


        self.paginator = Paginator(queryset, 10)  # 페이지당 20개 이메일 표시
        page_number = self.request.GET.get('page')
        self.page_obj = self.paginator.get_page(page_number)
        return self.page_obj.object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_email_count = Email.objects.filter(
            user=self.request.user, read=False
        ).count()
        context['unread_email_count'] = unread_email_count
        context['page_title'] = '보낸 이메일'
        context['img'] = AdditionalInform.objects.get(user_id=self.request.user.id).image
        return context

    def render_to_response(self, context, **response_kwargs):
        context.update({
            'paginator': self.paginator,
            'page_obj': self.page_obj,
        })
        return super().render_to_response(context, **response_kwargs)
    
class EmailListView_Trash(ListView):
    model = Email
    template_name = 'fillow/apps/email/email-trash.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(trash=True)
        queryset = queryset.filter(user=self.request.user).order_by('-email_date')
        self.paginator = Paginator(queryset, 10)  # 페이지당 20개 이메일 표시
        page_number = self.request.GET.get('page')
        self.page_obj = self.paginator.get_page(page_number)
        return self.page_obj.object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_email_count = Email.objects.filter(
            user=self.request.user, read=False
        ).count()
        context['unread_email_count'] = unread_email_count
        context['page_title'] = '휴지통'
        context['img'] = AdditionalInform.objects.get(user_id=self.request.user.id).image
        return context
    def render_to_response(self, context, **response_kwargs):
        context.update({
            'paginator': self.paginator,
            'page_obj': self.page_obj,
        })
        return super().render_to_response(context, **response_kwargs)
    
class EmailDetailView(DetailView):

    model = Email
    template_name = 'fillow/apps/email/email-read.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Get the email object
        email = self.get_object()

        # Check if the email belongs to the logged-in user
        if email.user != self.request.user:
            # If not, redirect to a different page (e.g., email list)
            return redirect('fillow:email_list')  # Adjust the URL name as needed

        # If the email belongs to the user, proceed with the normal dispatch
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.object.read:
            self.object.read = True
            self.object.save()
        context['page_title'] = '자세히'
        return context

def page_register_terms(request):
    if request.method == 'POST':
        # 폼 데이터 검증 및 처리
        return redirect('fillow:page-register')
    return render(request, 'fillow/pages/page-register-terms.html')

def email_trash(request, pk):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    email = Email.objects.get(pk=pk)

    if not email.trash:
        email.trash = True  # 휴지통 상태로 변경
        email.save()
        return redirect("fillow:email-list-trash")

    return redirect("fillow:email-list-trash")

def email_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
    email = Email.objects.get(pk=pk)

    if request.user == email.user:
        email.delete()
        messages.success(request, 'Email permanently deleted.')
        return redirect("fillow:email-list-trash")
    return redirect("fillow:email-list-trash")


def category_change(request, pk, category_name):
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    email = Email.objects.get(pk=pk)

    if request.user == email.user:
        email.category = category_name
        email.save()
        messages.success(request, f'Email category changed to {category_name}.')
        return redirect('fillow:email_list')
    else:
        messages.error(request, 'You do not have permission to change the category of this email.')
        return redirect('fillow:email_list') 

class EmailUpdateView(UpdateView):
    model = Email

    fields = [
        'email_subject',
        'email_from',
        'email_to',
        'email_cc',
        'email_text_content',
    ]


class EmailCreateView(CreateView):
    model = Email
    fields = [
        'email_file_name',
        'email_subject',
        'email_from',
        'email_to',
        'email_cc',
        'email_text_content',
    ]

    def form_valid(self, form):
        form.instance.email_attachments = self.request.FILES['email_attachments']
        return super().form_valid(form)