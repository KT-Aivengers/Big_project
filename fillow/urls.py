from django.urls import path
from fillow import fillow_views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static

app_name='fillow'
urlpatterns = [
    path('home/',fillow_views.home,name='home'),
    
    path('',fillow_views.home,name="home"),
    path('index/',fillow_views.index,name="index"),
    path('schedule/',fillow_views.schedule,name="schedule"),

    path('profile/',fillow_views.app_profile,name="profile"),
    path('check-password/',fillow_views.check_password_,name="check-password"),
    path('check-username/',fillow_views.check_username,name="check-username"),
    
    path('email-compose/',fillow_views.email_compose,name="email-compose"),
    path('email-compose-tpl/',fillow_views.email_compose_tpl,name="email-compose-tpl"),
    path('email-inbox/',fillow_views.email_inbox,name="email-inbox"),
    path('email-read/',fillow_views.email_read,name="email-read"),
    path('email-sent/',fillow_views.email_sent,name="email-sent"),
    path('faq/',fillow_views.faq,name="faq"),
    path('qna/',fillow_views.qna,name="qna"),
    path('qna/<int:id>/',fillow_views.qna_details,name="qna-details"),
    path('qna/<int:id>/update/', fillow_views.qna_details2, name="qna-details2"),

    path('page-login/', auth_views.LoginView.as_view(template_name="fillow/pages/page-login.html", form_class = LoginForm), name="page-login"),
    # path('page-login/', auth_views.LoginView.as_view(template_name="fillow/pages/page-login.html"), name="page-login"),
    path('page-logout/', auth_views.LogoutView.as_view(template_name="fillow/home/home.html"), name='page-logout'),
    # path('page-login/',fillow_views.page_login,name="page-login"),
    path('page-register/',fillow_views.page_register,name="page-register"),
    path('page-register-complete', fillow_views.page_register_complete, name="page-register-complete"),
    path('page-forgot-password/',fillow_views.page_forgot_password,name="page-forgot-password"),
    path('page-reset-done/', fillow_views.page_reset_done, name="page-reset-done"),
    path('reset/<uidb64>/<token>/', fillow_views.page_reset_confirm, name='page-reset-confirm'),
    path('page-reset-complete/', fillow_views.page_reset_complete, name="page-reset-complete"),
    path('additionalinfo/', fillow_views.fillow_additionalinform, name='additional_info'),
    path('page-error-400/',fillow_views.page_error_400,name="page-error-400"),
    path('page-error-403/',fillow_views.page_error_403,name="page-error-403"),
    path('page-error-404/',fillow_views.page_error_404,name="page-error-404"),
    path('page-error-500/',fillow_views.page_error_500,name="page-error-500"),
    path('page-error-503/',fillow_views.page_error_503,name="page-error-503"),

    path('upload/', fillow_views.upload_file, name='upload_file'),
    
    path('email/', fillow_views.EmailListView.as_view(), name='email_list'),
    path('email/<int:pk>', fillow_views.EmailDetailView.as_view(), name='email_detail'),
    path('email/trash/<int:pk>/', fillow_views.email_trash, name='email-trash'),
    path('email/trash/', fillow_views.EmailListView_Trash.as_view(), name='email-list-trash'),
    path('email/create/', fillow_views.EmailCreateView.as_view(), name='email_create'),
    path('email/<int:pk>/update/', fillow_views.EmailUpdateView.as_view(), name='email_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
