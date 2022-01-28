function changeMenuIcon(imgToHide, imgToView) {
    imgToHide.style.display = "none";
    imgToView.style.display = "block";
}

function openAsideMenu() {
    var imgOff = document.getElementById("nav-menu-ico--off");
    var imgOn = document.getElementById("nav-menu-ico--on");
    var aside = document.getElementById("nav-menu");
    changeMenuIcon(imgOff, imgOn);
    aside.className = "opened";
}

function closeAsideMenu() {
    var imgOff = document.getElementById("nav-menu-ico--off");
    var imgOn = document.getElementById("nav-menu-ico--on");
    var aside = document.getElementById("nav-menu");
    changeMenuIcon(imgOn, imgOff);
    aside.className = "";
}
