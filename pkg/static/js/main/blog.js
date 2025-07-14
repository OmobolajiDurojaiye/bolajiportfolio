"use strict";

document.addEventListener("DOMContentLoaded", () => {
  /**
   * Blog Category Filtering
   */
  const filterPills = document.querySelectorAll(".filter-pill");
  const blogCards = document.querySelectorAll(".blog-card");

  if (filterPills.length > 0 && blogCards.length > 0) {
    filterPills.forEach((pill) => {
      pill.addEventListener("click", () => {
        // Update active pill state
        filterPills.forEach((p) => p.classList.remove("active"));
        pill.classList.add("active");

        const filter = pill.getAttribute("data-filter");

        // Filter cards
        blogCards.forEach((card) => {
          const cardCategory = card.getAttribute("data-category");
          if (filter === "all" || cardCategory === filter) {
            card.style.display = "flex";
            // A simple fade-in effect
            setTimeout(() => (card.style.opacity = 1), 50);
          } else {
            card.style.opacity = 0;
            // Hide after transition
            setTimeout(() => (card.style.display = "none"), 300);
          }
        });
      });
    });
  }
});
