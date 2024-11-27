function edit() {
    const items = document.querySelectorAll('#profile>input');
    const inputFile = document.getElementById('input-file');
    inputFile.style.display = 'block';
    items.forEach(item => item.disabled = false);
}

function updateProfile() {
    const inputFile = document.getElementById('input-file');
    const hoTen = document.getElementById('ho-ten').value;
    const sdt = document.getElementById('sdt').value;
    const email = document.getElementById('email').value;
    const diaChi = document.getElementById('dia-chi').value;

    const formData = new FormData();
    formData.append('ten', hoTen);
    formData.append('sdt', sdt);
    formData.append('email', email);
    formData.append('dia_chi', diaChi);
    if (inputFile.files[0]) {
        formData.append('avatar', inputFile.files[0]);
    }

    fetch('/api/khach_hang', {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cập nhật hồ sơ thành công");
        } else {
            alert("Cập nhật hồ sơ thất bại");
        }
    })
    .catch(error => console.error('Error:', error));
}
