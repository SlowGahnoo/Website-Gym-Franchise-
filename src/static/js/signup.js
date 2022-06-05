function passwordMatchMessage(passwordsMatched) {
    try {
        const msgBox = document.querySelector("#confirmation-msg");
        if (passwordsMatched) {
            msgBox.textContent = "Ο κωδικός πρόσβασης επιβεβαιώθηκε.";
            msgBox.style.backgroundColor = 'green';
        }
        else {
            msgBox.textContent = "Οι κωδικοί είναι διαφορετικοί.";
            msgBox.style.backgroundColor = 'red';
        }
    }
    catch {
        let loginInfoWrapper = document.querySelector("fieldset.login-info");
        let msgBox = document.createElement("div");
        msgBox.setAttribute("id", "confirmation-msg");
        let msgText;
        if (passwordsMatched) {
            msgText = document.createTextNode("Ο κωδικός πρόσβασης επιβεβαιώθηκε.");
            msgBox.style.backgroundColor = 'green';
        }
        else {
            msgText = document.createTextNode("Οι κωδικοί είναι διαφορετικοί.");
            msgBox.style.backgroundColor = 'red';
        }
        msgBox.appendChild(msgText);
        loginInfoWrapper.appendChild(msgBox);
    }
}

function checkPasswords(passwordBox, rePasswordBox) {
    if (passwordBox.value === rePasswordBox.value && passwordBox.value === '') return;
    else if (passwordBox.value === rePasswordBox.value) passwordMatchMessage(true);
    else passwordMatchMessage(false);
}

const passwordBox = document.querySelector("fieldset.login-info div #password");
const rePasswordBox = document.querySelector("fieldset.login-info div #retype-password");
const submitBtn = document.querySelector(".submit-button");

rePasswordBox.addEventListener('input', () => checkPasswords(passwordBox, rePasswordBox));
rePasswordBox.addEventListener('focus', () => checkPasswords(passwordBox, rePasswordBox));

passwordBox.addEventListener('input', () => checkPasswords(passwordBox, rePasswordBox));
passwordBox.addEventListener('focus', () => checkPasswords(passwordBox, rePasswordBox));