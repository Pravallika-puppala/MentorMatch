// ==========================================================
// MentorMatch Frontend
// ==========================================================

const API_URL = "https://mentormatch-26rn.onrender.com";

let currentStudentId = null;


// ==========================================================
// ELEMENTS
// ==========================================================

const heroFindMentors = document.getElementById("hero-find-mentors");
const profileForm = document.getElementById("student-profile-form");
const formStatus = document.getElementById("form-status");
const mentorGrid = document.getElementById("mentor-grid");
const recommendationSubtitle = document.getElementById("recommendation-subtitle");


// AI Companion

const companionToggle = document.getElementById("companion-toggle");
const companionPopup = document.getElementById("companion-popup");
const closeCompanion = document.getElementById("close-companion");
const chatInput = document.getElementById("companion-input");
const chatButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const navCompanionButton = document.getElementById("nav-companion-button");


// ==========================================================
// HERO → PROFILE
// ==========================================================

heroFindMentors.addEventListener("click", () => {

    document
        .getElementById("student-profile")
        .scrollIntoView({
            behavior: "smooth"
        });

});


// ==========================================================
// CREATE STUDENT ID
// ==========================================================

function generateStudentId() {

    const randomNumber = Math.floor(
        10000 + Math.random() * 90000
    );

    return `S${randomNumber}`;
}


// ==========================================================
// SUBMIT STUDENT PROFILE
// ==========================================================

profileForm.addEventListener("submit", async (event) => {

    event.preventDefault();


    const name =
        document.getElementById("student-name")
            .value.trim();

    const careerGoal =
        document.getElementById("career-goal")
            .value.trim();

    const skills =
        document.getElementById("skills")
            .value.trim();

    const interests =
        document.getElementById("interests")
            .value.trim();

    const experienceLevel =
        document.getElementById("experience-level")
            .value;

    const preferredIndustry =
        document.getElementById("preferred-industry")
            .value.trim();

    const availability =
        document.getElementById("availability")
            .value.trim();


    currentStudentId = generateStudentId();


    const submitButton =
        document.getElementById("find-my-mentors");


    formStatus.textContent =
        "Creating your profile...";

    submitButton.disabled = true;
    submitButton.style.opacity = "0.6";


    try {

        // ==================================================
        // SAVE STUDENT
        // ==================================================

        const createResponse = await fetch(
            `${API_URL}/students`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    student_id: currentStudentId,
                    name: name,
                    career_goal: careerGoal,
                    skills: skills,
                    interests: interests,
                    experience_level: experienceLevel,
                    preferred_industry: preferredIndustry,
                    availability: availability

                })
            }
        );


        if (!createResponse.ok) {

            const errorData =
                await createResponse
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                "Could not create student profile."
            );
        }


        // ==================================================
        // GET RECOMMENDATIONS
        // ==================================================

        formStatus.textContent =
            "Finding your best mentor matches...";


        const recommendationResponse =
            await fetch(
                `${API_URL}/students/${currentStudentId}/recommendations`
            );


        if (!recommendationResponse.ok) {

            const errorData =
                await recommendationResponse
                    .json()
                    .catch(() => null);

            throw new Error(
                errorData?.detail ||
                "Could not load mentor recommendations."
            );
        }


        const recommendations =
            await recommendationResponse.json();


        // ==================================================
        // DISPLAY MENTORS
        // ==================================================

        renderMentors(recommendations);


        formStatus.textContent =
            "Your mentor matches are ready.";


        recommendationSubtitle.textContent =
            `Personalized matches for ${name}.`;


        document
            .getElementById("mentors")
            .scrollIntoView({
                behavior: "smooth"
            });


    } catch (error) {

        console.error(
            "MentorMatch error:",
            error
        );

        formStatus.textContent =
            error.message ||
            "Something went wrong. Please try again.";

    } finally {

        submitButton.disabled = false;
        submitButton.style.opacity = "1";

    }

});


// ==========================================================
// RENDER TOP 5 MENTORS
// ==========================================================

