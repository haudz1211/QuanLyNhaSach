function addComment(sachId) {
    if (confirm("Bạn chắc chắn thêm bình luận?") === true) {
        fetch(`/api/sach/${sachId}/binh_luan`, {
            method: "post",
            body: JSON.stringify({
                "binh_luan": document.getElementById('comment').value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.status === 200) {
                let c = data.comment;
                let d = document.getElementById("comments");
                d.innerHTML = `
                    <div class="row alert alert-info">
                        <div class="col-md-1 col-xs-4">
                            <img src="${c.khach_hang.avatar}" class="img-fluid rounded" />
                        </div>
                        <div class="col-md-11 col-xs-8">
                            <p><strong>${c.binh_luan}</strong></p>
                            <p>Bình luận lúc: <span class="date">${ moment(c.ngay_tao).locale("vi").fromNow() }</span></p>
                        </div>
                    </div>
                ` + d.innerHTML;
            } else
                alert(data.err_msg);
        })
    }
}