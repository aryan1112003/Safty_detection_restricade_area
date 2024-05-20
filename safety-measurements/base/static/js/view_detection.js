document.addEventListener("DOMContentLoaded", () => {
  viewDetectionDelete();
  viewPopup();
});

function viewDetectionDelete() {
  let viewDetectionDelete = document.getElementsByClassName(
    "viewDetectionDelete"
  );

  for (let element of viewDetectionDelete) {
    element.addEventListener("click", async () => {
      if (confirm("Are you sure?")) {
        let detection_id = element.getAttribute("data");
        let isLoaded = false;
        if (!isLoaded) {
          document.getElementById("preloader").style.display = "block";
        }
        await fetch(`view-detection?detection_id=${detection_id}`, {
          method: "GET",
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
}

function viewPopup() {
  let view = document.getElementsByClassName("view");

  for (let element of view) {
    element.addEventListener("click", async () => {
      let detection_stats = JSON.parse(element.getAttribute("data"));

      let popupContainer = document.getElementById("popup-container");
      let popupData = document.getElementById("popup-data");

      document.getElementById(
        "popup-heading"
      ).innerHTML = `${detection_stats.type} Statstics`;

      if (detection_stats.type == "Safety") {
        let html = `
        <p>Helmet = ${detection_stats.helmet}%</P>
        <p>No Helmet = ${detection_stats.no_helmet}%</P>
        <p>Vest = ${detection_stats.vest}%</P>
        <p>No Vest = ${detection_stats.no_vest}%</P>
        <p>Safety(Helmet + Vest) = ${detection_stats.safety}%</P>
        <p>Unsafety(No Helmet + No Vest) = ${detection_stats.unsafety}%</P>
        `;
        popupData.innerHTML = html;
      } else if (detection_stats.type == "Restricted Area") {
              let html = `
        <p>Person count = ${detection_stats.count}</p>
        `;
        html += `<table class="rwd-table">
        <tbody>
        <tr>
        <td>Id</td>
        <td>Entry time</td>
        <td>Exit time</td>
        </tr>
        `;
        for (let i = 0; i < detection_stats.stats.length; i++) {
          let enter = detection_stats.stats[i].enter_time
          let exit = detection_stats.stats[i].exit_time
          enter = enter !== null ? new Date(enter * 1000).toLocaleString() : 'Not Found'
          exit = exit !== null ? new Date(exit * 1000).toLocaleString() : 'Not Found'
          html += `
          <tr>
          <td>${detection_stats.stats[i].id}</td>
          <td>${enter}</td>
          <td>${exit}</td>
          </tr>
          `;
        }
        html += `
        </tbody>
        </table>
        `;
        popupData.innerHTML = html;
      }
      popupContainer.style.display = "flex";
      popupContainer.style.alignItems = "center";
      popupContainer.style.justifyContent = "center";
    });
  }
}

function closePopup() {
  document.getElementById("popup-container").style.display = "none";
}
