$(document).ready(function () {

    let siriWave = null;

    /* ================= TEXT ANIMATION ================= */
    if ($('.tlt').length) {
        $('.tlt').textillate({
            loop: true,
            in: { effect: "bounceIn" },
            out: { effect: "bounceOut" }
        });
    }

    if ($('.siri-message').length) {
        $('.siri-message').textillate({
            loop: true,
            in: { effect: "fadeInUp" },
            out: { effect: "fadeOutUp" }
        });
    }

    /* ================= CHAT HISTORY ================= */
    function addMessage(text, sender) {

        const msgClass = sender === "user"
            ? "sender_message ms-auto"
            : "receiver_message me-auto";

        const html = `
        <div class="d-flex mb-2">
            <div class="${msgClass} width-size">${text}</div>
        </div>`;

        $("#chat-history").append(html);
        $("#chat-history").scrollTop($("#chat-history")[0].scrollHeight);
    }


    /* ================= PYTHON -> UI MESSAGE ================= */

    eel.expose(DisplayMessage);

    function DisplayMessage(message) {
        addMessage(message, "bot");
    }


    /* ================= MIC BUTTON ================= */
    $("#MicBtn").on("click", async function () {

        $("#Oval").fadeOut(300, function () {
            $("#SiriWave").fadeIn(300);
        });

        if (!siriWave) {
            siriWave = new SiriWave({
                container: document.getElementById("siri-container"),
                width: 640,
                height: 200,
                style: "ios9",
                speed: 0.12,
                amplitude: 1.2,
                autostart: true
            });
        }

        try {
            await eel.allCommands()();
        } catch (err) {
            console.error("EEL Error:", err);
        }
    });


    /* ================= CHAT BUTTON ================= */
    $("#ChatBtn").on("click", function () {
        $("#ChatSection").fadeToggle(200);
        $("#Oval").toggle();
        $("#SiriWave").hide();
    });


    /* ================= TEXT COMMAND ================= */
    $("#chatbox").on("keypress", async function (e) {

        if (e.which === 13) {

            const text = $("#chatbox").val().trim();
            if (!text) return;

            addMessage(text, "user");
            $("#chatbox").val("");

            try {

                const reply = await eel.textCommand(text)();

                if (reply) {
                    addMessage(reply, "bot");
                }

            } catch (err) {

                addMessage("Error executing command", "bot");
                console.error(err);

            }

        }

    });

});
