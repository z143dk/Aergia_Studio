document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('interactive-video');
    const choiceOverlay = document.getElementById('choice-overlay');
    const choiceQuestion = document.getElementById('choice-question');
    const choiceButtonsContainer = document.getElementById('choice-buttons');

    let interactionManifest = null;

    // Get the storyboard ID from the URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const storyboardId = urlParams.get('id');

    if (!storyboardId) {
        document.body.innerHTML = '<h1>Error: No storyboard ID provided.</h1>';
        return;
    }

    // Define the paths to the video and manifest
    const videoPath = `/static/video/storyboard_${storyboardId}_final.mp4`;
    const manifestPath = `/static/video/storyboard_${storyboardId}_interaction_manifest.json`;

    // Set the video source
    video.src = videoPath;

    // Fetch the interaction manifest
    fetch(manifestPath)
        .then(response => {
            if (!response.ok) {
                throw new Error('Interaction manifest not found.');
            }
            return response.json();
        })
        .then(data => {
            interactionManifest = data;
            // Add a 'triggered' flag to each event to ensure it only fires once
            if (interactionManifest.events) {
                interactionManifest.events.forEach(event => event.triggered = false);
            }
            console.log('Interaction manifest loaded:', interactionManifest);
        })
        .catch(error => {
            console.warn(error.message);
            // If manifest is not found, the video will just play linearly.
        });

    // Listen for the video's time to update
    video.addEventListener('timeupdate', () => {
        if (!interactionManifest || !interactionManifest.events) return;

        const currentTime = video.currentTime;

        interactionManifest.events.forEach(event => {
            if (currentTime >= event.startTime && currentTime < event.endTime && !event.triggered) {
                event.triggered = true; // Mark as triggered
                video.pause();
                displayChoice(event.payload);
            }
        });
    });

    // Reset triggers if the user seeks backward
    video.addEventListener('seeking', () => {
        if (!interactionManifest || !interactionManifest.events) return;
        const currentTime = video.currentTime;
        interactionManifest.events.forEach(event => {
            if (currentTime < event.startTime) {
                event.triggered = false;
            }
        });
    });

    function displayChoice(payload) {
        choiceQuestion.textContent = payload.question;
        choiceButtonsContainer.innerHTML = ''; // Clear old buttons

        payload.choices.forEach(choice => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice.label;
            button.onclick = () => handleChoice(choice.seekTime);
            choiceButtonsContainer.appendChild(button);
        });

        choiceOverlay.style.display = 'block';
    }

    function handleChoice(seekTime) {
        choiceOverlay.style.display = 'none';
        video.currentTime = seekTime;
        video.play();
    }
});
