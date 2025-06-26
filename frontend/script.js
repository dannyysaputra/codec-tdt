const slider = document.getElementById("qualitySlider");
const sliderValue = document.getElementById("sliderValue");
slider.oninput = () => {
  sliderValue.innerText = slider.value;
};

document
  .getElementById("uploadForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const fileInput = document.getElementById("fileInput");
    const fileType = document.getElementById("fileType").value;
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // DCT/FFT cutoff logic
    const cutoffSlider = document.getElementById("qualitySlider");
    if (cutoffSlider) {
      formData.append("cutoff", cutoffSlider.value);
    }

    // Tampilkan original audio
    if (fileType === "audio") {
      const audioURL = URL.createObjectURL(file);
      document.getElementById("originalAudio").src = audioURL;
    }

    const response = await fetch(`http://localhost:5000/compress/${fileType}`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (fileType === "image") {
      const resultImg = `data:image/jpeg;base64,${data.compressed_image}`;
      document.getElementById("compressedImage").src = resultImg;
      document.getElementById(
        "compressionInfo"
      ).innerText = `Compression Reduced: ${data.compression_ratio}%`;
      document.getElementById("downloadBtn").href = resultImg;
    }

    if (fileType === "audio") {
      const resultAudio = `data:audio/wav;base64,${data.compressed_audio}`;
      document.getElementById("compressedAudio").src = resultAudio;
      document.getElementById(
        "compressionAudioInfo"
      ).innerText = `Compression Reduced: ${data.compression_ratio}%`;
      document.getElementById("downloadAudioBtn").href = resultAudio;
    }
  });
