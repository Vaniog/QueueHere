theme_btn = document.getElementById('theme-btn')

theme_btn.addEventListener('click', () => {
    let cur_theme = document.documentElement.getAttribute('data-bs-theme')
    if (cur_theme === 'dark')
        SetTheme('light')
    else
        SetTheme('dark')
})


cur_version = getCookie('version')

if (cur_version === null || cur_version < 1.0) {
    document.getElementById('info-notification').style.display = 'inline-block'
}

document.getElementById('update-ok-btn').addEventListener('click', () => {
    setCookie('version', 1.0)
    document.getElementById('info-notification').style.display = 'none'
})