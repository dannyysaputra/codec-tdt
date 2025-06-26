document.addEventListener('DOMContentLoaded', () => {
    // Element selectors
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileTypeSelect = document.getElementById('fileType');
    const qualitySlider = document.getElementById('qualitySlider');
    const sliderValueSpan = document.getElementById('sliderValue');
    const submitBtn = document.getElementById('submitBtn');
    
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('resultContainer');
    const originalMediaWrapper = document.getElementById('originalMediaWrapper');
    const compressedMediaWrapper = document.getElementById('compressedMediaWrapper');
    const originalSizeSpan = document.getElementById('originalSize');
    const compressedSizeSpan = document.getElementById('compressedSize');
    const reductionRatioSpan = document.getElementById('reductionRatio');
    const downloadBtn = document.getElementById('downloadBtn');

    // Update slider value display
    qualitySlider.addEventListener('input', () => {
        sliderValueSpan.textContent = qualitySlider.value;
    });

    // Form submission logic
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            alert('Please select a file first.');
            return;
        }

        // UI updates for loading
        submitBtn.disabled = true;
        submitBtn.textContent = 'Compressing...';
        resultContainer.style.display = 'none';
        loader.style.display = 'block';

        // Prepare data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('cutoff_level', qualitySlider.value);
        const fileType = fileTypeSelect.value;
        
        try {
            // API call
            const response = await fetch(`http://127.0.0.1:5000/compress/${fileType}`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || 'An unknown error occurred.');
            }

            const data = await response.json();
            
            // Display results
            displayResults(file, data, fileType);

        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            // Reset UI
            loader.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Compress File';
        }
    });

    function displayResults(originalFile, compressedData, fileType) {
        // Clear previous results
        originalMediaWrapper.innerHTML = '';
        compressedMediaWrapper.innerHTML = '';

        const originalUrl = URL.createObjectURL(originalFile);
        let compressedUrl;

        // Create media elements
        if (fileType === 'image') {
            compressedUrl = `data:image/jpeg;base64,${compressedData.image_base64}`;
            originalMediaWrapper.innerHTML = `<img src="${originalUrl}" alt="Original Image">`;
            compressedMediaWrapper.innerHTML = `<img src="${compressedUrl}" alt="Compressed Image">`;
            downloadBtn.download = 'compressed_image.jpg';
        } else if (fileType === 'audio') {
            compressedUrl = `data:audio/mp3;base64,${compressedData.audio_base64}`;
            originalMediaWrapper.innerHTML = `<div id="originalWaveform"></div><audio src="${originalUrl}" controls></audio>`;
            compressedMediaWrapper.innerHTML = `<div id="compressedWaveform"></div><audio src="${compressedUrl}" controls></audio>`;
            
            // Initialize Wavesurfer
            initWavesurfer('#originalWaveform', originalUrl, '#e0e0e0', '#d1d1d1');
            initWavesurfer('#compressedWaveform', compressedUrl, '#4a90e2', '#357ABD');
            downloadBtn.download = 'compressed_audio.mp3';

        } else if (fileType === 'video') {
            compressedUrl = `data:video/mp4;base64,${compressedData.video_base64}`;
            originalMediaWrapper.innerHTML = `<video src="${originalUrl}" controls></video>`;
            compressedMediaWrapper.innerHTML = `<video src="${compressedUrl}" controls></video>`;
            downloadBtn.download = 'compressed_video.mp4';
        }

        // Update info and show container
        originalSizeSpan.textContent = formatBytes(compressedData.original_size);
        compressedSizeSpan.textContent = formatBytes(compressedData.compressed_size);
        reductionRatioSpan.textContent = `${compressedData.compression_ratio}%`;
        
        downloadBtn.href = compressedUrl;
        downloadBtn.style.display = 'inline-block';
        resultContainer.style.display = 'grid';
    }

    function initWavesurfer(container, url, waveColor, progressColor) {
        WaveSurfer.create({
            container,
            waveColor,
            progressColor,
            height: 100,
            responsive: true,
            barWidth: 2,
            barRadius: 3
        }).load(url);
    }

    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    }
});
