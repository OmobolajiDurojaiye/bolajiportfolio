"use strict";

document.addEventListener("DOMContentLoaded", () => {
  /**
   * Mobile Navigation Toggle
   */
  const hamburgerMenu = document.querySelector(".hamburger-menu");
  const mobileNav = document.querySelector(".mobile-nav-menu");
  const navLinks = document.querySelectorAll(".mobile-nav-links a");

  if (hamburgerMenu && mobileNav) {
    hamburgerMenu.addEventListener("click", () => {
      mobileNav.classList.toggle("active");
    });
  }

  // Close menu when a link is clicked
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      mobileNav.classList.remove("active");
    });
  });

  /**
   * Global Scroll Reveal Animation
   *
   * This uses the Intersection Observer API to add a 'visible' class
   * to elements with the `.reveal` class when they enter the viewport.
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
        // Stop observing the element once it's visible to save resources
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Attach the observer to each reveal element
  revealElements.forEach((el) => {
    observer.observe(el);
  });
});
