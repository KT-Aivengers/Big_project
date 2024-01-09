$(".fa.fa-star").click(function () {
    $(this).toggleClass("yellow");
});

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');

    // 버튼 요소 가져오기
    const inboxBtn = document.getElementById('inbox');
    const cat1Btn = document.getElementById('cat1');
    const cat2Btn = document.getElementById('cat2');
    const cat3Btn = document.getElementById('cat3');
    const cat4Btn = document.getElementById('cat4');
    const cat5Btn = document.getElementById('cat5');
    const cat6Btn = document.getElementById('cat6');
    const cat7Btn = document.getElementById('cat7');
    const cat8Btn = document.getElementById('cat8');
    const cat9Btn = document.getElementById('cat9');

    // URL의 category 쿼리 매개변수에 따라 버튼 활성화
    if (categoryParam === '결재승인') {
        cat1Btn.classList.add('active');
    } else if (categoryParam === '휴가') {
        cat2Btn.classList.add('active');
    } else if (categoryParam === '진행업무') {
        cat3Btn.classList.add('active');
    } else if (categoryParam === '회의') {
        cat4Btn.classList.add('active');
    } else if (categoryParam === '보고') {
        cat5Btn.classList.add('active');
    } else if (categoryParam === '스크랩') {
        cat6Btn.classList.add('active');
    } else if (categoryParam === '공지') {
        cat7Btn.classList.add('active');
    } else if (categoryParam === '감사인사') {
        cat8Btn.classList.add('active');
    } else if (categoryParam === '기타') {
        cat9Btn.classList.add('active');
    } else {
        inboxBtn.classList.add('active');
    }
});
const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('category');

// 버튼 요소 가져오기
const button = document.getElementById('selected');

// URL의 쿼리 매개변수에 따라 버튼 클래스 변경
if (myParam === 'active') {
    button.classList.add('active');
}