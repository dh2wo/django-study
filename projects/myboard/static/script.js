// 1. 글쓰기와 수정에서 쓸 수 있는 함수
/// 제목이 비어있거나 또는 5글자 이하라면 경고창 표시,
/// 글 내용이 비어있거나 10 글자 이하라면 경고창 표시,
// 제목이나 글 내용에 바보, 멍청이, 한조 들어있으면 경고창 표시하고 진행 멈춤

function valiDation() {
  let title = document.getElementById("title").value;
  let content = document.getElementById("content").value;

  if (title.trim() == "" || title.trim().length < 5) {
    alert("제목이 비어있거나 5글자 이하입니다.");
    return false;
  }

  if (content.trim() == "" || content.trim().length < 10) {
    alert("내용이 비어있거나 10글자 이하입니다.");
    return false;
  }

  let bad = ["바보", "멍청이", "한조"];

  for (let n = 0; n < bad.length; n++) {
    if (title.includes(bad[n]) || content.includes(bad[n])) {
      alert(bad[n] + "(은)는 사용할 수 없는 단어입니다.");
      alert("금지어 : " + bad);
      return false;
    }
  }
}

// 2. 댓글에서 쓸 수 있는 함수
/// 댓글 창 비어있으면 경고창 표시
function valiDationReply(button) {
  let buttonText = button.value;
  let replyWrite = replyTextWrite.value;
  let replyUpdate = replyTextUpdate.value;

  if (buttonText.includes("쓰기")) {
    if (replyWrite.trim() == "") {
      alert("댓글이 비어있습니다.");
      return false;
    } else {
      writeReply();
    }
  } else if (buttonText.includes("수정")) {
    if (replyUpdate.trim() == "") {
      alert("수정 댓글이 비어있습니다.");
      return false;
    } else {
      updateReply();
    }
  }
}
