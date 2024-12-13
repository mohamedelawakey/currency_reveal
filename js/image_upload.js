function compareImages() {
    const file1 = document.getElementById('file1').files[0];
    const file2 = document.getElementById('file2').files[0];
    const errorMessage = document.getElementById('errorMessage');
    const results = document.getElementById('results');
    const uv1 = document.getElementById('uv1');
    const uv2 = document.getElementById('uv2');

    if (!file1 || !file2) {
        errorMessage.classList.remove('d-none');
        results.classList.remove('visible');
        return;
    }

    errorMessage.classList.add('d-none');
    results.classList.add('visible');

    uv1.src = URL.createObjectURL(file1);
    uv2.src = URL.createObjectURL(file2);
}