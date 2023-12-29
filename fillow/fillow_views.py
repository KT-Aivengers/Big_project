from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from fillow.forms import DocumentForm
from .models import Qna, EmailCompose, EmailComposeTpl
import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import UserForm, LoginForm, EmailComposeTplForm, EmailComposeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth import views
from .models import AdditionalInform
from .gpt import process_file

# 분류된 이메일 현황 받기
def get_most_4_category():
    # 이 부분은 DB에서 불러오기
    total = 60
    labels = ["요청", "결재승인", "작업완료", "안내"]
    count = [25, 10, 9, 6]
    
    # 그래프 색상
    color = [
        "var(--primary)",
        "#26E023",
        "#61CFF1",
        "#FFDA7C",
        "#FF86B1",
    ]
    
    sum_ = sum(count)
    
    if sum_ < total:
        labels.append("기타")
        count.append(total - sum_)
    
    zip_ = zip(labels, count, color)
    
    result = {
        "email_count": {
            "total" : total,
            "data": {
                "labels": labels,
                "count": count,
                "zip": list(zip_),
            }
        }
    }
    return result

# 일정 불러오기
def get_schedule(request):
    
    # DB에서 일정 불러오기
    
    emails = Email.objects.filter(user_id=request.user.id, reply_req_yn=True)
    schedule_list = [
    {
        'pk':email.id,
        'title': email.category + " / " + email.email_from,
        'start': email.reply_start_date.strftime('%Y-%m-%d'),
        'end': (email.reply_end_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
        'category': email.category,
    } for email in emails
    ]
    
    
    return schedule_list


# DB에 올리는 코드 여기에 작성
def save_schedule(schedule_json):
    print(schedule_json)
    return


def home(request):
    context={
        "page_title":"홈",
    }
    return render(request,'fillow/home/home.html',context)

from .models import AdditionalInform
def index(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    if request.user.is_authenticated:
        # 로그인이 된 상태에서 해당 유저의 id가 fillow_additionalinform 테이블의 user_ptr_id에 존재하는지 확인
        if not AdditionalInform.objects.filter(user_id=request.user.id).exists():
            # 존재하지 않는다면 additionalinform 웹페이지로 리다이렉트
            return redirect('fillow:additional_info')
    most4 = get_most_4_category()
    context={
        "page_title":"",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    
    context.update(most4)
        
    return render(request,'fillow/index.html', context)



from .forms import AdditionalInformForm

 
def fillow_additionalinform(request):
    if request.method == "POST":
        form = AdditionalInformForm(request.POST)
        if form.is_valid():
            # 로그인된 사용자의 추가 정보를 저장
            additional_inform = form.save(commit=False)
            additional_inform.user = request.user
            additional_inform.save()
            return redirect("fillow:index")
    else:
        form = AdditionalInformForm()
    
    return render(request, 'fillow/pages/page-additionalinform.html', {'form': form})


def index_2(request):
    context={
        "page_title":"메인"
    }
    return render(request,'fillow/index-2.html',context)


def project_page(request):
    context={
        "page_title":"Project"
    }
    return render(request,'fillow/project-page.html',context)


def contacts(request):
    context={
        "page_title":"Contacts"
    }
    return render(request,'fillow/contacts.html',context)


def kanban(request):
    context={
        "page_title":"Kanban"
    }
    return render(request,'fillow/kanban.html',context)


def calendar_page(request):
    context={
        "page_title":"일정 보기"
    }
    return render(request,'fillow/calendar-page.html',context)


def message(request):
    context={
        "page_title":"Message"
    }
    return render(request,'fillow/message.html',context)


def content(request):
    context={
        "page_title":"Content"
    }
    return render(request,'fillow/cms/content.html',context)


def add_content(request):
    context={
        "page_title":"Add Content"
    }
    return render(request,'fillow/cms/add-content.html',context)


def menu(request):
    context={
        "page_title":"Menu"
    }
    return render(request,'fillow/cms/menu.html',context)


def email_template(request):
    context={
        "page_title":"Email Template"
    }
    return render(request,'fillow/cms/email-template.html',context)


def add_email(request):
    context={
        "page_title":"Add Email"
    }
    return render(request,'fillow/cms/add-email.html',context)


def blog(request):
    context={
        "page_title":"Blog"
    }
    return render(request,'fillow/cms/blog.html',context)


def add_blog(request):
    context={
        "page_title":"Add Blog"
    }
    return render(request,'fillow/cms/add-blog.html',context)


def blog_category(request):
    context={
        "page_title":"Blog Category"
    }
    return render(request,'fillow/cms/blog-category.html',context)


from django.core.files.storage import FileSystemStorage

def app_profile(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    
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
            user.email = request.POST.get("email")
            
            user.save()
            inform.save()
            
        elif request.FILES['image']:
            img = request.FILES['image']
            inform.image = img
            inform.save()
            
          
        return redirect("fillow:app-profile")
    
    
    context={
        "page_title":"프로필",
        "company":inform.company,
        "dept":inform.department,
        "phone":inform.phone,
        "introduce":inform.introduce,
        "img":inform.image,
        "masking_name":request.user.first_name[1:],
    }
    
    return render(request,'fillow/apps/app-profile.html',context)


def edit_profile(request):
    context={
        "page_title":"Edit Profile"
    }
    return render(request,'fillow/apps/edit-profile.html',context)


def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'fillow/apps/post-details.html',context)


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
            return redirect("fillow:email-compose")

        else:
            print(form.errors)
            
    else:
        form = EmailComposeForm()
    
    return render(request,'fillow/apps/email/email-compose.html',context)

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

from .models import Qna, EmailComposeTpl

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from .forms import QnaSearchForm

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
            print(prev_title, prev_status)
            
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
        elif action=="delete":
            qna.delete()
            return redirect("fillow:qna")
        else:
            qna.answer = request.POST.get("answer")
            qna.edit_date = datetime.now()
            qna.save()
            return redirect("fillow:qna-details", id=id)
    
    return render(request, 'fillow/apps/cs/qna_details2.html',context)


def schedule(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    if request.method == "POST":
        # JSON으로 수정된 일정 데이터 받아옴
        received_data = json.loads(request.body.decode('utf-8'))
        
        # DB에 변경사항 올리는 함수
        save_schedule(received_data)

    context={
        "page_title":"일정 관리",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    
    schedule_list = get_schedule(request)
    # 달력에 배정 된 일정
    in_calendar = []
    # 배정되지 않은 일정
    not_in_calendar = []
    
    # 받아온 일정 리스트에서 start 속성이 없는(배정이 되지 않은) 일정 분리
    for schedule in schedule_list:
        if (schedule.get('end')):
            in_calendar.append(schedule)
        else:
            not_in_calendar.append(schedule)
        
    context['in_calendar'] = in_calendar
    context['not_in_calendar'] = not_in_calendar
    
    return render(request,'fillow/apps/schedule/schedule.html',context)



def app_calender(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
    context={
        "page_title":"일정 수정하기",
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    return render(request,'fillow/apps/app-calendar.html',context)


def ecom_product_grid(request):
    context={
        "page_title":"Product Grid"
    }
    return render(request,'fillow/apps/shop/ecom-product-grid.html',context)


def ecom_product_list(request):
    context={
        "page_title":"Product List"
    }
    return render(request,'fillow/apps/shop/ecom-product-list.html',context)


def ecom_product_detail(request):
    context={
        "page_title":"Product Detail"
    }
    return render(request,'fillow/apps/shop/ecom-product-detail.html',context)


def ecom_product_order(request):
    context={
        "page_title":"Product Order"
    }
    return render(request,'fillow/apps/shop/ecom-product-order.html',context)


def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'fillow/apps/shop/ecom-checkout.html',context)


def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'fillow/apps/shop/ecom-invoice.html',context)


def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'fillow/apps/shop/ecom-customers.html',context)



def chart_flot(request):
    context={
        "page_title":"Chart Flot"
    }
    return render(request,'fillow/charts/chart-flot.html',context)


def chart_morris(request):
    context={
        "page_title":"Chart Morris"
    }
    return render(request,'fillow/charts/chart-morris.html',context)


def chart_chartjs(request):
    context={
        "page_title":"Chart Chartjs"
    }
    return render(request,'fillow/charts/chart-chartjs.html',context)


def chart_chartist(request):
    context={
        "page_title":"Chart Chartist"
    }
    return render(request,'fillow/charts/chart-chartist.html',context)


def chart_sparkline(request):
    context={
        "page_title":"Chart Sparkline"
    }
    return render(request,'fillow/charts/chart-sparkline.html',context)


def chart_peity(request):
    context={
        "page_title":"Chart Peity"
    }
    return render(request,'fillow/charts/chart-peity.html',context)



def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'fillow/bootstrap/ui-accordion.html',context)


def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'fillow/bootstrap/ui-alert.html',context)


def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'fillow/bootstrap/ui-badge.html',context)


def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'fillow/bootstrap/ui-button.html',context)


