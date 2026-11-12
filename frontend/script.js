let lastRequest = null;
let placeholders = {};
let generatedType = "";

const type = document.getElementById("type");
const topic = document.getElementById("topic");
const tone = document.getElementById("tone");
const toneBox = document.getElementById("toneBox");

const text = document.getElementById("text");
const task = document.getElementById("task");

const temperature = document.getElementById("temperature");
const temperatureValue =
    document.getElementById("temperatureValue");

const temperatureBox =
    document.getElementById("temperatureBox");

const result = document.getElementById("result");
const edit = document.getElementById("edit");
const fields = document.getElementById("placeholderFields");

const dot = document.getElementById("statusDot");


/* =========================
   DARK MODE
========================= */

if (localStorage.dark === "true") {
    document.body.classList.add("dark");
}

function darkMode() {

    document.body.classList.toggle("dark");

    localStorage.dark =
        document.body.classList.contains("dark");
}


/* =========================
   TOAST
========================= */

function showToast(message, type = "success") {

    const toast =
        document.getElementById("toast");

    toast.innerText = message;

    toast.className =
        "toast-" + type;

    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}


/* =========================
   TYPE
========================= */

function changeType() {

    if (type.value === "Quiz Generation") {

        toneBox.style.display = "none";

    } else {

        toneBox.style.display = "block";
    }
}


/* =========================
   TEMPERATURE
========================= */

function showTemperature() {

    const allowed = [
        "Correct Grammar",
        "Rewrite & Improve",
        "Summarize",
        "Expand"
    ];

    if (allowed.includes(task.value)) {

        temperatureBox.style.display = "block";

    } else {

        temperatureBox.style.display = "none";
    }
}

function updateTemperature() {

    temperatureValue.innerText =
        temperature.value;
}


/* =========================
   CLEAN TEXT
========================= */

