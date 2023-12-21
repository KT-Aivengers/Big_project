(function($) {
    "use strict"

    //date picker classic default
    $('.datepicker-default').pickadate({
        monthsShort: [
            "1월",
            "2월",
            "3월",
            "4월",
            "5월",
            "6월",
            "7월",
            "8월",
            "9월",
            "10월",
            "11월",
            "12월",
        ],
        monthsFull: [
            "1월",
            "2월",
            "3월",
            "4월",
            "5월",
            "6월",
            "7월",
            "8월",
            "9월",
            "10월",
            "11월",
            "12월",
        ],
        weekdaysFull: ["일", "월", "화", "수", "목", "금", "토"],
        weekdaysShort: ["일", "월", "화", "수", "목", "금", "토"],
        max: true,
        close: "닫기",
        clear: "초기화",
        today: "오늘",
        format: "yyyy-mm-dd",
    });

})(jQuery);