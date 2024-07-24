let currentModel = 'mistral';
let currentTopK = 3;
let currentTemperature = 0.7;

function initSettings() {
    const settingItems = document.querySelectorAll('.setting-item');
    const modelOptions = document.querySelectorAll('.model-option');
    const topkSlider = document.getElementById('topk-slider');
    const topkValue = document.getElementById('topk-value');
    const temperatureSlider = document.getElementById('temperature-slider');
    const temperatureValue = document.getElementById('temperature-value');

    settingItems.forEach(item => {
        const button = item.querySelector('button');
        const options = item.querySelector('.setting-options');
    
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = options.classList.contains('show');
            
            settingItems.forEach(otherItem => {
                otherItem.querySelector('.setting-options').classList.remove('show');
            });
    
            if (!isVisible) {
                options.classList.add('show');
            }
        });
    });

    modelOptions.forEach(option => {
        option.addEventListener('click', () => {
            currentModel = option.dataset.model;
            console.log('Model changed to:', currentModel);
            modelOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
        });
    });

    topkSlider.addEventListener('input', () => {
        currentTopK = parseInt(topkSlider.value);
        topkValue.textContent = currentTopK;
        console.log('Top K changed to:', currentTopK);
    });

    temperatureSlider.addEventListener('input', () => {
        currentTemperature = parseFloat(temperatureSlider.value).toFixed(1);
        temperatureValue.textContent = currentTemperature;
        console.log('Temperature changed to:', currentTemperature);
    });

    document.addEventListener('click', () => {
        settingItems.forEach(item => {
            item.querySelector('.setting-options').classList.remove('show');
        });
    });

    document.querySelectorAll('.setting-options').forEach(options => {
        options.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
}