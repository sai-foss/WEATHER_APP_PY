import json

import reflex as rx

# the particles packed is being brought in via npm's CDN
PARTICLES_CDN = "https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"

PARTICLES_CONFIG = {
    "particles": {
        "number": {"value": 120, "density": {"enable": True, "value_area": 900}},
        "color": {"value": "#ffffff"},
        "shape": {"type": "circle"},
        "opacity": {"value": 0.5},
        "size": {"value": 2, "random": True},
        "line_linked": {
            "enable": True,
            "distance": 140,
            "color": "#ffffff",
            "opacity": 0.5,
            "width": 2,
        },
        "move": {"enable": True, "speed": 0.2},
    },
    "interactivity": {
        "events": {
            "onhover": {"enable": False},
            "onclick": {"enable": False},
            "resize": True,
        }
    },
    "retina_detect": True,
}


# render the particles
#
def particles_background() -> rx.Component:
    cfg = json.dumps(PARTICLES_CONFIG)

    return rx.fragment(
        rx.box(
            id="particles-js",
            position="fixed",
            top="0",
            right="0",
            bottom="0",
            left="0",
            z_index="-1",
            pointer_events="none",
        ),
        rx.script(src=PARTICLES_CDN),
        rx.script(
            f"""
(function initParticles() {{
  const cfg = {cfg};
  function start() {{
    const el = document.getElementById("particles-js");
    if (!el || !window.particlesJS) return false;
    if (el.getAttribute("data-initialized") === "1") return true;
    window.particlesJS("particles-js", cfg);
    el.setAttribute("data-initialized", "1");
    return true;
  }}
  if (start()) return;
  let tries = 0;
  const t = setInterval(() => {{
    if (start() || ++tries > 50) clearInterval(t);
  }}, 100);
}})();
"""
        ),
    )
