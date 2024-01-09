document.addEventListener("DOMContentLoaded", function() {
    if (isUploaded) {
        Swal.fire({
            html: "메일이 성공적으로 저장되었습니다",
            icon: "success",
            showCloseButton: true,
            showConfirmButton: false,
        });
    }
});