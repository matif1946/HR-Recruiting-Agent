let currentInterviewId = null;

// UI Elements
const screens = {
    setup: document.getElementById('setup-screen'),
    interview: document.getElementById('interview-screen'),
    results: document.getElementById('results-screen')
};

// Setup form
const setupForm = document.getElementById('setup-form');
const startBtn = document.getElementById('start-btn');
const setupError = document.getElementById('setup-error');

// Interview elements
const displayRole = document.getElementById('display-role');
const questionProgress = document.getElementById('question-progress');
const aiQuestion = document.getElementById('ai-question');
const interviewError = document.getElementById('interview-error');

// Silence Modal Elements
const silenceModal = document.getElementById('silence-modal');
const silenceRetryBtn = document.getElementById('silence-retry-btn');
const silenceTextBtn = document.getElementById('silence-text-btn');
const silenceEndBtn = document.getElementById('silence-end-btn');

// Voice interaction elements
const micBtn = document.getElementById('mic-btn');
const voiceStatus = document.getElementById('voice-status');
const transcriptPreview = document.getElementById('transcript-preview');
const endInterviewBtn = document.getElementById('end-interview-btn');

// Text fallback elements
const textFallbackContainer = document.getElementById('text-fallback-container');
const textAnswer = document.getElementById('text-answer');
const submitAnswerBtn = document.getElementById('submit-answer-btn');

// Results elements
const summaryText = document.getElementById('summary-text');
const strengthsList = document.getElementById('strengths-list');
const improvementsList = document.getElementById('improvements-list');
const assessmentText = document.getElementById('assessment-text');
const assessmentDisclaimer = document.getElementById('assessment-disclaimer');
const restartBtn = document.getElementById('restart-btn');

const resCandidateName = document.getElementById('res-candidate-name');
const resJobRole = document.getElementById('res-job-role');
const resExperienceLevel = document.getElementById('res-experience-level');

// Speech API objects
let recognition = null;
let synthesis = window.speechSynthesis;
let isVoiceSupported = false;
let isListening = false;
let isProcessing = false;
let isSpeaking = false;
let silenceTimeout = null;

function initVoice() {
    // Check SpeechRecognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        isVoiceSupported = true;

        recognition.onstart = () => {
            isListening = true;
            updateMicState('listening', 'Listening...');
            transcriptPreview.textContent = '';
            transcriptPreview.classList.remove('hidden');

            // Set up silence timeout handles prolonged silence (5 seconds)
            clearTimeout(silenceTimeout);
            silenceTimeout = setTimeout(() => {
                if (isListening && transcriptPreview.textContent.trim() === '') {
                    recognition.stop();
                    showSilenceModal();
                }
            }, 5000);
        };

        recognition.onresult = (event) => {
            clearTimeout(silenceTimeout);
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            transcriptPreview.textContent = finalTranscript || interimTranscript;
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            clearTimeout(silenceTimeout);
            isListening = false;
            updateMicState('idle', 'Ready');

            if (event.error === 'not-allowed' || event.error === 'service-not-allowed' || event.error === 'network' || event.error === 'audio-capture') {
                enableTextFallback();
            } else if (event.error === 'no-speech') {
                // 'no-speech' is often fired by the browser organically after a period of silence.
                // We show our silence modal when this happens, just like our manual timeout.
                if (transcriptPreview.textContent.trim() === '') {
                    showSilenceModal();
                }
            }
        };

        recognition.onend = () => {
            isListening = false;
            clearTimeout(silenceTimeout);

            // If we have a transcript, submit it automatically
            if (transcriptPreview.textContent.trim().length > 0) {
                const finalAnswer = transcriptPreview.textContent.trim();
                updateMicState('processing', 'Processing...');
                submitAnswer(finalAnswer);
            } else {
                updateMicState('idle', 'Ready');
                transcriptPreview.classList.add('hidden');
            }
        };
    } else {
        isVoiceSupported = false;
        console.warn('SpeechRecognition API not supported in this browser.');
    }
}

