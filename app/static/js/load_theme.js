function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

cur_theme = getCookie('theme')

if (cur_theme === null) {
    setCookie('theme', 'dark')
    cur_theme = 'dark'
}

function SetTheme(theme_name) {
    if (theme_name === 'dark')
        document.documentElement.setAttribute('data-bs-theme', 'dark')
    else
        document.documentElement.setAttribute('data-bs-theme', 'light')
    setCookie('theme', theme_name)
}

SetTheme(cur_theme)
