document.addEventListener("DOMContentLoaded", () => {
  onSubmitBtn();
});

function onSubmitBtn() {
  let btn = document.getElementById("safety-detection-btn");

  btn.addEventListener("click", async () => {
    let video = document.getElementById("video");
    if (!video.files[0]) {
      alert("Please upload video");
    } else {
      let isLoaded = false;

      const formData = new FormData();
      formData.append("video", video.files[0]);

      if (!isLoaded) {
        document.getElementById("preloader").style.display = "block";
      }

      const res = await fetch("safety-detection", {
        method: "POST",
        body: formData,
      })
        .then((data) => {
          isLoaded = true;
          return data.text();
        })
        .then((html) => {
          document.open();
          document.write(html);
          document.close();
        })
        .catch(() => {
          isLoaded = true;
        });

      if (isLoaded) {
        document.getElementById("preloader").style.display = "none";
      }
    }
  });
}
