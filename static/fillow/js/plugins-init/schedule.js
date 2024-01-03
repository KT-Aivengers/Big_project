// 일정에 변경점이 있는지 저장
var changed = false;

// 일정 데이터 파싱
function dateParsing(schedule) {
    var pk = schedule.extendedProps.pk;
    var title = schedule.title;
    var start = schedule.start;
    var end = schedule.end;
    var category = schedule.extendedProps.category;
    
    // 실제 날짜보다 1 적게 나와서 전부 1을 더함
    start = moment(start).add(1, 'days');
    var fstart = start.toISOString().substring(0, 10);

    // 만약 end 값이 없다면 start의 하루 뒤로 설정
    if (end) {
        end = moment(end).add(1, 'days');
        var fend = end.toISOString().substring(0, 10);
    } else {
        start = moment(start).add(1, 'days');
        var fend = start.toISOString().substring(0, 10);
    }
    
    return {
        'pk': pk,
        'title': title,
        'start': fstart,
        'end': fend,
        'category': category,
    }
}

// 이동된 일정 삭제하기(pk값)
function removeAI(pk) {
    notInCalendar = notInCalendar.filter(function(schedule) {
        return schedule['pk'] != pk;
    });
}

// 버튼 활성화/비활성화 변경
function changeDisable() {
    $('#save').prop('disabled', !changed);
    $('#reset').prop('disabled', !changed);
}

// 초기화(단순 새로고침)
$('#reset-db').click(function() {
    location.reload();
});

// 화면이 나오기 전, 버튼 비활성화 하기
changeDisable();

