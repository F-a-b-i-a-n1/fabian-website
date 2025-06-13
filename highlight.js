// highlight.js
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const suchbegriff = params.get('q');
  if (!suchbegriff) return;

  const regex = new RegExp(`(${suchbegriff})`, 'ig');
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let found = false;

  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.nodeValue.match(regex)) {
      const span = document.createElement('span');
      span.innerHTML = node.nodeValue.replace(regex, '<mark>$1</mark>');
      node.parentNode.replaceChild(span, node);
      if (!found) {
        span.scrollIntoView({ behavior: 'smooth', block: 'center' });
        found = true;
      }
    }
  }
});
