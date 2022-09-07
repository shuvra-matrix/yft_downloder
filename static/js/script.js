let click = document.querySelector(".cros");

let warnng = document.querySelector(".warning_main");

let bodys = document.querySelector("body");

click.addEventListener("click", () => {
  warnng.classList.add("hidden_message");
  bodys.classList.remove("grddient");
});
