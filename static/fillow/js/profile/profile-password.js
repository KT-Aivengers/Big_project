const password1 = $('#password1');
const password2 = $('#password2');

const valid1 = $('#valid1');
const valid2 = $('#valid2');
const valid3 = $('#valid3');
const valid4 = $('#valid4');
const valid5 = $('#valid5');

const invalid1 = $('#invalid1');
const invalid2 = $('#invalid2');
const invalid3 = $('#invalid3');
const invalid4 = $('#invalid4');
const invalid5 = $('#invalid5');

const same = $('#same');
const length = $('#length');;
const number = $('#number');
const common = $('#common');
const similar = $('#similar');

const passwordBtn = $('#passwordBtn');

function isCommon(password) {
    let result = false;
    const lower = password.toLowerCase();

    commonWords.forEach(function(word) {
        if (lower == word) {
            result = true;
            return;
        }
    });

    return result;
}


function isSameF(p1, p2) {
    if (p1 === p2) {
        return true;
    }
    return false;
}


function isSimilar(p1) {
    const userAttrs = [
        username,
        firstName,
        lastName,
        email,
    ]

    let result = false;

    userAttrs.forEach(function(attr) {
        let a = attr;
        let list = a.split(/\W+/).concat(a);

        list.forEach(function(l) {
            s = new difflib.SequenceMatcher(null, p1.toLowerCase(), l.toLowerCase());
            if (s.quickRatio() >= 0.7) {
                result = true;
                return;
            }
        });

        if (result) {
            return;
        }
    });
    return result
}


const textListValid = [
    ' 확인란과 동일합니다.',
    ' 길이가 8이상입니다.',
    ' 숫자로만 구성되어 있지 않습니다.',
    ' 자주 쓰이는 단어가 아닙니다.',
    ' 개인정보와 다릅니다.',
]

const textListInvalid = [
    ' 확인란과 다릅니다.',
    ' 길이가 8 미만입니다.',
    ' 숫자로만 구성되어있습니다.',
    ' 자주 쓰이는 단어입니다.',
    ' 개인정보와 비슷합니다.',
]


function changeState(bool, valid, invalid, html, index) {
    if (bool) {
        valid.css('display', 'inline-block');
        invalid.css('display', 'none');
        html.css('color', 'green');
        html.find('span').text(textListValid[index]);
    } else {
        valid.css('display', 'none')
        invalid.css('display', 'inline-block')
        html.css('color', 'red');
        html.find('span').text(textListInvalid[index]);
    }
}


function validatePassword() {
    // 비밀번호 유효성 체크하기
    const password = password1.val();
    const passwordConfirm = password2.val();

    let isSame = false;
    let isMore8 = false;
    let isNotNumber = false;
    let isNotCommon = false;
    let isNotSimilar = false;

    // 확인 값이 같은지 확인하기
    if (isSameF(password, passwordConfirm)) {
        isSame = true;
    }

    // 길이가 8이상인지 확인하기
    if (password.length >= 8) {
        isMore8 = true;
    }

    // 숫자로만 이루어져있는지 확인하기
    if (isNaN(password)) {
        isNotNumber = true;
    }

    // 자주 쓰이는 단어인지 확인하기
    if (!isCommon(password)) {
        isNotCommon = true;
    }

    // 유사도 확인하기
    if (!isSimilar(password)) {
        isNotSimilar = true;
    }

    changeState(isSame, valid1, invalid1, same, 0);
    changeState(isMore8, valid2, invalid2, length, 1);
    changeState(isNotNumber, valid3, invalid3, number, 2);
    changeState(isNotCommon, valid4, invalid4, common, 3);
    changeState(isNotSimilar, valid5, invalid5, similar, 4);

    if (isSame && isMore8 && isNotNumber && isNotCommon && isNotSimilar) {
        passwordBtn.removeClass('disabled');
    } else {
        passwordBtn.addClass('disabled');
    }
}

password1.on('input', validatePassword);
password2.on('input', validatePassword);

validatePassword();