function renderMentors(mentors) {

    mentorGrid.innerHTML = "";


    if (!mentors || mentors.length === 0) {

        mentorGrid.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    ✦
                </div>

                <h3>
                    No mentor matches found.
                </h3>

                <p>
                    Try adjusting your profile
                    preferences and search again.
                </p>

            </div>

        `;

        return;
    }


    mentors.forEach((mentor, index) => {

        const card =
            document.createElement("div");

        card.className =
            "mentor-card";


        const matchPercentage =
            Math.round(
                mentor.match_probability * 100
            );


        const initial =
            mentor.mentor_name
                ? mentor.mentor_name
                    .charAt(0)
                    .toUpperCase()
                : "?";


        let reasonsHTML = "";


        if (
            mentor.reasons &&
            Array.isArray(mentor.reasons)
        ) {

            reasonsHTML =
                mentor.reasons
                    .map(reason => `

                        <p class="mentor-reason">
                            ✓ ${escapeHTML(reason)}
                        </p>

                    `)
                    .join("");

        }


        card.innerHTML = `

            <span class="mentor-rank">
                MATCH ${String(index + 1).padStart(2, "0")}
            </span>

            <span class="mentor-match">
                ${matchPercentage}%
            </span>

            <div class="mentor-avatar-small">
                ${escapeHTML(initial)}
            </div>

            <h3>
                ${escapeHTML(
                    mentor.mentor_name
                )}
            </h3>

            <p class="mentor-role">
                ${escapeHTML(
                    mentor.role
                )}
            </p>

            <div class="mentor-reasons">

                <span class="mentor-reasons-title">
                    Why this mentor?
                </span>

                ${reasonsHTML}

            </div>

            <button
                class="view-mentor"
                type="button"
            >
                View mentor →
            </button>

        `;


        // ==================================================
        // VIEW MENTOR
        // ==================================================

        const viewButton =
            card.querySelector(".view-mentor");


        viewButton.addEventListener(
            "click",
            () => {

                openMentorModal(
                    mentor,
                    matchPercentage
                );

            }
        );


        mentorGrid.appendChild(card);

    });

}


// ==========================================================
// MENTOR DETAIL MODAL
// ==========================================================

function openMentorModal(
    mentor,
    matchPercentage
) {

    // Remove an existing modal

    const existingModal =
        document.getElementById(
            "mentor-modal"
        );

    if (existingModal) {
        existingModal.remove();
    }


    const modal =
        document.createElement("div");

    modal.id =
        "mentor-modal";

    modal.className =
        "mentor-modal";


    // ==================================================
    // REASONS
    // ==================================================

    let reasonsHTML = "";


    if (
        mentor.reasons &&
        Array.isArray(mentor.reasons)
    ) {

        reasonsHTML =
            mentor.reasons
                .map(reason => `

                    <div class="modal-reason">

                        <span>✓</span>

                        <p>
                            ${escapeHTML(reason)}
                        </p>

                    </div>

                `)
                .join("");

    }


    const initial =
        mentor.mentor_name
            ? mentor.mentor_name
                .charAt(0)
                .toUpperCase()
            : "?";


    // ==================================================
    // MODAL HTML
    // ==================================================

    modal.innerHTML = `

        <div class="mentor-modal-backdrop"></div>


        <div class="mentor-modal-card">

            <button
                class="mentor-modal-close"
                type="button"
                aria-label="Close mentor details"
            >
                ×
            </button>


            <div class="modal-top">

                <div class="modal-avatar">
                    ${escapeHTML(initial)}
                </div>


                <div>

                    <span class="modal-label">
                        Mentor match
                    </span>

                    <div class="modal-match">
                        ${matchPercentage}%
                    </div>

                </div>

            </div>


            <div class="modal-profile">

                <h2>
                    ${escapeHTML(
                        mentor.mentor_name
                    )}
                </h2>

                <p>
                    ${escapeHTML(
                        mentor.role
                    )}
                </p>

            </div>


            <div class="modal-divider"></div>


            <div class="modal-section">

                <span class="modal-section-title">
                    Why this mentor?
                </span>


                <div class="modal-reasons">

                    ${reasonsHTML}

                </div>

            </div>


            <div class="modal-footer">

                <span>
                    Mentor ID:
                    ${escapeHTML(
                        mentor.mentor_id
                    )}
                </span>


                <button
                    class="modal-close-button"
                    type="button"
                >
                    Close
                </button>

            </div>

        </div>

    `;


    document.body.appendChild(modal);


    // ==================================================
    // CLOSE BUTTONS
    // ==================================================

    const closeButtons =
        modal.querySelectorAll(
            ".mentor-modal-close, .modal-close-button"
        );


    closeButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                modal.remove();

            }
        );

    });


    // ==================================================
    // CLOSE BACKDROP
    // ==================================================

    const backdrop =
        modal.querySelector(
            ".mentor-modal-backdrop"
        );


    backdrop.addEventListener(
        "click",
        () => {

            modal.remove();

        }
    );


    // ==================================================
    // ESCAPE KEY
    // ==================================================

    function escapeHandler(event) {

        if (event.key === "Escape") {

            modal.remove();

            document.removeEventListener(
                "keydown",
                escapeHandler
            );

        }

    }


    document.addEventListener(
        "keydown",
        escapeHandler
    );

}


// ==========================================================
// HTML ESCAPING
// ==========================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;
}


// ==========================================================
// AI COMPANION — OPEN
// ==========================================================

function openCompanion() {

    companionPopup.classList.add(
        "active"
    );


    setTimeout(() => {

        chatInput.focus();

    }, 100);

}


// ==========================================================
// AI COMPANION — CLOSE
// ==========================================================

function closeCompanionPopup() {

    companionPopup.classList.remove(
        "active"
    );

}


// ==========================================================
// FLOATING COMPANION BUTTON
// ==========================================================

companionToggle.addEventListener(
    "click",
    () => {

        if (
            companionPopup.classList.contains(
                "active"
            )
        ) {

            closeCompanionPopup();

        } else {

            openCompanion();

        }

    }
);


// ==========================================================
// NAV AI COMPANION
// ==========================================================

navCompanionButton.addEventListener(
    "click",
    () => {

        openCompanion();

    }
);


// ==========================================================
// CLOSE COMPANION
// ==========================================================

closeCompanion.addEventListener(
    "click",
    () => {

        closeCompanionPopup();

    }
);


// ==========================================================
// SEND AI MESSAGE
// ==========================================================

async function sendMessage(message) {

    if (!message.trim()) {
        return;
    }


    if (!currentStudentId) {

        const messageElement =
            document.createElement("div");

        messageElement.className =
            "message ai-message";

        messageElement.textContent =
            "Create your student profile first so I can give you personalized guidance.";

        chatMessages.appendChild(
            messageElement
        );

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

        return;
    }


    // User message

    const userMessage =
        document.createElement("div");

    userMessage.className =
        "message user-message";

    userMessage.textContent =
        message;

    chatMessages.appendChild(
        userMessage
    );


    chatInput.value = "";


    // Loading

    const loadingMessage =
        document.createElement("div");

    loadingMessage.className =
        "message ai-message";

    loadingMessage.textContent =
        "Thinking...";

    chatMessages.appendChild(
        loadingMessage
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    try {

        const response =
            await fetch(
                `${API_URL}/students/${currentStudentId}/companion`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Failed to contact AI Companion."
            );

        }


        const data =
            await response.json();


        loadingMessage.remove();


        const aiMessage =
            document.createElement("div");

        aiMessage.className =
            "message ai-message";

        aiMessage.textContent =
            data.response;

        chatMessages.appendChild(
            aiMessage
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;


    } catch (error) {

        console.error(
            "AI Companion error:",
            error
        );


        loadingMessage.textContent =
            "Sorry, I couldn't connect to the AI Companion.";

    }

}


// ==========================================================
// ENTER TO SEND
// ==========================================================

chatInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {

            event.preventDefault();

            const message =
                chatInput.value;

            if (message.trim()) {

                sendMessage(message);

            }

        }

    }
);


// ==========================================================
// BUTTON TO SEND
// ==========================================================

chatButton.addEventListener(
    "click",
    () => {

        const message =
            chatInput.value;

        if (message.trim()) {

            sendMessage(message);

        }

    }
);