def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'fillow/bootstrap/ui-modal.html',context)


def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'fillow/bootstrap/ui-button-group.html',context)


def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'fillow/bootstrap/ui-list-group.html',context)


def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'fillow/bootstrap/ui-card.html',context)


def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'fillow/bootstrap/ui-carousel.html',context)


def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'fillow/bootstrap/ui-dropdown.html',context)


def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'fillow/bootstrap/ui-popover.html',context)


def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'fillow/bootstrap/ui-progressbar.html',context)


def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'fillow/bootstrap/ui-tab.html',context)


def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'fillow/bootstrap/ui-typography.html',context)


def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'fillow/bootstrap/ui-pagination.html',context)


def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'fillow/bootstrap/ui-grid.html',context)




def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'fillow/plugins/uc-select2.html',context)


def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'fillow/plugins/uc-nestable.html',context)


def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'fillow/plugins/uc-noui-slider.html',context)


def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'fillow/plugins/uc-sweetalert.html',context)


def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'fillow/plugins/uc-toastr.html',context)


def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'fillow/plugins/map-jqvmap.html',context)


def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'fillow/plugins/uc-lightgallery.html',context)


def widget_basic(request):
    context={
        "page_title":"Widget"
    }
    return render(request,'fillow/widget-basic.html',context)

