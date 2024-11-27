// function addComment(sachId) {
//     if (confirm("Bạn chắc chắn thêm bình luận?") === true) {
//         fetch(`/api/sach/${sachId}/binh_luan`, {
//             method: "post",
//             body: JSON.stringify({
//                 "binh_luan": document.getElementById('comment').value
//             }),
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         }).then(res => res.json()).then(data => {
//             if (data.status === 200) {
//                 let c = data.comment;
//                 let d = document.getElementById("comments");
//                 d.innerHTML = `
//                     <div class="row alert alert-info">
//                         <div class="col-md-1 col-xs-4">
//                             <img src="${c.khach_hang.avatar}" class="img-fluid rounded" />
//                         </div>
//                         <div class="col-md-11 col-xs-8">
//                             <p><strong>${c.binh_luan}</strong></p>
//                             <p>Bình luận lúc: <span class="date">${ moment(c.ngay_tao).locale("vi").fromNow() }</span></p>
//                         </div>
//                     </div>
//                 ` + d.innerHTML;
//             } else
//                 alert(data.err_msg);
//         })
//     }
// }
//
//  // Sự kiện khi người dùng nhấn nút thêm bình luận
// document.getElementById("addCommentButton").onclick = function() {
//     let commentText = document.getElementById("commentInput").value;
//
//     $.ajax({
//         type: "POST",
//         url: "/api/sach/${sachId}/binh_luan",  // URL của server để xử lý thêm bình luận
//         data: { comment: commentText },
//         success: function(newCommentHtml) {
//             // Thêm bình luận mới vào danh sách mà không load lại trang
//             let commentsContainer = document.getElementById("commentsContainer");
//             commentsContainer.innerHTML += newCommentHtml;
//
//             // Reset nội dung ô nhập bình luận
//             document.getElementById("commentInput").value = "";
//
//             // Định dạng thời gian với moment.js
//             updateTimeAgo();
//         },
//         error: function() {
//             alert("Đã xảy ra lỗi khi thêm bình luận.");
//         }
//     });
// };

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
