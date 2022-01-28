function removeElement(elementId) {
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}
function updateSneakyInput() {
    var sneakyInput = document.getElementById("sneaky");
    sneakyInput.value = EATperKg.toFixed(2); // two decimal places
}
function advancedOption(){
    var checkBox = document.getElementById("advanced_check");
    var adCalc = document.getElementById("advanced_calc");
    if (checkBox.checked/* == true*/){
        adCalc.style.display = "block";
    } else {
        adCalc.style.display = "none";
    }
}
function addAct(){
    var time = document.getElementById("hours").value; // time from the time input
    if (time){
        var select = document.getElementById("sel"); // select element
        var name = select.options[select.selectedIndex].innerHTML; // name of chosen activity
        var epkgh = select.options[select.selectedIndex].value; // value of chosen activity
        var container = document.getElementById("user_act-s"); // div where new activities created

        //creating div for new activity
        var newDiv = document.createElement("div");
        actIdCounter = actIdCounter + 1; // incrementing the identifier of the block
        newDiv.id = "act" + actIdCounter;

        //creating spans for time and epkgh, because this values must be accessible
        var timeSpan = document.createElement("span");
        timeSpan.innerHTML = time;
        var epkghSpan = document.createElement("span");
        epkghSpan.innerHTML = epkgh;
        epkghSpan.setAttribute("style", "visibility: hidden;"); // user don't need to see it
        // but it has to be stored nearby for delAct() function

        //creating button
        var clickme = document.createElement("button"); // creating delete button
        clickme.innerHTML = "Remove";
        clickme.type = "button";
        clickme.setAttribute("onclick", "delAct(" + actIdCounter + ")");

        // arranging div elements in order with plain text in between
        newDiv.appendChild(timeSpan);
        newDiv.innerHTML += " hour"; if (time !== "1"){newDiv.innerHTML += "s"}
        newDiv.innerHTML += " of " + name;
        newDiv.appendChild(clickme);
        newDiv.appendChild(epkghSpan);
        container.appendChild(newDiv); // adding new created div to the container div

        //calculating calories contribution
        time = parseFloat(time);
        epkgh = parseFloat(epkgh);
        EATperKg += epkgh * time;
        updateSneakyInput();
    } else {
        alert("Please, enter the number of hours");
    }
}
function delAct(id){
    // collecting data from spans and converting to float
    var time  = document.getElementById("act" + id).getElementsByTagName("span")[0].innerHTML;
    var epkgh = document.getElementById("act" + id).getElementsByTagName("span")[1].innerHTML;
    time = parseFloat(time);
    epkgh = parseFloat(epkgh);

    EATperKg -= epkgh * time; //calculating calories contribution

    updateSneakyInput();

    removeElement("act" + id); //removing activity note
}
// Global variables
var actIdCounter = 0;
var EATperKg = 0;
