let selectedGender = 'male';

function selectVoice(gender) {
    selectedGender = gender;

    // Update UI
    document.querySelectorAll('.voice-option').forEach(option => {
        option.classList.remove('selected');
        if (option.getAttribute('data-gender') === gender) {
            option.classList.add('selected');
        }
    });

    // Optional: Add a subtle sound or feedback here
    console.log(`Voice selected: ${gender}`);
}

async function generateSpeech() {
    const textInput = document.getElementById('textInput');
    const text = textInput.value.trim();
    const btn = document.getElementById('generateBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('loadingSpinner');

    if (!text) {
        alert("Please enter some text to convert.");
        return;
    }

    // UI Loading State
    btn.disabled = true;
    btnText.textContent = "Generating...";
    spinner.style.display = "block";

    try {
        const response = await fetch('/speak', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                gender: selectedGender
            }),
        });

        if (response.ok) {
            console.log("Speech generation started");

            // Handle binary audio data
            const blob = await response.blob();
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);

            audio.onended = () => {
                URL.revokeObjectURL(audioUrl); // Clean up
            };

            await audio.play();

        } else {
            const data = await response.json();
            console.error("Error:", data.error);
            alert("Error generating speech: " + data.error);
        }

    } catch (error) {
        console.error("Network Error:", error);
        alert("Network error occurred.");
    } finally {
        // Reset UI State
        setTimeout(() => {
            btn.disabled = false;
            btnText.textContent = "Convert to Speech";
            spinner.style.display = "none";
        }, 1000); // Small delay to prevent flickering if response is too fast
    }
}

// Character Count
document.getElementById('textInput').addEventListener('input', function () {
    const currentLength = this.value.length;
    document.getElementById('charCount').textContent = currentLength;
});
