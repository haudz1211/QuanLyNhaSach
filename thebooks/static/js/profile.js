function edit() {
    const items = document.querySelectorAll('#profile>input');
    const inputFile = document.getElementById('input-file');
    inputFile.style.display = 'block';
    items.forEach(item => item.disabled = false);
}

function updateProfile() {
    const image = document.getElementById('input-file').value
    const hoTen = document.getElementById('ho-ten').value
    const sdt = document.getElementById('sdt').value
    const email = document.getElementById('email').value
    const diaChi = document.getElementById('dia-chi').value

    fetch('/api/khach_hang', {
        method: 'put',
        body: JSON.stringify({
            'ten': hoTen,
            'sdt': sdt,
            'email': email,
            'avatar': image,
            'dia_chi': diaChi
        }),
        headers: {}

    })
}