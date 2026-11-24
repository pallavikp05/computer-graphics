# SkyFlight

**A 2D computer graphics animation built with Python and Pygame.** SkyFlight turns the synopsis into an interactive desktop experience: a hand-drawn passenger aircraft crosses a layered landscape while its propeller spins, clouds drift, and the scenery scrolls at different speeds.

> This is a visual learning model for 2D translation, rotation, parallax and frame-by-frame animation. It does not model aerodynamics.

## Features

- Gradient sky, glowing sun, drifting clouds, distant mountain silhouettes and scrolling ground
- Airplane assembled from polygons, ellipses, circles and lines; gentle bobbing and a spinning propeller
- Continuous wrap-around flight and multi-speed parallax
- Clickable pause, reset and speed buttons; keyboard shortcuts
- Resizable window with a consistent layout
- Fullscreen mode with `F11`
- No downloaded art assets: every scene element is drawn with Pygame primitives

## Run it

Requires Python 3.10+ and Pygame 2.5+.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

On macOS/Linux, activate with `source .venv/bin/activate`, then run the same install and launch commands with `python`.

## Controls

| Action | Control |
| --- | --- |
| Pause / resume | `Space` or the on-screen button |
| Increase / decrease speed | `↑` / `↓` or on-screen `+` / `−` |
| Reset flight | `R` or the on-screen button |
| Toggle fullscreen | `F11` |
| Quit | `Esc` or close the window |

Flight speed ranges from 0.2× to 3.0×. The window can be resized; the scene scales to fit.

## Project structure

```text
skyflight/
├── main.py           # scene, airplane, controls and animation loop
├── requirements.txt  # Pygame dependency
├── README.md         # setup and usage
└── .gitignore
```

## Graphics concepts demonstrated

- **Translation:** airplane and clouds change position over time.
- **Rotation:** propeller blades rotate around the nose hub.
- **Frame updates:** elapsed time and delta time keep movement smooth across frame rates.
- **Parallax:** cloud, mountain and ground layers move at different rates.
- **Compositing:** geometric primitives combine into a recognizable scene and aircraft.
- **Event-driven interaction:** keyboard and mouse events control the animation.

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10 or newer
- Pygame 2.5 or newer
- Any modern desktop computer (4 GB RAM recommended)

## License

MIT. See [LICENSE](LICENSE).
