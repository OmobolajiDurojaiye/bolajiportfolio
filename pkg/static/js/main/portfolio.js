"use strict";

document.addEventListener("DOMContentLoaded", () => {
  /**
   * Hover-to-play video functionality for the new portfolio design
   */
  const projectItems = document.querySelectorAll(".project-item");

  projectItems.forEach((item) => {
    const video = item.querySelector(".project-video");
    if (video) {
      item.addEventListener("mouseenter", () => {
        // .play() returns a promise. We catch potential errors if
        // the user moves the mouse away before playback starts.
        const playPromise = video.play();
        if (playPromise !== undefined) {
          playPromise.catch(() => {
            // Playback was interrupted. We can ignore this.
          });
        }
      });

      item.addEventListener("mouseleave", () => {
        video.pause();
        video.currentTime = 0; // Rewind video to the start
      });
    }
  });
});
