let click = document.querySelector(".cros");

let warnng = document.querySelector(".warning_main");

click.addEventListener("click", () => {
  warnng.classList.add("hidden_message");
});
