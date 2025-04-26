async function generateImage() {
    const promptInput = document.getElementById('prompt');
    const typeSelect = document.getElementById('type');
    const styleSelect = document.getElementById('style');
    const resultDiv = document.getElementById('result');
    const generatedImage = document.getElementById('generatedImage');
    const errorP = document.getElementById('error');

    const prompt = promptInput.value.trim();
    const type = typeSelect.value;
    const style = styleSelect.value;

    // Проверка на пустой промпт
    if (!prompt) {
        errorP.style.display = 'block';
        errorP.textContent = 'Пожалуйста, введите описание изображения.';
        generatedImage.style.display = 'none';
        return;
    }

    // Очистка предыдущих результатов
    errorP.style.display = 'none';
    generatedImage.style.display = 'none';
    resultDiv.innerHTML = '<p>Генерация...</p>';
    console.log(`Sending request to /generate with prompt: ${prompt}, type: ${type}, style: ${style}`);

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt, type: type, style: style }),
        });

        const data = await response.json();
        console.log('Response from server:', data);

        if (data.image_url) {
            generatedImage.src = data.image_url;
            generatedImage.alt = `Generated Image: ${prompt}`;
            generatedImage.style.display = 'block';
            resultDiv.innerHTML = ''; // Очистить "Генерация..."
            resultDiv.appendChild(generatedImage);
        } else {
            errorP.style.display = 'block';
            errorP.textContent = 'Ошибка генерации изображения.';
        }
    } catch (error) {
        console.error('Error:', error);
        errorP.style.display = 'block';
        errorP.textContent = 'Ошибка при отправке запроса. Проверьте сервер.';
    }
}