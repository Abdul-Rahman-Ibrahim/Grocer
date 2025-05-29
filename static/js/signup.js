const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".show-password-toggle")

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent == "Show") {
        showPasswordToggle.textContent = "Hide";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "Show";
        passwordField.setAttribute("type", "password");
    }
}

showPasswordToggle.addEventListener("click", handleToggleInput);