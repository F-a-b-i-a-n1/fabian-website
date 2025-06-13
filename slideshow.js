// Es wäre ziemlich aufwändig hier alles manuell für jedes einzelne Foto einzutragen. Deshalb erstellt generate_slideshow_data.py mithilfe bildbeschreibungen.json (Hier muss ich die Beschreibung natürlich schon selber eintragen) automatisch die Bildbeschreibungen inkl. Fotoeigenschaften.
const urlParams = new URLSearchParams(window.location.search);
const setName = urlParams.get("set");
const container = document.getElementById("slideshow-container");
const dotsContainer = document.getElementById("dots-container");

// Neue zentrale JSON laden
fetch('./Fotos/output.json')
  .then(res => res.json())
  .then(allSlideshows => {
    const keyMap = {
      Lusen: "2021_LusenSonnenuntergang",
      Berlin: "2022_Berlin",
      Bibione: "2022_Bibione",
      Dresden: "2022_Dresden",
      Hamburg: "2023_Hamburg",
      Koenigssee: "2023_Koenigssee"
    };

    function getFolderName(set) {
      return keyMap[set] || set;
    }

    const realKey = keyMap[setName] || setName;
    const slides = allSlideshows[realKey];

    if (!slides || slides.length === 0) {
      container.innerHTML = `<p style="text-align:center;">Kein Bildersatz "${setName}" gefunden.</p>`;
      return;
    }

    slides.forEach((slide, i) => {
      const figure = document.createElement("figure");
      figure.className = "mySlides fade";
      figure.style.display = "none";
      figure.innerHTML = `
        <div class="numbertext">${i + 1} / ${slides.length}</div>
        <img src="${slide.src}" alt="${slide.alt}" style="width:100%">
        <figcaption style="text-align:center;">${slide.description}</figcaption>
        <div class="button-container">
          <a href="${slide.src}" download>
            <button class="btn">Download</button>
          </a>
        </div>
      `;
      container.appendChild(figure);

      const dot = document.createElement("span");
      dot.className = "dot";
      dot.addEventListener("click", () => showSlides(i));
      dotsContainer.appendChild(dot);
    });

    let slideIndex = 0;

    function showSlides(n) {
      const slidesElems = document.querySelectorAll(".mySlides");
      const dots = document.querySelectorAll(".dot");

      if (n >= slidesElems.length) slideIndex = 0;
      else if (n < 0) slideIndex = slidesElems.length - 1;
      else slideIndex = n;

      slidesElems.forEach((slide, i) => {
        slide.style.display = (i === slideIndex) ? "block" : "none";
      });

      dots.forEach((dot, i) => {
        dot.className = (i === slideIndex) ? "dot active" : "dot";
      });
    }

    function plusSlides(n) {
      showSlides(slideIndex + n);
    }

    // Start Slideshow
    showSlides(slideIndex);

    // Download-All-Button einfügen, falls Ordnername bekannt ist
    // Es ist zwar richtig, dass der zip Ordner kaum komprimiert ist (Weil jpg bereits komprimiert ist & somit kaum mehr komprimiert werden kann. Man kann jedoch im Browser ohne zip Ordner keinen Ordner downloaden!)
    // const downloadContainer = document.getElementById("download-all-container");
    // const availableZipDownloads = ["Lusen", "Berlin", "Bibione"];
    // if (availableZipDownloads.includes(setName)) {
    //   const zipPath = `Fotos/${getFolderName(setName)}.zip`;
    //   downloadContainer.innerHTML = `
    //     <a href="${zipPath}" download>
    //       <button class="btn">Alle Fotos downloaden</button>
    //     </a>
    //   `;
    // }
  })

  .catch(err => {
    container.innerHTML = `<p style="text-align:center;">Fehler beim Laden der Slideshow-Daten.</p>`;
    console.error(err);
  });