function speakQuestion(text) {
    if (!synthesis) {
        enableTextFallback();
        return;
    }

    // Stop any ongoing speech
    synthesis.cancel();

    if (!isVoiceSupported) return; // Don't speak if they are using text fallback from the start

    const utterance = new SpeechSynthesisUtterance(text);

    // Pick a good default voice (Google English or similar)
    const voices = synthesis.getVoices();
    const defaultVoice = voices.find(v => v.lang === 'en-US' && v.name.includes('Google')) || voices[0];
    if (defaultVoice) {
        utterance.voice = defaultVoice;
    }

    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
        isSpeaking = true;
        updateMicState('speaking', 'AI Speaking...');
        micBtn.disabled = true; // Prevent interrupting the AI
    };

    utterance.onend = () => {
        isSpeaking = false;
        micBtn.disabled = false;
        updateMicState('idle', 'Ready');
    };

    utterance.onerror = (e) => {
        console.error('Speech synthesis error', e);
        isSpeaking = false;
        micBtn.disabled = false;
        updateMicState('idle', 'Ready');
        enableTextFallback();
    };

    synthesis.speak(utterance);
}

function showSilenceModal() {
    isListening = false;
    updateMicState('idle', 'Ready');
    silenceModal.classList.remove('hidden');
}

function hideSilenceModal() {
    silenceModal.classList.add('hidden');
}

silenceRetryBtn.addEventListener('click', () => {
    hideSilenceModal();
    // Restart voice listening
    if (!isListening) {
        try {
            recognition.start();
        } catch (e) {
            console.error('Failed to start recognition:', e);
            enableTextFallback();
        }
    }
});

silenceTextBtn.addEventListener('click', () => {
    hideSilenceModal();
    enableTextFallback();
});

silenceEndBtn.addEventListener('click', () => {
    hideSilenceModal();
    endInterviewBtn.click();
});

function updateMicState(state, statusText) {
    micBtn.className = `mic-btn ${state}`;
    voiceStatus.textContent = statusText;

    if (state === 'processing') {
        micBtn.disabled = true;
        isProcessing = true;
    } else if (state === 'idle') {
        micBtn.disabled = false;
        isProcessing = false;
    }
}

function enableTextFallback() {
    isVoiceSupported = false;
    document.querySelector('.voice-interaction').classList.add('hidden');
    textFallbackContainer.classList.remove('hidden');

    // Stop any ongoing voice activities
    if (recognition && isListening) recognition.stop();
    if (synthesis && isSpeaking) synthesis.cancel();
}

function showScreen(screenName) {
    Object.values(screens).forEach(screen => {
        screen.classList.remove('active');
        screen.classList.add('hidden');
    });
    screens[screenName].classList.remove('hidden');
    screens[screenName].classList.add('active');
}

function showError(el, message) {
    el.textContent = message;
    el.classList.remove('hidden');
}

function hideError(el) {
    el.classList.add('hidden');
}

// Toggle Mic
micBtn.addEventListener('click', () => {
    if (isProcessing || isSpeaking) return;

    hideError(interviewError);

    if (isListening) {
        recognition.stop();
    } else {
        try {
            recognition.start();
        } catch (e) {
            console.error('Failed to start recognition:', e);
            enableTextFallback();
        }
    }
});

// Setup Event
setupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideError(setupError);

    const name = document.getElementById('candidate-name').value;
    const role = document.getElementById('job-role').value;
    const levelElement = document.querySelector('input[name="experience-level"]:checked');

    if (!levelElement) {
        showError(setupError, "Please select an experience level.");
        return;
    }
    const level = levelElement.value;

    startBtn.disabled = true;
    startBtn.textContent = 'Initializing...';

    // Initialize voice APIs only after a user interaction (browser requirement)
    initVoice();
    if (synthesis && synthesis.getVoices().length === 0) {
        // Safari/Chrome might need a moment to load voices
        synthesis.onvoiceschanged = () => { console.log('Voices loaded'); };
    }

    try {
        const response = await fetch('/api/interviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                job_role: role,
                experience_level: level
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to start interview');
        }

        const data = await response.json();
        currentInterviewId = data.interview_id;

        // Update Interview Screen UI
        displayRole.textContent = `${role} • ${level.replace(' Level', '')}`;
        questionProgress.textContent = `Question ${data.current_question_number} of 5`;
        aiQuestion.textContent = `"${data.latest_question}"`;

        if (!isVoiceSupported) {
            enableTextFallback();
        } else {
            document.querySelector('.voice-interaction').classList.remove('hidden');
            textFallbackContainer.classList.add('hidden');
        }

        showScreen('interview');

        // Speak the first question
        speakQuestion(data.latest_question);

    } catch (error) {
        showError(setupError, error.message);
    } finally {
        startBtn.disabled = false;
        startBtn.textContent = 'Start Interview';
    }
});

// Submit text answer fallback
submitAnswerBtn.addEventListener('click', async () => {
    const answer = textAnswer.value.trim();
    if (!answer) {
        showError(interviewError, 'Please type an answer before submitting.');
        return;
    }

    hideError(interviewError);
    updateMicState('processing', 'Processing...');
    submitAnswerBtn.disabled = true;
    textAnswer.disabled = true;

    await submitAnswer(answer);
});

