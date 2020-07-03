icons = document.querySelectorAll("i.nav-menu");
nav = document.querySelector("nav.site-nav");

icons.forEach(icon => {
    icon.addEventListener("click", () => {
        if (icon.getAttribute("data-nav-action") === "open") {
            nav.style.right = "0";
        }
        else {
            nav.style.right = "-1000px";
        }
    });
});