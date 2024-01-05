const firstNameElement = $('[name="first_name"]');
const lastNameElement = $('[name="last_name"]');
const companyElement = $('[name="company"]');
const deptElement = $('[name="dept"]');
const phoneElement = $('[name="phone"]')

const postBtn = $('[name="btn-post"]');

const phoneValid = $('#phone');

const phoneRegex = /^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$/;

listElement = [
    firstNameElement,
    lastNameElement,
    companyElement,
    deptElement,
]

function validateInfo() {
    if (phoneRegex.test(phoneElement.val())) {
        phoneValid.css('color', 'green');
        phoneValid.find('span').text(' 알맞은 전화번호 형식입니다.');
        phoneValid.find('i#phone-valid').css('display', 'inline-block');
        phoneValid.find('i#phone-invalid').css('display', 'none');
    } else {
        phoneValid.css('color', 'red');
        phoneValid.find('span').html(' 전화번호 형식이 아닙니다<br>(xxx-xxx-xxxx 또는 xxx-xxxx-xxxx, -는 생략 가능).');
        phoneValid.find('i#phone-valid').css('display', 'none');
        phoneValid.find('i#phone-invalid').css('display', 'inline-block');
        return false;
    }

    for(let i = 0; i < 4; i++) {
        if (listElement[i].val().trim() === '') {
            return false;
        }
    }

    return true;
}

function validate() {
    if (validateInfo()) {
        postBtn.removeClass('disabled');
    } else {
        postBtn.addClass('disabled');
    }
}

firstNameElement.on('input', validate);
lastNameElement.on('input', validate);
companyElement.on('input', validate);
deptElement.on('input', validate);
phoneElement.on('input', validate);
