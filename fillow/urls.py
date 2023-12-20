from django.urls import path
from fillow import fillow_views
from django.contrib.auth import views as auth_views


app_name='fillow'
urlpatterns = [
    path('',fillow_views.index,name="index"),
    path('index/',fillow_views.index,name="index"),
    path('index-2/',fillow_views.index_2,name="index-2"),
    path('project-page/',fillow_views.project_page,name="project-page"),
    path('contacts/',fillow_views.contacts,name="contacts"),
    path('kanban/',fillow_views.kanban,name="kanban"),
    path('calendar-page/',fillow_views.calendar_page,name="calendar-page"),
    path('message/',fillow_views.message,name="message"),

    path('app-profile/',fillow_views.app_profile,name="app-profile"),
    path('edit-profile/',fillow_views.edit_profile,name="edit-profile"),
    path('post-details/',fillow_views.post_details,name="post-details"),
    path('email-compose/',fillow_views.email_compose,name="email-compose"),
    path('email-inbox/',fillow_views.email_inbox,name="email-inbox"),
    path('email-read/',fillow_views.email_read,name="email-read"),
    path('app-calender/',fillow_views.app_calender,name="app-calender"),
    path('ecom-product-grid/',fillow_views.ecom_product_grid,name="ecom-product-grid"),
    path('ecom-product-list/',fillow_views.ecom_product_list,name="ecom-product-list"),
    path('ecom-product-detail/',fillow_views.ecom_product_detail,name="ecom-product-detail"),
    path('ecom-product-order/',fillow_views.ecom_product_order,name="ecom-product-order"),
    path('ecom-checkout/',fillow_views.ecom_checkout,name="ecom-checkout"),
    path('ecom-invoice/',fillow_views.ecom_invoice,name="ecom-invoice"),
    path('ecom-customers/',fillow_views.ecom_customers,name="ecom-customers"),
    path('chart-flot/',fillow_views.chart_flot,name="chart-flot"),
    path('chart-morris/',fillow_views.chart_morris,name="chart-morris"),
    path('chart-chartjs/',fillow_views.chart_chartjs,name="chart-chartjs"),
    path('chart-chartist/',fillow_views.chart_chartist,name="chart-chartist"),
    path('chart-sparkline/',fillow_views.chart_sparkline,name="chart-sparkline"),
    path('chart-peity/',fillow_views.chart_peity,name="chart-peity"),

    path('content/',fillow_views.content,name="content"),
    path('add-content/',fillow_views.add_content,name="add-content"),
    path('menu/',fillow_views.menu,name="menu"),
    path('email-template/',fillow_views.email_template,name="email-template"),
    path('add-email/',fillow_views.add_email,name="add-email"),
    path('blog/',fillow_views.blog,name="blog"),
    path('add-blog/',fillow_views.add_blog,name="add-blog"),
    path('blog-category/',fillow_views.blog_category,name="blog-category"),

    path('ui-accordion/',fillow_views.ui_accordion,name="ui-accordion"),
    path('ui-alert/',fillow_views.ui_alert,name="ui-alert"),
    path('ui-badge/',fillow_views.ui_badge,name="ui-badge"),
    path('ui-button/',fillow_views.ui_button,name="ui-button"),
    path('ui-modal/',fillow_views.ui_modal,name="ui-modal"),
    path('ui-button-group/',fillow_views.ui_button_group,name="ui-button-group"),
    path('ui-list-group/',fillow_views.ui_list_group,name="ui-list-group"),
    path('ui-card/',fillow_views.ui_card,name="ui-card"),
    path('ui-carousel/',fillow_views.ui_carousel,name="ui-carousel"),
    path('ui-dropdown/',fillow_views.ui_dropdown,name="ui-dropdown"),
    path('ui-popover/',fillow_views.ui_popover,name="ui-popover"),
    path('ui-progressbar/',fillow_views.ui_progressbar,name="ui-progressbar"),
    path('ui-tab/',fillow_views.ui_tab,name="ui-tab"),
    path('ui-typography/',fillow_views.ui_typography,name="ui-typography"),
    path('ui-pagination/',fillow_views.ui_pagination,name="ui-pagination"),
    path('ui-grid/',fillow_views.ui_grid,name="ui-grid"),
    

    path('uc-select2/',fillow_views.uc_select2,name="uc-select2"),
    path('uc-nestable/',fillow_views.uc_nestable,name="uc-nestable"),
    path('uc-noui-slider/',fillow_views.uc_noui_slider,name="uc-noui-slider"),
    path('uc-sweetalert/',fillow_views.uc_sweetalert,name="uc-sweetalert"),
    path('uc-toastr/',fillow_views.uc_toastr,name="uc-toastr"),
    path('map-jqvmap/',fillow_views.map_jqvmap,name="map-jqvmap"),
    path('uc-lightgallery/',fillow_views.uc_lightgallery,name="uc-lightgallery"),

    path('widget-basic/',fillow_views.widget_basic,name="widget-basic"),

    path('form-element/',fillow_views.form_element,name="form-element"),
    path('form-wizard/',fillow_views.form_wizard,name="form-wizard"),
    path('form-editor/',fillow_views.form_editor,name="form-editor"),
    path('form-pickers/',fillow_views.form_pickers,name="form-pickers"),
    path('form-validation/',fillow_views.form_validation,name="form-validation"),

    path('table-bootstrap-basic/',fillow_views.table_bootstrap_basic,name="table-bootstrap-basic"),
    path('table-datatable-basic/',fillow_views.table_datatable_basic,name="table-datatable-basic"),


    path('page-login/',fillow_views.page_login,name="page-login"),    
    path('page-register/',fillow_views.page_register,name="page-register"),
    path('page-forgot-password/',fillow_views.page_forgot_password,name="page-forgot-password"),
    path('page-lock-screen/',fillow_views.page_lock_screen,name="page-lock-screen"),
    path('page-empty/',fillow_views.page_empty,name="page-empty"),
    path('page-error-400/',fillow_views.page_error_400,name="page-error-400"),
    path('page-error-403/',fillow_views.page_error_403,name="page-error-403"),
    path('page-error-404/',fillow_views.page_error_404,name="page-error-404"),
    path('page-error-500/',fillow_views.page_error_500,name="page-error-500"),
    path('page-error-503/',fillow_views.page_error_503,name="page-error-503"),

]