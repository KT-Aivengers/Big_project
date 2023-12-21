// 닫기 버튼
var closeModalBtn = document.getElementById('closeModal');

// 게시 버튼
var postBtn = document.getElementById('post');

// 모달 요소
var qnaModal = new bootstrap.Modal(document.getElementById('postModal'))

// 모달 닫기
closeModalBtn.addEventListener('click', function() {
    // 입력된 내용 가져오기
    var title = document.getElementById('title').value.trim();
    var detail = document.getElementById('detail').value.trim();

    // 제목 또는 내용 중 하나라도 존재하는 경우 SweetAlert 표시, 아니면 바로 모달 닫기
    if (title !== '' || detail !== '') {
        // SweetAlert 띄우기
        Swal.fire({
            title: '지금까지 작성한 내용이 삭제됩니다',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#fc2e53',
            cancelButtonColor: '#15c08c',
            confirmButtonText: '삭제',
            cancelButtonText: '뒤로',
        }).then((result) => {
            // 여기에 SweetAlert 확인 후 할 작업 추가
            if (result.isConfirmed) {
                document.getElementById('title').value = '';
                document.getElementById('detail').value = '';
                Swal.close();
                qnaModal.hide();
            }
        });
    } else {
        qnaModal.hide();
    }
});

// 게시
postBtn.addEventListener('click', function() {
    document.getElementById('title').value = '';
    document.getElementById('detail').value = '';
});