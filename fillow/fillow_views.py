from typing import Any
from django.shortcuts import render
from django.http import HttpResponse


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
def get_schedule():
    # DB에서 일정 불러오기
    schedule_list = [
        # {
        #     'title' 제목
        #     'start' 시작일
        #     'end' 종료일
        #     'url' 클릭 시 이동할 url
        #     'groupID' 같이 움직일 일정 설정(쓸 일 없을 듯?)
        #     'className' 설정할 클래스
        # }
        {
            'title': '크리스마스',
            'start': '2023-12-25',
            'className': 'bg-danger',
        },
        {
            'title': '연락 바람',
            'start': '2023-12-21',
            'end': '2023-12-27',
        },
        {
            'title': '이메일 페이지로',
            'start': '2023-12-10',
            'end': '2023-12-15',
            'url': 'http://127.0.0.1:8000/email-inbox/',
            'className': 'bg-info',
        },
    ]
    return schedule_list


def home(request):
    context={
        "page_title":"홈",
    }
    return render(request,'fillow/home/home.html',context)

from .models import AdditionalInform
def index(request):
    context={
        "page_title":"메인",
    }
    
    most4 = get_most_4_category()
    
    context.update(most4)
    if request.user.is_authenticated:
        # 로그인이 된 상태에서 해당 유저의 id가 fillow_additionalinform 테이블의 user_ptr_id에 존재하는지 확인
        if not AdditionalInform.objects.filter(user_id=request.user.id).exists():
            # 존재하지 않는다면 additionalinform 웹페이지로 리다이렉트
            return redirect('fillow:additional_info')
        
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


def app_profile(request):
    context={
        "page_title":"App Profile"
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
    context={
        "page_title":"이메일 전송"
    }
    return render(request,'fillow/apps/email/email-compose.html',context)

def email_compose_tpl(request):
    context={
        "page_title":"전송 템플릿"
    }
    if request.method == "POST":
        form = EmailComposeTplForm(request.POST)
        if form.is_valid():
            user = request.user
            texts = form.cleaned_data.get('texts', '')
            print(texts)
            EmailComposeTpl.objects.create(texts = texts, user = user)

            
            return redirect("fillow:email-template")

    else:
        form = EmailComposeTplForm()
    
    return render(request,'fillow/apps/email/email-compose-tpl.html',context)



def email_inbox(request):
    context={
        "page_title":"받은 이메일"
    }
    return render(request,'fillow/apps/email/email-inbox.html',context)


def email_read(request):
    context={
        "page_title":"내용 보기"
    }
    return render(request,'fillow/apps/email/email-read.html',context)


def email_sent(request):
    context={
        "page_title":"보낸 이메일"
    }
    return render(request,'fillow/apps/email/email-sent.html',context)


def faq(request):
    context={
        "page_title":"FAQ"
    }
    return render(request,'fillow/apps/cs/faq.html',context)

from .models import Qna, EmailComposeTpl
from datetime import datetime
from django.shortcuts import get_object_or_404


def qna(request):
    Qnas = Qna.objects.all().order_by('-edit_date')  # 내림차순 정렬
    context={
        "page_title":"Q&A",
        'Qnas':Qnas
    }

    if request.method == "POST":
        action = request.POST.get('btn_action')
        if action == "close":
            return redirect("fillow:qna")
        user_id = request.user.id
        title = request.POST.get("title1")
        question = request.POST.get("question")
        edit_date = datetime.now()
        
        Qna.objects.create(question = question, title = title, user_id = user_id, edit_date = edit_date, status = "답변 대기중")
        
        return redirect("fillow:qna")

    return render(request,'fillow/apps/cs/qna.html',context)


def qna_details(request, id):
    qna = get_object_or_404(Qna, id=id)
    
    context={
        "page_title":"Q&A_details",
        "qna":qna,
    }
    return render(request, 'fillow/apps/cs/qna_details.html',context)

def schedule(request):
    context={
        "page_title":"일정 관리"
    }
    
    context['schedule_data'] = get_schedule()
    
    return render(request,'fillow/apps/schedule/schedule.html',context)



def app_calender(request):
    context={
        "page_title":"일정 수정하기"
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

def page_register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        additional_form = AdditionalInformForm(request.POST)
        if user_form.is_valid() and additional_form.is_valid():
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
            
            process_file(result['text_content'])
            text=translate(result['text_content'])
            print("translate text",text)
            detect_spam(text)
            email_instance = Email(
            user=request.user,
            email_file_name=result.get('file_name', ''),
            email_subject=result.get('Subject', ''),
            email_date=result.get('Date', ''),
            email_from=result.get('From', ''),
            email_to=result.get('To', ''),
            email_cc=result.get('Cc', ''),
            email_text_content=result.get('text_content', '')
            )

            email_instance.save()
            
            return redirect("fillow:index")
    else:
        form = DocumentForm()
    return render(request, 'fillow/pages/upload.html', {'form': form})

from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, FormView
from django.urls import reverse_lazy
from .models import Email

class EmailListView(ListView):
    model = Email
    #template_name = 'fillow/test2.html'  # 수정: template_name을 inbox.html로 변경
    template_name = 'fillow/apps/email/email-inbox.html'  # 수정: template_name을 inbox.html로 변경

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-email_date')  # 받은 편지함, 발신 날짜 기준 정렬
        return queryset

class EmailDetailView(DetailView):
    model = Email
    #template_name = 'fillow/test.html'
    template_name = 'fillow/apps/email/email-read.html'  # 수정: template_name을 read.html로 변경

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['attachments'] = self.object.email_attachments  # 첨부파일 추가
        return context


class EmailDeleteView(DeleteView):
    model = Email
    success_url = reverse_lazy('email_list')


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

