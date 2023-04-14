document.cookie = 'SameSite=None;path=/;'
cur_theme = document.cookie.split("; ")
    .find((row) => row.startsWith("theme="))
    ?.split("=")[1];

if (cur_theme === undefined || cur_theme === 'undefined') {
    document.cookie = `theme=dark;path=/;`
    cur_theme = 'dark'
}

function SetTheme(theme_name) {
    if (theme_name === 'dark')
        document.documentElement.setAttribute('data-bs-theme', 'dark')
    else
        document.documentElement.setAttribute('data-bs-theme', 'light')
    document.cookie = `theme=${theme_name};path=/;`
}

SetTheme(cur_theme)