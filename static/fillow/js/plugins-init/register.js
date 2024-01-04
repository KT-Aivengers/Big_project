const password1 = document.getElementById('id_password1');
const password2 = document.getElementById('id_password2');

const valid = document.getElementById('valid');
const invalid = document.getElementById('invalid');

const same = document.getElementById('same');

const submit = document.getElementById('submit');

const username = document.getElementById('username');

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function validatePassword() {
    password = password1.value;
    passwordConfirm = password2.value;

    if ((password.length === 0) | (password !== passwordConfirm)){
        valid.style.display = 'none';
        invalid.style.display = 'inline-block';
        same.style.color = 'red';
        submit.classList.add('disabled');
    } else {
        valid.style.display = 'inline-block';
        invalid.style.display = 'none';
        same.style.color = 'green';
        submit.classList.remove('disabled');
    }
}

validatePassword();

password1.addEventListener('input', validatePassword);
password2.addEventListener('input', validatePassword);

username.addEventListener('click', function() {
    event.preventDefault()

    const name = $('#id_username').val();
    const username_data = {"username": name}

    $.ajax({
        url: '/check-username/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(username_data),
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            if (response.available) {
                $('#message').text('사용 가능한 아이디입니다.');
            } else {
                $('#message').text('이미 존재하는 아이디입니다.');
            }
        },
        error: function(xhr, status, error) {
            console.error('서버 에러 발생');
        }
    });
});