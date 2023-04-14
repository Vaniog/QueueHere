theme_btn = document.getElementById('theme-btn')

theme_btn.addEventListener('click', () => {
    let cur_theme = document.documentElement.getAttribute('data-bs-theme')
    if (cur_theme === 'dark')
        SetTheme('light')
    else
        SetTheme('dark')
})