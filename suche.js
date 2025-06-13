// Wenn es auf der gesamten Website nur 1 passenden Begriff gibt: Es leitet zur diesem Tab, scrollt dahin & markiert das Wort dort gelb.
// Wenn es auf der gesamten Website mehr als 1 passenden Begriff gibt: Es leitet zur einer weißen "Suchbegriffe" Seite und listet dort alle Tabs und kurze Ausschnitte auf.

const params = new URLSearchParams(window.location.search);
const suchbegriff = params.get('q');

const ergebnisContainer = document.getElementById('ergebnisse');

if (!suchbegriff) {
  ergebnisContainer.innerHTML = "Bitte gib einen Suchbegriff ein.";
} else {
  fetch('search-index.json')
    .then(res => res.json())
    .then(index => {
      const treffer = index
        .map(eintrag => {
          const textLower = eintrag.text.toLowerCase();
          const pos = textLower.indexOf(suchbegriff.toLowerCase());

          if (pos === -1) return null;

          const snippetStart = Math.max(0, pos - 60);
          const snippetEnd = Math.min(eintrag.text.length, pos + suchbegriff.length + 60);

          let snippet = eintrag.text.slice(snippetStart, snippetEnd);
          const regex = new RegExp(`(${suchbegriff})`, 'ig');
          snippet = snippet.replace(regex, '<mark>$1</mark>');

          return {
            url: eintrag.url,
            snippet: '... ' + snippet + ' ...'
          };
        })
        .filter(Boolean);

    if (treffer.length === 0) {
    ergebnisContainer.innerHTML = `Keine Ergebnisse für „${suchbegriff}“ gefunden.`;
    } else if (treffer.length === 1) {
    // Nur ein Treffer – direkt weiterleiten
    window.location.href = treffer[0].url + '?q=' + encodeURIComponent(suchbegriff);
    } else {
    // Mehrere Treffer anzeigen
    const list = document.createElement('ul');
    list.style.listStyle = "none";
    list.style.padding = "0";

    treffer.forEach(treffer => {
        const item = document.createElement('li');
        item.style.marginBottom = "2em";

        const link = document.createElement('a');
        link.href = treffer.url + '?q=' + encodeURIComponent(suchbegriff);  // Auch hier Query anhängen!
        link.textContent = treffer.url;
        link.style.fontWeight = "bold";
        link.style.fontSize = "1.1em";
        link.style.color = "#007acc";

        const snippet = document.createElement('p');
        snippet.innerHTML = treffer.snippet;
        snippet.style.margin = "0.5em 0";

        item.appendChild(link);
        item.appendChild(snippet);
        list.appendChild(item);
    });

    ergebnisContainer.innerHTML = '';
    ergebnisContainer.appendChild(list);
    }
    })
    .catch(err => {
      console.error("Fehler beim Laden des Index:", err);
      ergebnisContainer.innerHTML = "Fehler beim Laden der Suchdaten.";
    });
}
