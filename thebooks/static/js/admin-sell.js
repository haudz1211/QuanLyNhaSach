function addOrder() {
    let sachId = document.getElementById('sachId').value;
    fetch(`/api/don_hang/${sachId}`, {
        method: 'GET'
    })
    .then(res => res.json())
    .then(data => {
        let bookItem = document.getElementById(`book${data.sach.id}`);
        let quantityBook = document.getElementById(`quantity-book${data.sach.id}`);

        if (bookItem) {
            // Cập nhật số lượng sách nếu đã có trong đơn hàng
            quantityBook.value = data.sach.so_luong;
        } else {
            // Thêm sách mới vào đơn hàng
            let item = document.getElementById('startRow');
            item.innerHTML += `<tr id="book${data.sach.id}">
                                    <th class="align-middle">${data.sach.id}</th>
                                    <th class="align-middle">${data.sach.ten}</th>
                                    <th class="align-middle">${data.sach.the_loai}</th>
                                    <th class="align-middle w-25">
                                        <input type="number" id="quantity-book${data.sach.id}" onblur="updateOrder(${data.sach.id}, this)" class="form-control w-100" value="${data.sach.so_luong}" />
                                    </th>
                                    <th class="align-middle">${data.sach.gia.toLocaleString('en')} VNĐ</th>
                                    <th>
                                        <button onclick="deleteOrder(${data.sach.id}, this)" class="btn btn-danger">&times;</button>
                                    </th>
                                </tr>`;
        }

        // Cập nhật tổng số lượng và tổng tiền
        let orderCount = document.getElementById('order-count');
        let orderAmount = document.getElementById('order-amount');

        orderCount.innerText = data.thong_tin.tong_so_luong;
        orderAmount.innerText = data.thong_tin.tong_tien.toLocaleString('en') + ' VNĐ';
    })
    .catch(error => console.error('Error:', error));
}

function updateOrder(id, obj) {
    obj.disabled = true;

    fetch(`/api/don_hang/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ 'so_luong': obj.value }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        obj.disabled = false;

        let orderCount = document.getElementById('order-count');
        let orderAmount = document.getElementById('order-amount');

        orderCount.innerText = data.tong_so_luong;
        orderAmount.innerText = data.tong_tien.toLocaleString('en') + ' VNĐ';
    })
    .catch(error => {
        obj.disabled = false;
        console.error('Error:', error);
    });
}

function deleteOrder(id, obj) {
    obj.disabled = true;

    fetch(`/api/don_hang/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        let orderCount = document.getElementById('order-count');
        let orderAmount = document.getElementById('order-amount');

        orderCount.innerText = data.tong_so_luong;
        orderAmount.innerText = data.tong_tien.toLocaleString('en') + ' VNĐ';

        let bookItem = document.getElementById(`book${id}`);
        if (bookItem) {
            bookItem.remove(); // Xóa sách khỏi bảng
        }
    })
    .catch(error => {
        obj.disabled = false;
        console.error('Error:', error);
    });
}

function findCustomer() {
    let sdt = document.getElementById('phone').value;
    fetch(`/api/khach_hang/${sdt}`, {
        method: 'GET'
    })
    .then(res => res.json())
    .then(data => {
        let customerInfo = document.getElementById('customer-info');
        if (data.id !== undefined) {
            customerInfo.innerHTML = `<h3 class="col-md-12">Thông tin khách hàng:</h3>
                                        <ul class="list-group col-md-6"> 
                                          <li class="list-group-item">Mã khách hàng: <span id="khach-hang-id">${data.id}</span></li>
                                          <li class="list-group-item">Họ tên: ${data.ten}</li>
                                          <li class="list-group-item">Số điện thoại: ${data.sdt}</li>
                                          <li class="list-group-item">Địa chỉ: ${data.dia_chi}</li>
                                        </ul>`;
        } else {
            customerInfo.innerHTML += `<div class='alert alert-danger col-md-12 mx-3 mt-3'>Không tìm thấy khách hàng</div>`;
        }
    })
    .catch(error => console.error('Error:', error));
}

function pay() {
    let item = document.getElementById('khach-hang-id').innerText;
    let khachHangId = parseInt(item);

    fetch('/api/don_hang/dat_hang', {
        method: 'POST',
        body: JSON.stringify({ 'khach_hang_id': khachHangId }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);  // In log dữ liệu để kiểm tra
        if (data.status === 200) {
            alert('Đặt hàng thành công');
            location.reload();
        } else {
            alert(data.error_message || 'Đặt hàng không thành công');
        }
    })
    .catch(error => console.error('Error:', error));
}


function payWithMoMo() {
    console.log('Nút thanh toán MoMo đã được click.');
    let item = document.getElementById('khach-hang-id').innerText;
    let khachHangId = parseInt(item);

    // Giả sử bạn đã có thông tin đơn hàng cần thiết
    fetch('/api/don_hang/dat_hang', {
        method: 'POST',
        body: JSON.stringify({
            'khach_hang_id': khachHangId,
            'payment_method': 'MoMo' // Thêm phương thức thanh toán
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);  // In log dữ liệu để kiểm tra
        if (data.status === 200) {
            // Giả sử bạn cần chuyển hướng đến trang thanh toán MoMo
            window.location.href = data.payment_url; // URL thanh toán từ server
        } else {
            alert(data.error_message || 'Thanh toán không thành công');
        }
    })
    .catch(error => console.error('Error:', error));
}
