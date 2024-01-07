const company = $('#id_company');
const phone = $('#id_phone');

const phoneValid = $('#phone');

const postBtn = $("#post");

const phoneRegex = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;

var isCompanyFilled = false;
var isPhoneValid = false;

function validate() {
    if (company.val().trim() !== "") {
        isCompanyFilled = true;
    } else {
        isCompanyFilled = false;
    }

    if (phoneRegex.test(phone.val())) {
        isPhoneValid = true;
        phoneValid.css('color', 'green');
        phoneValid.find('span').text(' 알맞은 전화번호 형식입니다.');
        phoneValid.find('i#phone-valid').css('display', 'inline-block');
        phoneValid.find('i#phone-invalid').css('display', 'none');
    } else {
        isPhoneValid = false;
        phoneValid.css('color', 'red');
        phoneValid.find('span').html(' 전화번호 형식이 아닙니다<br>(xxx-xxx-xxxx 또는 xxx-xxxx-xxxx, -는 생략 가능).');
        phoneValid.find('i#phone-valid').css('display', 'none');
        phoneValid.find('i#phone-invalid').css('display', 'inline-block');
    }

    if (isCompanyFilled && isPhoneValid) {
        postBtn.removeClass('disabled');
        
    } else {
        postBtn.addClass('disabled');
    }
}

company.on('input', validate);
phone.on('input', validate);

validate();