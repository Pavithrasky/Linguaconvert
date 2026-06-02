const sourceText = document.getElementById('sourceText');
const translatedText = document.getElementById('translatedText');
const fromLanguage = document.getElementById('fromLanguage');
const toLanguage = document.getElementById('toLanguage');
const translateBtn = document.getElementById('translateBtn');
const swapLanguages = document.getElementById('swapLanguages');
const translateMessage = document.getElementById('translateMessage');
const charCount = document.getElementById('charCount');
const copyOutput = document.getElementById('copyOutput');
const clearAll = document.getElementById('clearAll');
const sendMessage = document.getElementById('sendMessage');
const contactStatus = document.getElementById('contactStatus');

function showBanner(target, type, message) {
    target.className = `alert alert-${type}`;
    target.classList.remove('d-none');
    target.textContent = message;
}

sourceText?.addEventListener('input', () => {
    charCount.textContent = sourceText.value.length;
});

swapLanguages?.addEventListener('click', () => {
    const oldFrom = fromLanguage.value;
    fromLanguage.value = toLanguage.value;
    toLanguage.value = oldFrom;
    const oldSource = sourceText.value;
    sourceText.value = translatedText.value;
    translatedText.value = oldSource;
    charCount.textContent = sourceText.value.length;
});

translateBtn?.addEventListener('click', async () => {
    translateMessage.classList.add('d-none');
    translatedText.value = '';

    const payload = {
        text: sourceText.value,
        from: fromLanguage.value,
        to: toLanguage.value,
    };

    translateBtn.disabled = true;
    translateBtn.textContent = 'Translating...';

    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok || !data.ok) {
            throw new Error(data.error || 'Unable to translate right now.');
        }
        translatedText.value = data.translatedText;
        showBanner(translateMessage, 'success', 'Translation completed successfully.');
    } catch (error) {
        showBanner(translateMessage, 'danger', error.message);
    } finally {
        translateBtn.disabled = false;
        translateBtn.textContent = 'Translate';
    }
});

copyOutput?.addEventListener('click', async () => {
    if (!translatedText.value) return;
    await navigator.clipboard.writeText(translatedText.value);
    showBanner(translateMessage, 'success', 'Translated text copied to clipboard.');
});

clearAll?.addEventListener('click', () => {
    sourceText.value = '';
    translatedText.value = '';
    charCount.textContent = '0';
    translateMessage.classList.add('d-none');
});

sendMessage?.addEventListener('click', async () => {
    contactStatus.classList.add('d-none');
    const payload = {
        name: document.getElementById('contactName').value,
        email: document.getElementById('contactEmail').value,
        message: document.getElementById('contactMessage').value,
    };

    sendMessage.disabled = true;
    sendMessage.textContent = 'Sending...';

    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok || !data.ok) {
            throw new Error(data.error || 'Unable to send your message right now.');
        }
        showBanner(contactStatus, 'success', data.message);
        document.getElementById('contactName').value = '';
        document.getElementById('contactEmail').value = '';
        document.getElementById('contactMessage').value = '';
    } catch (error) {
        showBanner(contactStatus, 'danger', error.message);
    } finally {
        sendMessage.disabled = false;
        sendMessage.textContent = 'Send Message';
    }
});