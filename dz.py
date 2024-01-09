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
                        ],
                        "app_profile": [
                        ],
                        "email_compose": [
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
                            f"{folder_name}/vendor/apexchart/apexchart.js",
                            f"{folder_name}/vendor/chart-js/chart.bundle.min.js",
                            f"{folder_name}/js/dashboard/dashboard-1.js",
                        ],
                        "app_profile": [
                            f"{folder_name}/vendor/chart-js/chart.bundle.min.js",
                            f"{folder_name}/js/plugins-init/common-data.js",
                        ],
                        "email_compose": [
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
                            f"{folder_name}/vendor/sweetalert2/sweetalert2.min.js",
                            f"{folder_name}/js/qna/qna.js",
                        ],
                        "schedule": [
                            f"{folder_name}/vendor/moment/moment.min.js",
                            f"{folder_name}/vendor/fullcalendar/js/main.min.js",
                            f"{folder_name}/vendor/sweetalert2/sweetalert2.min.js",
                            f"{folder_name}/vendor/bootstrap-daterangepicker/daterangepicker.js",
                            f"{folder_name}/js/schedule/schedule.js",
                        ],
                    },
                }
            }
        }


}