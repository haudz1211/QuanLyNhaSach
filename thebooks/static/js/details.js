
function addComment(sachId) {
    let commentInput = document.getElementById(`comment-${sachId}`);
    let commentText = commentInput.value.trim();

    if (commentText === "") {
        alert("Bình luận không được để trống!");
        return;
    }

    if (confirm("Bạn chắc chắn muốn thêm bình luận?")) {
        fetch(`/api/sach/${sachId}/binh_luan`, {
            method: "POST",
            body: JSON.stringify({ "binh_luan": commentText }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => {
            console.log("Response:", res);
            return res.json();
        })
        .then(data => {
            console.log("Data:", data);
            if (data.status === 200) {
                // Thêm bình luận như trước
                 location.reload();
            } else {
                alert(data.err_msg || "Có lỗi xảy ra!");
            }
        })
        .catch(err => {
            console.error("Fetch error:", err);
            alert("Đã xảy ra lỗi. Vui lòng thử lại sau!");
        });

    }
}

// Hàm cập nhật thời gian với Moment.js
function updateTimeAgo() {
    let dates = document.getElementsByClassName("date");
    for (let d of dates) {
        d.innerText = moment(d.innerText).locale("vi").fromNow();
    }
}
