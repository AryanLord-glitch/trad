$(document).ready(function () {

    /* ===== DISPLAY MESSAGE ABOVE SIRI ===== */
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $(".siri-message").textillate("start");
    }

    /* ===== RETURN TO MAIN UI ===== */
    eel.expose(ShowHood);
    function ShowHood() {

        console.log("🔁 UI reset");

        // stop siri wave safely
        if (window.siriWave) {
            window.siriWave.stop();
        }

        $("#SiriWave").fadeOut(300, function () {
            $("#Oval").fadeIn(300);
        });
    }

});

