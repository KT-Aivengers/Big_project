#Static Folder Name
folder_name = "fillow" 

dz_array = {
        "public":{
            "favicon":f"{folder_name}/images/favicon.ico",
            "description":"AI가 자동으로 메일함을 정리하여 업무 효율성이 향상됩니다.",
            "og_title":"협재씨 | Aivengers(4기 18조)",
            "og_description":"AI가 자동으로 메일함을 정리하여 업무 효율성이 향상됩니다.",
            "og_image":f"{folder_name}/images/logofull.svg",
            "title":"협재씨 | 당신의 메일함을 정리해드립니다, | 18조",
        },
        "global":{
            "css":[
                    f"{folder_name}/vendor/bootstrap-select/css/bootstrap-select.min.css",
					f"{folder_name}/css/style.css",
                ],

            "js":{
                "top":[
                    f"{folder_name}/vendor/global/global.min.js",
					f"{folder_name}/vendor/bootstrap-select/js/bootstrap-select.min.js",
                ],
                "bottom":[
                    f"{folder_name}/js/custom.min.js",
                    f"{folder_name}/js/dlabnav-init.js",
                ]
            },

        },
        "pagelevel":{
            "fillow":{#AppName
                "fillow_views":{
                    "css":{
                        "home" : [
                        ],
                        "index": [
                            f"{folder_name}/vendor/owl-carousel/owl.carousel.css",
                            f"{folder_name}/vendor/nouislider/nouislider.min.css",
                        ],
                        "app_profile": [
                            f"{folder_name}/vendor/lightgallery/dist/css/lightgallery.css",
                            f"{folder_name}/vendor/lightgallery/dist/css/lg-thumbnail.css",
                            f"{folder_name}/vendor/lightgallery/dist/css/lg-zoom.css",
                        ],
                        "email_compose": [
                            f"{folder_name}/vendor/ckeditor/ckeditor.js",
                        ],
                        "email_inbox": [
                        ],
                        "email_read": [
                            f"{folder_name}/vendor/jqueryui/css/jquery-ui.min.css",
                        ],
                        "email_sent": [
                        ],
                        "faq": [
                        ],
                        "qna": [
                            f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                            f"{folder_name}/vendor/clockpicker/css/bootstrap-clockpicker.min.css",
                            f"{folder_name}/vendor/jquery-asColorPicker/css/asColorPicker.min.css",
                            f"{folder_name}/vendor/bootstrap-material-datetimepicker/css/bootstrap-material-datetimepicker.css",
                            f"{folder_name}/vendor/bootstrap-datepicker-master/css/bootstrap-datepicker.min.css",
                            f"{folder_name}/vendor/pickadate/themes/default.css",
                            f"{folder_name}/vendor/pickadate/themes/default.date.css",
                            f"{folder_name}/vendor/sweetalert2/sweetalert2.min.css",
                        ],
                        "schedule": [
                            f"{folder_name}/vendor/fullcalendar/css/main.min.css",
                            f"{folder_name}/vendor/sweetalert2/sweetalert2.min.css",
                            f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.css",
                        ],
                    },
                    "js":{
                        "index": [
                            f"{folder_name}/vendor/counter/counter.min.js",
                            f"{folder_name}/vendor/counter/waypoint.min.js",
                            f"{folder_name}/vendor/apexchart/apexchart.js",
                            f"{folder_name}/vendor/chart-js/chart.bundle.min.js",
                            f"{folder_name}/vendor/peity/jquery.peity.min.js",
                            f"{folder_name}/js/dashboard/dashboard-1.js",
                            f"{folder_name}/vendor/owl-carousel/owl.carousel.js",
                        ],
                        "app_profile": [
                            f"{folder_name}/vendor/chart-js/chart.bundle.min.js",	
                            f"{folder_name}/vendor/lightgallery/dist/lightgallery.min.js",	
                            f"{folder_name}/vendor/lightgallery/dist/plugins/thumbnail/lg-thumbnail.min.js",
                            f"{folder_name}/vendor/lightgallery/dist/plugins/zoom/lg-zoom.min.js",
                            f"{folder_name}/js/plugins-init/common-data.js",
                        ],
                        "email_compose": [
                            f"{folder_name}/vendor/dropzone/dist/dropzone.js",
                        ],
                        "email_inbox": [
                        ],
                        "email_read": [
                            f"{folder_name}/vendor/jqueryui/js/jquery-ui.min.js",
                        ],
                        "email_sent": [
                        ],
                        "faq": [
                        ],
                        "qna": [
                            f"{folder_name}/vendor/moment/moment.min.js",
                            f"{folder_name}/vendor/bootstrap-material-datetimepicker/js/bootstrap-material-datetimepicker.js",
                            f"{folder_name}/vendor/pickadate/picker.js",
                            f"{folder_name}/vendor/pickadate/picker.time.js",
                            f"{folder_name}/vendor/pickadate/picker.date.js",
                            f"{folder_name}/js/plugins-init/pickadate-init.kr.js",
                            f"{folder_name}/vendor/sweetalert2/sweetalert2.min.js",
                            f"{folder_name}/js/plugins-init/qna-init.js",
                        ],
                        "schedule": [
                            f"{folder_name}/vendor/moment/moment.min.js",
                            f"{folder_name}/vendor/fullcalendar/js/main.min.js",
                            f"{folder_name}/vendor/sweetalert2/sweetalert2.min.js",
                            f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                            f"{folder_name}/js/plugins-init/schedule.js",
                        ],
                    },
                }
            }
        }


}