def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'fillow/forms/form-element.html',context)


def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'fillow/forms/form-wizard.html',context)


def form_editor(request):
    context={
        "page_title":"CkEditor"
    }
    return render(request,'fillow/forms/form-editor.html',context)


def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'fillow/forms/form-pickers.html',context)


def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'fillow/forms/form-validation.html',context)


def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'fillow/table/table-bootstrap-basic.html',context)


def table_datatable_basic(request):
    context={
        "page_title":"Table Datatable"
    }
    return render(request,'fillow/table/table-datatable-basic.html',context)


from django.shortcuts import redirect
from .forms import UserForm, LoginForm, EmailComposeTplForm, DocumentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth import views
from django.contrib import messages

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
            additional_inform.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')


            return redirect("fillow:index")
    else:
        user_form = UserForm()
        additional_form = AdditionalInformForm()
    return render(request, 'fillow/pages/page-register.html', {'user_form': user_form, 'additional_form': additional_form})

def page_forgot_password(request):
    return render(request,'fillow/pages/page-forgot-password.html')

def page_lock_screen(request):
    return render(request,'fillow/pages/page-lock-screen.html')

def page_empty(request):
    context={
        "page_title":"Empty Page"
    }
    return render(request,'fillow/pages/page-empty.html',context)

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


from fillow import emlExtracter
import os
import sys
from .models import Document
from django.core.files.base import ContentFile
import io
from fillow.msgToEml import load
from .spam_detection import *
from .gpt import *
from .translation import *

def upload_file(request):
    # 유저가 로그인 되지 않은 상태일 때, redirect 홈
    if not request.user.is_authenticated:
        return redirect("fillow:home")
        
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
            msg_name = request.FILES['uploaded_file'].name
            form.cleaned_data['uploaded_file'].seek(0)
            msg_contents = form.cleaned_data['uploaded_file'].read()
            
            uploaded_file = request.FILES['uploaded_file'] 
            recent_document = Document.objects.latest('id')
            file_path = recent_document.uploaded_file.path
            
            # eml_name = os.path.basename(file_path).split('.msg')[0] + '.eml'
            eml_name = file_path.split('.msg')[0] + '.eml'
            print(eml_name)
            
            with open(eml_name , "wb") as f:
                contents = load(uploaded_file)
                f.write(contents.as_bytes())        
                    
            headers = ['file_name','Subject','Date','From','To','Cc','text_content']
            result = emlExtracter.prcessing_dir(headers, eml_name)
            # print(result['text_content'])
            
            gpt_result = process_file(result['text_content'])
            
            reply_req_yn = gpt_result.get('회신요청여부','')
            reply_req_yn = True if reply_req_yn == 'Y' else False
            
            # text=translate(result['text_content'])
            # print("translate text",text)
            # detect_spam(text)
            email_instance = Email(
            user=request.user,
            email_file_name=result.get('file_name', ''),
            email_subject=result.get('Subject', ''),
            email_date=result.get('Date', ''),
            email_from=result.get('From', ''),
            email_to=result.get('To', ''),
            email_cc=result.get('Cc', ''),
            email_text_content=result.get('text_content', ''),
            category = gpt_result.get('카테고리',''),
            from_company = gpt_result.get('회사',''),
            from_dept = gpt_result.get('부서',''),
            from_name = gpt_result.get('이름',''),
            reply_req_yn = reply_req_yn,
            reply_start_date = result.get('Date',''),
            reply_end_date = gpt_result.get('회신마감일자',''),
            )

            email_instance.save()
            
            return redirect("fillow:index")
    else:
        form = DocumentForm()
        
    context={
        'form':form,
        "img":AdditionalInform.objects.get(user_id=request.user.id).image,
        "masking_name":request.user.first_name[1:],
    }
    return render(request, 'fillow/pages/upload.html', context)

from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, FormView
from django.urls import reverse_lazy
from .models import Email
from django.core.paginator import Paginator

class EmailListView(ListView):
    model = Email
    template_name = 'fillow/apps/email/email-inbox.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(trash=False)
        queryset = queryset.filter(user=self.request.user).order_by('-email_date')
        self.paginator = Paginator(queryset, 1)  # 페이지당 20개 이메일 표시
        page_number = self.request.GET.get('page')
        self.page_obj = self.paginator.get_page(page_number)
        return self.page_obj.object_list

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
        self.paginator = Paginator(queryset, 1)  # 페이지당 20개 이메일 표시
        page_number = self.request.GET.get('page')
        self.page_obj = self.paginator.get_page(page_number)
        return self.page_obj.object_list

    def render_to_response(self, context, **response_kwargs):
        context.update({
            'paginator': self.paginator,
            'page_obj': self.page_obj,
        })
        return super().render_to_response(context, **response_kwargs)
    
class EmailDetailView(DetailView):
    model = Email
    #template_name = 'fillow/test.html'
    template_name = 'fillow/apps/email/email-read.html'  # 수정: template_name을 read.html로 변경

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['attachments'] = self.object.email_attachments  # 첨부파일 추가
        return context

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