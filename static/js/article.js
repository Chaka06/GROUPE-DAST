/**
 * Article page: auto-generate Table of Contents from headings.
 */
"use strict";

const tocContent = document.getElementById("tocContent");
const article    = document.querySelector(".article__content");

if (tocContent && article) {
  const headings = article.querySelectorAll("h2, h3");

  if (headings.length > 2) {
    const ul = document.createElement("ul");
    ul.style.cssText = "list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px;";

    headings.forEach((h, i) => {
      if (!h.id) h.id = `heading-${i}`;
      const li = document.createElement("li");
      const a  = document.createElement("a");
      a.href = `#${h.id}`;
      a.textContent = h.textContent;
      if (h.tagName === "H3") a.style.paddingLeft = "1rem";
      li.appendChild(a);
      ul.appendChild(li);
    });

    tocContent.appendChild(ul);

    // Highlight active heading
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const id   = entry.target.id;
          const link = tocContent.querySelector(`a[href="#${id}"]`);
          if (!link) return;
          if (entry.isIntersecting) {
            tocContent.querySelectorAll("a").forEach((a) => a.classList.remove("is-active"));
            link.classList.add("is-active");
          }
        });
      },
      { rootMargin: "-80px 0px -70% 0px" }
    );

    headings.forEach((h) => observer.observe(h));
  } else {
    tocContent.closest(".sidebar-card")?.remove();
  }
}