function fullCalender() {
    // DB에 변경사항 저장
    $('#save-db').click(function() {
        var currentSchedule = calendar.getEvents();
        var newList = []
        
        // 모든 일정 날짜 파싱하여 저장
        currentSchedule.forEach(function(schedule) {
            var scheduleData = dateParsing(schedule);
            newList.push(scheduleData);
        });
        
        // 달력 위 일정, 배정 안된 일정 합쳐서 json 형태로 저장
        var data_list = {'schedule': newList.concat(notInCalendar)};

        // csrf 토큰 설정
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // AJAX 요청
        $.ajax({
            type: 'POST',
            url: '/schedule/',
            contentType: 'application/json',
            data: JSON.stringify(data_list),
            headers: {
                'X-CSRFToken': csrftoken
            },
        });

        // DB에 저장된 뒤 새로고침
        location.reload();
    });

    // 내용 변경 여부 확인하기
    var isChanged = function(info) {
        var currentSchedule = calendar.getEvents()
        var newList = []
        
        currentSchedule.forEach(function(schedule) {
            var scheduleData = dateParsing(schedule);
            newList.push(scheduleData);
        });

        // 일정의 상태를 문자열화 하여 기존 데이터와 비교
        changed = JSON.stringify(scheduleList) !== JSON.stringify(newList);
        changeDisable();
    }

    /* 드래그 앤 드롭 초기화
    -----------------------------------------------------------------*/
    var containerEl = document.getElementById('external-events');
    new FullCalendar.Draggable(containerEl, {
        itemSelector: '.external-event',
        eventData: function(eventEl) {
            return {
                pk: eventEl.getAttribute('pk'),
                title: eventEl.innerText.trim(),
                category: eventEl.getAttribute('category'),
            }
        }
    });
    /* 달력 생성
    -----------------------------------------------------------------*/
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        // 이벤트 목록
        events: scheduleList,
        height: '100%',
        locale: 'kr',
        headerToolbar: {
            left: 'prev',
            center: 'title',
            right: 'next',
        },
        selectable: true,
        editable: true,
        
        // 색상 설정
        eventContent: function(info) {
            // 사용자 정의 일정 색
            var color = '#faefd1';

            // extendedProps에서 값을 가져와서 색상 설정
            let cat = info.event.extendedProps.category
            if (cat === '감사인사') {
                color = '#312a2a';
            } else if (cat === '결재승인') {
                color = '#fc2e53';
            } else if (cat === '공지') {
                color = '#d653c1';
            } else if (cat === '보고') {
                color = '#15c08c';
            } else if (cat === '스크랩') {
                color = '#ffa7d7';
            } else if (cat === '진행업무') {
                color = '#ffdc00';
            } else if (cat === '회의') {
                color = '#09bd3c';
            } else if (cat === '휴가') {
                color = '#ffbf00';
            } else if (cat === '기타') {
                color = '#c8c8c8';
            }

            info.backgroundColor = color;
            info.boxShadow = color;
        },

        // 툴팁 설정
        eventMouseEnter: function (info) {
            $(info.el).popover({
                title: info.event.title,
                placement: 'top',
                trigger: 'hover',
                content: moment(info.event.start).add(1, 'days').toISOString().substring(0, 10) +
                '~' +
                moment(info.event.end).add(1, 'days').toISOString().substring(0, 10),
                container: 'body'
            });

            $(info.el).on('hidden.bs.popover', function () {
                $(this).popover('dispose');
            });
        },

        // 날짜 클릭 시
        select: function (info) {
            Swal.fire({
                html: "<div class='mb-5'>새로운 일정 추가하기</div><input type='text' class='form-control' id='swal-title' />",
                icon: "info",
                showCancelButton: true,
                confirmButtonText: "추가",
                cancelButtonText: "취소",
                confirmButtonColor: '#15c08c',
                cancelButtonColor: '#fc2e53',
                preConfirm: function () {
                    var title = document.getElementById('swal-title').value;
                    if (!title) {
                        Swal.showValidationMessage('일정 제목을 입력해주세요.');
                    }
                    return title;
                }
            }).then(function (result) {
                if (result.isConfirmed) {
                    calendar.addEvent({
                        title: result['value'],
                        start: info.start,
                        end: info.end,
                        allDay: info.allDay,
                    })
                    calendar.unselect()
                }
            });
        },
        // 일정 추가시
        eventAdd: function (info) {
            isChanged();
        },
        // 일정 변경 시
        eventChange: function (info) {
            isChanged();
        },
        // 일정 제거 시
        eventRemove: function (info) {
            isChanged();
        },
        // 일정 드래그 앤 드롭 시
        // eventDrop: function(obj) {
        // },
        
        // 클릭 시
        eventClick: function (info) {
            const defaultSchedule = dateParsing(info.event);
            let defaultTitled = defaultSchedule['title'];
            let defaultStart = defaultSchedule['start'];
            let defaultEnd = defaultSchedule['end'];

            let cancelButton = true;
            if (!info.event.extendedProps.pk) {
                cancelButton = false;
            }

            Swal.fire({
                text: "이 일정에 어떤 작업을 하시겠습니까?",
                icon: "info",
                showCloseButton: true,
                showDenyButton: true,
                showCancelButton: cancelButton,
                confirmButtonText: '삭제',
                denyButtonText: '수정',
                cancelButtonText: '이동',
                confirmButtonColor: '#fc2e53',
                denyButtonColor: '#ffc107',
                cancelButtonColor: '#15c08c',
            }).then(function (result) {
                if (result.isConfirmed) {
                    Swal.fire({
                        text: '해당 일정이 삭제됩니다',
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: "네",
                        cancelButtonText: "아니오",
                        confirmButtonColor: '#15c08c',
                        cancelButtonColor: '#fc2e53',
                    }).then(function (result) {
                        if (result.isConfirmed) {
                            info.event.remove();
                        }
                    });
                } else if (result.isDenied) {
                    Swal.fire({
                        html:
                            `
                            <h3>일정 수정하기</h3>
                            <input id="title" class="swal2-input" value="${defaultTitled}">
                            <input id="date-range" class="swal2-input">
                            `,
                        showCancelButton: true,
                        confirmButtonText: '수정',
                        cancelButtonText: '취소',
                        confirmButtonColor: '#15c08c',
                        cancelButtonColor: '#fc2e53',

                        preConfirm: function () {
                            var title = document.getElementById('title').value;
                            if (!title) {
                                Swal.showValidationMessage('일정 제목을 입력해주세요.');
                            }
                            return title;
                        },
                        
                        didOpen : function() {
                            $('#date-range').daterangepicker({
                                opens: 'left',
                                startDate: defaultStart,
                                endDate: defaultEnd,
                                locale: {
                                    format: 'YYYY-MM-DD',
                                    applyLabel: '적용',
                                    cancelLabel: '취소',
                                    daysOfWeek: ['일', '월', '화', '수', '목', '금', '토'],
                                    monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
                                },
                            });
                        }
                    }).then(function(result) {
                        if (result.isConfirmed) {
                            const changedTitle = $('#title').val();
                            const selectedRange = $('#date-range').val();
                            const dates = selectedRange.split(' - ');
                            const changedStart = dates[0];
                            var changedEnd = dates[1];
                            info.event.setProp('title', changedTitle);

                            // 선택한 날짜가 같은 날짜일 때 종료 날짜에 1을 더함
                            if (changedStart === changedEnd) {
                                var temp = new Date(changedEnd);
                                temp.setDate(temp.getDate() + 1);
                                changedEnd = temp.toISOString().substring(0, 10);
                            }
                            info.event.setStart(changedStart);
                            info.event.setEnd(changedEnd);
                            Swal.fire({
                                text: '성공적으로 수정하였습니다',
                                icon: 'success',
                                confirmButtonText: "확인",
                                confirmButtonColor: '#15c08c',  
                            });
                        }
                    });
                } else if (result.dismiss === Swal.DismissReason.cancel) {
                    Swal.fire({
                        text: '해당 이메일 페이지로 이동합니다',
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: "네",
                        cancelButtonText: "아니오",
                        confirmButtonColor: '#15c08c',
                        cancelButtonColor: '#fc2e53',
                    }).then(function (result) {
                        if (result.isConfirmed) {
                            window.location.href = '{% url "fillow:email_list" %}' + `${info.event.extendedProps.pk}`;
                        }
                    });
                }
            });
        },
        // 외부에서 드래그 앤 드롭
        eventReceive: function (info) {
            // 목록에서 삭제하기
            isChanged();
            info.draggedEl.parentNode.removeChild(info.draggedEl);
            removeAI(info.event.extendedProps.pk);
        },
        // 달력에서 '일' 제거
        dayCellContent: function (info) {
            var number = document.createElement('a');
            number.classList.add('fc-daygrid-day-number');
            number.innerHTML = info.dayNumberText.replace('일', '')
            if (info.view.type == 'dayGridMonth') {
                return {
                    html: number.outerHTML
                };
            }
            return {
                domNodes: []
            }
        }
    });
    calendar.render();
}

// 캘린더 잘 표시 안되는 버그 수정한 코드
jQuery(window).on('load', function() {
    setTimeout(function() {
        fullCalender();
    }, 1000);
});