function clean(value) {

    return value
        .replace(/\*\*/g, "")
        .replace(/^#{1,6}\s*/gm, "")
        .trim();
}


/* =========================
   GENERATE
========================= */

function runAI() {

    if (!topic.value.trim()) {

        return showToast(
            "Enter topic",
            "warning"
        );
    }

    generatedType = type.value;

    lastRequest = {

        mode: "generate",

        topic: topic.value.trim(),

        tone: tone.value.trim(),

        content_type: type.value
    };

    send(lastRequest);
}


/* =========================
   IMPROVE
========================= */

function improveAI() {

    if (!text.value.trim()) {

        return showToast(
            "Enter text",
            "warning"
        );
    }

    lastRequest = {

        mode: "improve",

        text: text.value,

        task: task.value,

        temperature:
            Number(temperature.value)
    };

    generatedType = "";

    send(lastRequest);
}


/* =========================
   API REQUEST
========================= */

async function send(data) {

    dot.classList.add("busy");

    try {

        const url =
            data.mode === "improve"
                ? "/generate-improve"
                : "/generate";

        const response = await fetch(url, {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(data)
        });

        const json =
            await response.json();

        if (!response.ok) {

            throw new Error(
                json.detail ||
                "Request failed"
            );
        }

        generatedType =
            json.content_type ||
            generatedType;

        /*
         * Quiz gets special HTML formatting.
         */
        if (
            data.mode === "generate" &&
            generatedType === "Quiz Generation"
        ) {

            displayQuiz(json.output);

        } else {

            result.innerText =
                clean(json.output);
        }

        /*
         * Email placeholders only.
         */
        edit.classList.toggle(
            "hide",
            !createFields(result.innerText)
        );

        showToast("Completed");

    } catch (error) {

        showToast(
            error.message,
            "error"
        );

    } finally {

        dot.classList.remove("busy");
    }
}


/* =========================
   QUIZ DISPLAY
========================= */

function displayQuiz(output) {

    const cleaned = clean(output);

    /*
     * Separate questions from answer key.
     */
    const parts =
        cleaned.split(
            /Answer\s*Key\s*:/i
        );

    const questionsPart =
        parts[0].trim();

    const answerKey =
        parts.length > 1
            ? parts[1].trim()
            : "";

    /*
     * Find every Question X block.
     */
    const questionBlocks =
        questionsPart.split(
            /(?=Question\s+\d+\s*:)/i
        );

    let html = "";

    questionBlocks.forEach(block => {

        block = block.trim();

        if (!block) {
            return;
        }

        /*
         * Question number.
         */
        const numberMatch =
            block.match(
                /^Question\s+(\d+)\s*:/i
            );

        if (!numberMatch) {
            return;
        }

        const number =
            numberMatch[1];

        /*
         * Question text.
         *
         * Everything between
         * "Question X:" and "A."
         */
        const questionMatch =
            block.match(
                /^Question\s+\d+\s*:\s*([\s\S]*?)(?=\s*\n?\s*A\.\s*)/i
            );

        if (!questionMatch) {
            return;
        }

        const question =
            questionMatch[1].trim();

        /*
         * Extract A, B, C and D.
         */
        const optionMatches = [
            ...block.matchAll(
                /(?:^|\n)\s*([A-D])\.\s*([^\n]*)(?=\n|$)/gi
            )
        ];

        /*
         * Ignore incomplete questions.
         */
        if (
            !question ||
            optionMatches.length < 4
        ) {
            return;
        }

        html +=
            '<div class="quiz-question">';

        html +=
            '<h3>Question ' +
            number +
            '</h3>';

        html +=
            '<p class="quiz-text">' +
            escapeHTML(question) +
            '</p>';

        html +=
            '<div class="quiz-options">';

        optionMatches
            .slice(0, 4)
            .forEach(match => {

                const letter =
                    match[1].toUpperCase();

                const option =
                    match[2].trim();

                html +=
                    '<div class="quiz-option">' +

                    '<span class="quiz-letter">' +
                    letter +
                    '.' +
                    '</span>' +

                    '<span>' +
                    escapeHTML(option) +
                    '</span>' +

                    '</div>';
            });

        html +=
            '</div>';

        html +=
            '</div>';
    });


    /*
     * Answer key.
     */
    if (answerKey) {

        html +=
            '<div class="quiz-answer-key">';

        html +=
            '<h3>Answer Key</h3>';

        html +=
            '<div class="answer-list">' +
            escapeHTML(answerKey) +
            '</div>';

        html +=
            '</div>';
    }


    /*
     * If parser fails,
     * show original text instead.
     */
    if (!html) {

        result.innerText =
            cleaned;

        return;
    }

    /*
     * Display formatted quiz.
     */
    result.innerHTML =
        html;
}


/* =========================
   HTML SAFETY
========================= */

function escapeHTML(text) {

    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* =========================
   EMAIL PLACEHOLDERS
========================= */

function createFields(content) {

    fields.innerHTML = "";

    placeholders = {};

    if (generatedType !== "Email") {

        return false;
    }

    const names = [
        ...new Set(
            [
                ...content.matchAll(
                    /\[([^\]]+)\]/g
                )
            ]
        )
    ].map(x => x[1]);

    if (!names.length) {

        return false;
    }

    names.forEach(name => {

        placeholders[name] = "";

        const input =
            document.createElement("input");

        input.placeholder = name;

        input.oninput = () => {

            placeholders[name] =
                input.value;
        };

        fields.appendChild(input);
    });

    return true;
}


/* =========================
   APPLY EMAIL DETAILS
========================= */

function applyDetails() {

    let output =
        result.innerText;

    Object.keys(placeholders)
        .forEach(key => {

            output =
                output.replaceAll(
                    `[${key}]`,
                    placeholders[key] ||
                    `[${key}]`
                );
        });

    result.innerText =
        output;

    edit.classList.add("hide");

    showToast(
        "Details filled"
    );
}


/* =========================
   REGENERATE
========================= */

function regenerate() {

    if (lastRequest) {

        send(lastRequest);

    } else {

        showToast(
            "No previous request",
            "warning"
        );
    }
}


/* =========================
   COPY
========================= */

function copyText() {

    navigator.clipboard.writeText(
        result.innerText
    );

    showToast("Copied");
}


/* =========================
   NOTION
========================= */

async function saveNotion() {

    try {

        const response =
            await fetch(
                "/save-notion",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text:
                            result.innerText
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to save"
            );
        }

        showToast("Saved");

    } catch (error) {

        showToast(
            error.message,
            "error"
        );
    }
}


/* =========================
   DOWNLOAD
========================= */

function downloadText() {

    const file =
        new Blob(
            [result.innerText],
            {
                type: "text/plain"
            }
        );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(file);

    link.download =
        "AI-output.txt";

    link.click();

    showToast("Downloaded");
}


/* =========================
   RESET
========================= */

function resetPage() {

    topic.value = "";

    tone.value = "";

    text.value = "";

    result.innerText =
        "Nothing generated yet.";

    fields.innerHTML = "";

    placeholders = {};

    edit.classList.add("hide");

    lastRequest = null;

    generatedType = "";

    showToast("Reset");
}


/* =========================
   INITIALIZE
========================= */

showTemperature();

changeType();