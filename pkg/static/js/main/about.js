// START OF FILE about.js

"use strict";

document.addEventListener("DOMContentLoaded", () => {
  /**
   * Scroll Reveal Animation
   *
   * This uses the Intersection Observer API to add a 'visible' class
   * to elements when they enter the viewport.
   */
  const revealElements = document.querySelectorAll(".reveal");

  const observerOptions = {
    root: null, // observes intersections relative to the viewport
    rootMargin: "0px",
    threshold: 0.1, // trigger when 10% of the element is visible
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        // Optional: Stop observing the element once it's visible
        // to prevent re-triggering the animation.
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Attach the observer to each reveal element
  revealElements.forEach((el) => {
    observer.observe(el);
  });
});
