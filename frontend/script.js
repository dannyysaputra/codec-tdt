const fileInput = document.querySelector('#fileInput')

function checkFileType(type = null) {
  document.querySelectorAll('.preview').forEach(e => e.style.display = 'none')
  document.querySelectorAll('.downloadBtn').forEach(e => e.style.display = 'none')
  if (type != null) document.querySelector(`#${type}Preview`).style.display = 'flex'
}
checkFileType()

fileInput.addEventListener('change', function () {
  const [file] = fileInput.files
  const [type] = file.type.split('/')
  let previewUrl = URL.createObjectURL(file);

  switch (type) {
    case 'image':
      document.querySelector(`#imagePreview img`).src = previewUrl
      break;
    case 'audio':
      document.querySelector(`#audioPreview audio`).src = previewUrl
      break;
    case 'video':
      document.querySelector(`#videoPreview video`).src = previewUrl
      break;
    default:
      checkFileType()
      this.value = null
      alert('Silahkan pilih file dari salah satu berikut (gambar, audio, video)')
      return;
  }
  checkFileType(type)
  setTimeout(() => URL.revokeObjectURL(previewUrl), 1000)
})

document
  .getElementById("uploadForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const file = fileInput.files[0];
    const fileType = file.type.split('/')[0]
    if (!['image', 'audio', 'video'].includes(fileType)) return alert('Silahkan pilih file dari salah satu berikut (gambar, audio, video)')

    document.querySelector('form button').disabled = true
    const formData = new FormData();
    formData.append("file", file);

    // DCT/FFT cutoff logic
    const cutoff = document.getElementById("qualitySlider");
    if (cutoff) {
      formData.append("cutoff", cutoff.value);
    }

    const response = await fetch(`http://localhost:5000/compress/${fileType}`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    const result = `data:image/jpeg;base64,${data[`compressed_${fileType}`]}`;
    document.querySelector(`#${fileType}Preview .compressed`).src = result;
    document.querySelector(`#${fileType}Preview .compressed`).classList.add('w-100');
    document.querySelector(
      `#${fileType}Preview .compressionInfo`
    ).innerText = `Compression Reduced: ${data.compression_ratio}%`;
    document.querySelector(`#${fileType}Preview .downloadBtn`).style.display = 'block';
    document.querySelector(`#${fileType}Preview .downloadBtn`).href = result;

    document.querySelector('form button').disabled = false
  });
