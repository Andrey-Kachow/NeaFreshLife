function openSuggestions() {
    document.getElementById("suggestions-opener").style.maxHeight = "0px";
    document.getElementById("suggestions").style.maxHeight = "900px";
}

function changeIcon(icon){
    var iconPk = icon.id.substring(4);

    var addToFavUrl = "add_to_favourite/" + iconPk;
    var removeFavUrl = "remove_from_favourite/" + iconPk;
    var addToIgnoreUrl = "add_to_ignore/" + iconPk;
    var removeIgnoreUrl = "remove_from_ignore/" + iconPk;

    if (icon.className.includes("ico--inactive")) {

        icon.classList.remove("ico--inactive");
        if (icon.className.includes("fa-ban")) {
            icon.classList.add("ico--red");
            icon.href = removeIgnoreUrl;
        } else if (icon.className.includes("fa-star")) {
            icon.classList.add("ico--yellow");
            icon.href = removeFavUrl;
        }
    } else {

        if (icon.className.includes("fa-ban")) {
            icon.classList.remove("ico--red");
            icon.href = addToIgnoreUrl;
        } else if (icon.className.includes("fa-star")) {
            icon.classList.remove("ico--yellow");
            icon.href = addToFavUrl;
        }
        icon.classList.add("ico--inactive");
    }
}

$("a.fas").click(function(event){
    event.preventDefault();
    $.ajax({
        type: 'POST',  // should be POST!
        url: event.currentTarget.href,
        data: {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: changeIcon(event.currentTarget)
    })
});


// $(".ntr-angle").click(rotateAngle);

// $(".ntr-sign").click(function (event) {
//     openCloseTable(event.target);
// });



