function addToCart(id) {
    fetch('/api/gio_hang', {
        method: 'post',
        body: JSON.stringify({
            'id': id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let cartCounts = document.getElementsByClassName('cart-count');
        for (let c of cartCounts)
            c.innerText = data.tong_so_luong;
    });
}

function updateCart(id, obj) {
    obj.disable = true;

    fetch(`/api/gio_hang/${id}`, {
        method: 'put',
        body: JSON.stringify({
            'so_luong': obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        obj.disable = false;
        let cartCounts = document.getElementsByClassName('cart-count')
        for(let c of cartCounts)
            c.innerText = data.tong_so_luong;

        let cartAmounts = document.getElementsByClassName('cart-amount')
        for (let c of cartAmounts)
            c.innerText = data.tong_tien.toLocaleString('en');
    })
}

function deleteCart(id, obj) {
    fetch(`/api/gio_hang/${id}`, {
        method: 'delete',
    }).then(res => res.json()).then(data => {
        obj.disable = true;
        let cartCounts = document.getElementsByClassName('cart-count')
        for(let c of cartCounts)
            c.innerText = data.tong_so_luong;

        let cartAmounts = document.getElementsByClassName('cart-amount')
        for (let c of cartAmounts)
            c.innerText = data.tong_tien.toLocaleString('en');

        let item = document.getElementById(`book${id}`);
        item.style.display = 'none';
    })
}


function pay() {
    fetch('/api/dat_hang', {
        method: 'post'
    }).then(res => res.json()).then(data => {
        if (data.status === 200) {
            // Hiển thị thông báo thành công bằng SweetAlert2
            Swal.fire({
                icon: 'success',
                title: 'Đặt hàng thành công!',
                text: 'Cảm ơn bạn đã đặt hàng!',
                showConfirmButton: false,
                timer: 2000 // Tự động đóng sau 2 giây
            }).then(() => location.reload()); // Reload trang sau khi thông báo đóng
        } else {
            // Hiển thị thông báo lỗi bằng SweetAlert2
            Swal.fire({
                icon: 'error',
                title: 'Có lỗi xảy ra!',
                text: data.error_message, // Hiển thị lỗi từ backend
                confirmButtonText: 'OK'
            });
        }
    }).catch(error => {
        // Hiển thị lỗi kết nối bằng SweetAlert2
        Swal.fire({
            icon: 'error',
            title: 'Lỗi kết nối!',
            text: 'Không thể kết nối tới server. Vui lòng thử lại sau.',
            confirmButtonText: 'OK'
        });
    });
}

function pay() {
    // Lấy thông tin từ các trường cần thiết
    let phone = document.getElementById('phone').value;  // Lấy số điện thoại khách hàng
    let orderAmount = document.getElementById('order-amount').innerText.replace(' VNĐ', '').replace(',', ''); // Lấy tổng tiền

    // Kiểm tra thông tin đầu vào
    if (!phone) {
        alert("Vui lòng nhập số điện thoại khách hàng.");
        return;
    }

    // Tạo đối tượng dữ liệu cần gửi đi
    let orderData = {
        phone: phone,
        totalAmount: orderAmount
    };

    // Gửi yêu cầu thanh toán tới backend
    fetch('/api/payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Thanh toán thành công!");
            // Bạn có thể thực hiện hành động sau khi thanh toán thành công, ví dụ như cập nhật trạng thái đơn hàng
        } else {
            alert("Thanh toán thất bại: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Có lỗi xảy ra trong quá trình thanh toán.");
    });
}

function payAdmin() {
    // Lấy thông tin số điện thoại và tổng tiền từ trang admin
    let phone = document.getElementById('admin-phone').value;  // Số điện thoại khách hàng
    let orderAmount = document.getElementById('admin-order-amount').innerText.replace(' VNĐ', '').replace(',', ''); // Tổng tiền

    // Kiểm tra thông tin
    if (!phone) {
        alert("Vui lòng nhập số điện thoại khách hàng.");
        return;
    }

    // Tạo dữ liệu cần gửi
    let orderData = {
        phone: phone,
        totalAmount: orderAmount
    };

    // Gửi yêu cầu thanh toán đến backend
    fetch('/admin/api/payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Thanh toán thành công!");
            // Sau khi thanh toán thành công, có thể chuyển hướng hoặc làm mới trang
        } else {
            alert("Thanh toán thất bại: " + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Có lỗi xảy ra trong quá trình thanh toán.");
    });
}


