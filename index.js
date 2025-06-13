// Globale Navigationsleiste
class Header extends HTMLElement {
  constructor() {
    super();
  }
  
  connectedCallback() {
    this.innerHTML = `
      <header>
        <nav>
          <ul id="Navigationsleiste">
              <li id="logo">FT</li>
              <li><a href="index.html">Home</a></li>
              <li><a href="news.html">News</a></li>
              <li><a href="physik.html">Physik</a></li>
              <li><a href="fotos.html">Fotos</a></li>
              <li><a href="modelleisenbahn.html">Modelleisenbahn</a></li>
              <!-- <li><a href="bjj.html">BJJ</a></li> -->
              <!-- <li><a href="dj.html">DJ</a></li> -->
              <li><a href="contact.html">Contact</a></li>
              <li><a href="about.html">About</a></li>
              <li><a href="sonstiges.html">Sonstiges</a></li>
              <li id="freak">
                <form id="site-search-form">
                  <input type="search" name="q" placeholder="Website durchsuchen" id="site-search-input">
                  <button id="searchButton">Suchen</button>
                </form>
              </li>
          </ul>
        </nav>
      </header>
    `;
  }
}

customElements.define('header-component', Header);

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("site-search-form");
  const input = document.getElementById("site-search-input");

  form.addEventListener("submit", e => {
    e.preventDefault(); // Verhindert Seiten-Neuladen
    const query = input.value.toLowerCase().trim();

    if (!query) return;


    // Seite nach dem Suchbegriff durchsuchen und markieren
    // const bodyText = document.body.textContent.toLowerCase();

    // const regex = new RegExp(`(${query})`, "gi");

    // let matches = 0;
    // const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);

    // while (walk.nextNode()) {
    //   const node = walk.currentNode;
    //   if (node.parentNode.tagName !== "SCRIPT" && node.nodeValue.toLowerCase().includes(query)) {
    //     const span = document.createElement("span");
    //     span.innerHTML = node.nodeValue.replace(regex, `<mark>$1</mark>`);
    //     node.parentNode.replaceChild(span, node);
    //     matches++;
    //   }
    // }

    // if (matches > 0) {
    //   alert(`"${query}" wurde ${matches}× auf dieser Seite gefunden und markiert.`);
    // } else {
    //   alert(`"${query}" wurde NICHT gefunden.`);
    // }


    // Bonus: output.json nach Bildbeschreibungen durchsuchen
    fetch("/Fotos/output.json")
      .then(res => res.json())
      .then(data => {
        let foundInJson = [];

        for (const [key, slides] of Object.entries(data)) {
          slides.forEach(slide => {
            const allText = [slide.alt, slide.description].join(" ").toLowerCase();
            if (allText.includes(query)) {
              foundInJson.push({ set: key, src: slide.src, description: slide.description });
            }
          });
        }

        if (foundInJson.length > 0) {
          console.log("Treffer in output.json:", foundInJson);

          // Optional: Anzeige unten auf der Seite
          const resultsContainer = document.getElementById("search-results") || document.createElement("div");
          resultsContainer.id = "search-results";
          resultsContainer.innerHTML = `<h3>Gefunden in Bildern:</h3>` + foundInJson.map(entry => `
            <div style="margin-bottom: 1em;">
              <strong>Set:</strong> ${entry.set}<br>
              <img src="${entry.src}" style="max-width:150px;"><br>
              <em>${entry.description}</em>
            </div>
          `).join("");
          document.body.appendChild(resultsContainer);
        }
      });


    // Seitenübergreifende Suche
    fetch("/search-index.json")
      .then(res => res.json())
      .then(pages => {
        const matchedPages = [];
        for (const [url, text] of Object.entries(pages)) {
          if (text.toLowerCase().includes(query)) {
            matchedPages.push(url);
          }
        }

        if (matchedPages.length > 0) {
          const list = matchedPages.map(url => `<li><a href="${url}">${url}</a></li>`).join("");
          const resultBox = document.createElement("div");
          resultBox.innerHTML = `<h3>Auch gefunden auf anderen Seiten:</h3><ul>${list}</ul>`;
          document.body.appendChild(resultBox);
        }
      });

  });
});

document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.getElementById("searchButton");
  const searchInput = document.querySelector('input[type="search"]');

  searchBtn?.addEventListener("click", () => {
    const query = searchInput.value.trim();
    if (query) {
      // Weiterleitung auf die Suchseite mit Suchbegriff als URL-Parameter
      window.location.href = `suche.html?q=${encodeURIComponent(query)}`;
    }
  });
});










// Fußzeile
class Footer extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
      <footer>
        <link rel="stylesheet" href="index.css">
        <ul>
          <li>
            <h1>Kontaktiere mich</h1>
            <a href="mailto:fabian.tanzer@t-online.de"> fabian.tanzer@t-online.de</a>
          </li>
          <li>
            <h1>Folge mir</h1>
            <ul class="LeisteSocialMediaLogos">
                <li class="SocialMediaLogo"><a href="https://www.facebook.com/fabian.tanzer.5" target="_blank" rel="noopener noreferrer"><img src="Logos/FacebookLogo/Facebook Brand Asset Pack/Logo/Primary Logo/Facebook_Logo_Primary.png" alt="Facebook Logo"></a></li>
                <li class="SocialMediaLogo"><a href="https://www.instagram.com/fa.bian_x/?hl=en" target="_blank" rel="noopener noreferrer"><img src="Logos/InstagramLogo/01 Static Glyph/01 Gradient Glyph/Instagram_Glyph_Gradient.png" alt="Instagram Logo"></a></li>
                <li class="SocialMediaLogo"><a href="https://www.linkedin.com/in/fabian-tanzer-3165ab21a/" target="_blank" rel="noopener noreferrer"><img src="Logos/LinkedInLogo/LinkedIn-Logos/LI-In-Bug.png" alt="LinkedIn Logo"></a></li>
                <li class="SocialMediaLogo"><a href="https://www.xing.com/profile/Fabian_Tanzer" target="_blank" rel="noopener noreferrer"><img src="Logos/XingLogo/icons8-xing.svg" alt="Xing Logo"></a></li>
            </ul>
          </li>
        </ul>
        <br>

        &copy Copyright 2025 | Fabian Tanzer | All rights reserved.
      </footer>
    `;
  }
}

customElements.define('footer-component', Footer);








// Slide-Show (Von https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_slideshow kopiert)
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}                       /*  Wenn man also beim letzten Foto auf nächstes Foto klickt, gelangt man wieder zum 1. Foto */
  if (n < 1) {slideIndex = slides.length}                       /*  Wenn man also beim 1. Foto auf vorheriges Foto klickt, gelangt man  zum letzten Foto */
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";                 /* Diese Zeile bringt Fehler unter "DEBUG CONSOLE", weil sie iwi nicht auf css zugreifen kann */
  dots[slideIndex-1].className += " active";
}
