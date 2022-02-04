$("#login-form").on("submit", (e) => {
  e.preventDefault();
  const id = $("#id").val();
  const pw = $("#pw").val();

  $.ajax({
    url: "/login",
    method: "POST",
    data: {
      id,
      pw,
    },
    success: (response) => {
      if (response["result"] === "fail") {
        alert(response["msg"]);
        return;
      }
      localStorage.setItem("userID", id);
      location.href = "/main";
    },
  });
});

$("#singup-form").on("submit", (e) => {
  e.preventDefault();
  const id = $("#id").val().trim();
  const pw = $("#pw").val().trim();
  const pw2 = $("#pw2").val().trim();
  if (id === "") {
    alert("아이디를 입력해주세요");
  } else if (pw === "" || pw2 === "") {
    alert("비밀번호를 입력해주세요");
  } else if (pw !== pw2) {
    alert("비밀번호가 일치하지 않습니다");
  } else {
    $.ajax({
      url: "/singup",
      data: { id, pw, pw2 },
      method: "POST",
      success: (response) => {
        if (response["result"] === "exist") {
          alert(response["msg"]);
        } else if (response["result"] === "succes") {
          alert(response["msg"]);
          location.href = "/";
        }
      },
    });
  }
});

$("#logout-btn").on("click", () => {
  console.log("로그아웃");
  localStorage.removeItem("userID");
  $.ajax({
    url: "/logout",
    success: () => {
      location.href = "/";
    },
  });
});

$("#write-form").on("submit", (e) => {
  e.preventDefault();
  const title = $("#title").val().trim();
  const contents = $("#contents").val().trim();
  const id = localStorage.getItem("userID");

  if (title === "") {
    alert("글 제목을 입력해주세요");
  } else if (contents === "") {
    alert("글 내용을 입력해주세요");
  } else {
    $.ajax({
      url: "/borad",
      method: "POST",
      data: {
        title,
        contents,
        id,
      },
      success: (res) => {
        if (res["result"] === "success") {
          location.href = "/main";
        }
      },
    });
  }
});
