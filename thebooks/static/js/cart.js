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
            alert('Cảm ơn bạn đã đặt hàng');
            location.reload();
        }
        else
            alert(data.error_message);
    })
}