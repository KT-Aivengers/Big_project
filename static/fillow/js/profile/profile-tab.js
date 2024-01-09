document.getElementById('btn-upload').addEventListener('click', function(e) {
    var fileInput = document.getElementById('formFile-upload');
    if (fileInput.files.length === 0) {
        e.preventDefault();
        $('#submitModal').modal('show');
    }
});

// 탭 상태 유지하기
$(document).ready(function() {
    var activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
          $('.nav-tabs a[href="' + activeTab + '"]').tab('show');
    }

    $('.nav-tabs a').on('shown.bs.tab', function(e) {
         var activeTab = $(e.target).attr('href');
          localStorage.setItem('activeTab', activeTab);
    });
});