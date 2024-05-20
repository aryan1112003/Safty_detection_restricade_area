document.addEventListener("DOMContentLoaded", function () {
  const unsafety = document.getElementById("unsafety").innerHTML;
  const safety = document.getElementById("safety").innerHTML;
  const helmet = document.getElementById("helmet").innerHTML;
  const vest = document.getElementById("vest").innerHTML;
  const no_helmet = document.getElementById("no_helmet").innerHTML;
  const no_vest = document.getElementById("no_vest").innerHTML;

  google.charts.load("current", { packages: ["corechart"] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    const data = google.visualization.arrayToDataTable([
      ["Result", "Percentage"],
      ["Safety", parseFloat(safety)],
      ["Unsafety", parseFloat(unsafety)],
    ]);
    const data2 = google.visualization.arrayToDataTable([
      ["Result", "Percentage"],
      ["Helmet", parseFloat(helmet)],
      ["Vest", parseFloat(vest)],
      ["No Helmet", parseFloat(no_helmet)],
      ["No Vest", parseFloat(no_vest)],
    ]);

    const options = {
      backgroundColor: "transparent",
      fontColor: "#000",
      width: 280,
      height: 330,
      chartArea: { width: "100%", height: "80%" },
      legend: {
        textStyle: {
          color: "#000",
          fontSize: 14,
        },
        position: "bottom",
      },
      pieSliceTextStyle: {
        color: "#fff",
        fontSize: 14,
      },
    };

    const chart = new google.visualization.PieChart(
      document.getElementById("myChart")
    );
    const chart2 = new google.visualization.PieChart(
      document.getElementById("myChart2")
    );
    chart.draw(data, options);
    chart2.draw(data2, options);
  }
});