async function submitAnswer(answer) {
    try {
        const response = await fetch(`/api/interviews/${currentInterviewId}/response`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answer: answer
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to submit answer');
        }

        const data = await response.json();

        if (data.is_completed) {
            await loadAssessment();
        } else {
            questionProgress.textContent = `Question ${data.current_question_number} of 5`;
            aiQuestion.textContent = `"${data.latest_question}"`;

            if (!isVoiceSupported) {
                textAnswer.value = '';
                textAnswer.disabled = false;
                submitAnswerBtn.disabled = false;
                textAnswer.focus();
                updateMicState('idle', 'Ready');
            } else {
                updateMicState('idle', 'Ready');
                transcriptPreview.classList.add('hidden');
                speakQuestion(data.latest_question);
            }
        }
    } catch (error) {
        showError(interviewError, error.message);
        updateMicState('idle', 'Ready');
        if (!isVoiceSupported) {
            textAnswer.disabled = false;
            submitAnswerBtn.disabled = false;
        }
    }
}

// End Interview Early
endInterviewBtn.addEventListener('click', async () => {
    if (!currentInterviewId) return;

    if (isListening) recognition.stop();
    if (isSpeaking) synthesis.cancel();

    if (confirm("Are you sure you want to end the interview early?")) {
        try {
            await fetch(`/api/interviews/${currentInterviewId}/end`, {
                method: 'POST'
            });
            await loadAssessment();
        } catch(e) {
            showError(interviewError, "Failed to end interview.");
        }
    }
});

async function loadAssessment() {
    if (isListening) recognition.stop();
    if (isSpeaking) synthesis.cancel();

    // Show a loading UI for assessment
    aiQuestion.textContent = 'Interview complete. Generating assessment...';
    document.querySelector('.voice-interaction').classList.add('hidden');
    textFallbackContainer.classList.add('hidden');
    endInterviewBtn.classList.add('hidden');
    updateMicState('processing', 'Processing...');

    try {
        const response = await fetch(`/api/interviews/${currentInterviewId}/assessment`);
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Failed to generate assessment');
        }

        const data = await response.json();

        if (resCandidateName) resCandidateName.textContent = data.candidate_name;
        if (resJobRole) resJobRole.textContent = data.applied_role;
        if (resExperienceLevel) resExperienceLevel.textContent = data.experience_level;

        summaryText.textContent = data.overall_summary;

        strengthsList.innerHTML = '';
        data.key_strengths.forEach(s => {
            const li = document.createElement('li');
            li.textContent = s;
            strengthsList.appendChild(li);
        });

        improvementsList.innerHTML = '';
        data.areas_for_improvement.forEach(s => {
            const li = document.createElement('li');
            li.textContent = s;
            improvementsList.appendChild(li);
        });

        assessmentText.textContent = data.overall_assessment;

        // Add color highlighting based on recommendation
        assessmentText.className = 'assessment-item-text'; // reset class
        if (data.overall_assessment.includes('RECOMMENDED TO PROCEED')) {
            assessmentText.style.color = '#15803d'; // green-700
            assessmentText.style.fontWeight = '600';
            assessmentText.style.backgroundColor = '#dcfce7'; // green-100
            assessmentText.style.padding = '0.5rem';
            assessmentText.style.borderRadius = '0.375rem';
        } else if (data.overall_assessment.includes('NOT RECOMMENDED')) {
            assessmentText.style.color = '#b91c1c'; // red-700
            assessmentText.style.fontWeight = '600';
            assessmentText.style.backgroundColor = '#fee2e2'; // red-100
            assessmentText.style.padding = '0.5rem';
            assessmentText.style.borderRadius = '0.375rem';
        }

        assessmentDisclaimer.textContent = data.disclaimer;

        showScreen('results');
    } catch (error) {
        showError(interviewError, error.message);
        endInterviewBtn.classList.remove('hidden');
        endInterviewBtn.textContent = 'Retry Assessment';
        endInterviewBtn.onclick = loadAssessment;
    }
}

restartBtn.addEventListener('click', () => {
    currentInterviewId = null;
    setupForm.reset();

    // Reset interview UI states
    endInterviewBtn.classList.remove('hidden');
    endInterviewBtn.textContent = 'End Interview';
    endInterviewBtn.onclick = null;

    transcriptPreview.classList.add('hidden');
    transcriptPreview.textContent = '';

    showScreen('setup');
});