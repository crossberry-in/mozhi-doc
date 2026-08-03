# gravity_simulation

N-body physics simulation library for Mozhi. Simulate gravity, springs, electrostatics, and collisions with velocity-Verlet integration. Render to SVG, HTML canvas, or export as JSON.

Inspired by [gravity-simulation on PyPI](https://pypi.org/project/gravity-simulation/).

## Install

```bash
pkg install gravity_simulation
```

## Quick Start

```mozhi
import mod from "gravity_simulation"
import presets from "gravity_simulation/src/presets.mz"
import renderer from "gravity_simulation/src/renderer.mz"

# Load the solar system preset
w = presets.solar_system()

# Run simulation for 100 steps
w = mod.run_steps(w, 100)

# Render to HTML and save
html = renderer.render_html(presets.solar_system(), 200)
write_file("simulation.html", html)
echo("Open simulation.html in your browser!")
```

## Features

- **N-body gravity** — Newton's law of universal gravitation
- **Spring forces** — Hooke's law for pendulums and elastic constraints
- **Electrostatic** — Coulomb force between charged particles
- **Collisions** — Elastic collision detection and response
- **Boundary** — Walls with energy-damping bounce
- **Verlet integration** — Velocity-Verlet for energy stability
- **Energy tracking** — Kinetic, potential, and total energy
- **Rendering** — SVG, HTML canvas animation, ASCII, JSON export

## API

### Core (`mod.mz`)

| Function | Description |
|----------|-------------|
| `body(name, x, y, vx, vy, mass, radius)` | Create a body |
| `world(bodies, dt, g, w, h, forces)` | Create a simulation world |
| `step(w)` | Advance simulation by one timestep |
| `run_steps(w, n)` | Run n steps |
| `kinetic_energy(w)` | Total KE of all bodies |
| `potential_energy(w)` | Total gravitational PE |
| `total_energy(w)` | KE + PE (conserved) |
| `simulate_trajectory(w, n)` | Run n steps, return all positions |

### Presets (`presets.mz`)

| Function | Description |
|----------|-------------|
| `solar_system()` | Sun + 4 planets |
| `binary_stars()` | Two stars + planet |
| `pendulum()` | Simple pendulum |
| `double_pendulum()` | Chaotic double pendulum |
| `three_body()` | Classic three-body problem |
| `bouncing_balls()` | Collision demo |
| `electrostatic_charges()` | Repelling charges |
| `projectile()` | Projectile motion |

### Renderer (`renderer.mz`)

| Function | Description |
|----------|-------------|
| `render_svg(w)` | Single SVG frame |
| `render_html(w, steps)` | Full HTML with canvas animation |
| `render_ascii(w)` | Text-based visualization |
| `export_json(w, steps)` | JSON trajectory data |

## Examples

### Solar System

```mozhi
import presets from "gravity_simulation/src/presets.mz"
import renderer from "gravity_simulation/src/renderer.mz"

html = renderer.render_html(presets.solar_system(), 300)
write_file("solar_system.html", html)
```

### Three-Body Problem

```mozhi
import presets from "gravity_simulation/src/presets.mz"
import renderer from "renderer.mz"

html = renderer.render_html(presets.three_body(), 500)
write_file("three_body.html", html)
```

### Custom Simulation

```mozhi
import mod from "gravity_simulation"

# Create bodies
bodies = []
bodies.push(mod.body("Star", 400.0, 300.0, 0.0, 0.0, 10000.0, 20.0))
bodies.push(mod.body("Planet", 500.0, 300.0, 0.0, 40.0, 5.0, 8.0))

# Create world: bodies, dt=0.05, G=50, 800x600, gravity
w = mod.world(bodies, 0.05, 50.0, 800.0, 600.0, "gravity")

# Run 200 steps
w = mod.run_steps(w, 200)

# Check energy
echo("KE: " + string(mod.kinetic_energy(w)))
echo("PE: " + string(mod.potential_energy(w)))
echo("Total: " + string(mod.total_energy(w)))
```

## Physics

### Forces

- **Gravity**: `F = G·m₁·m₂/r²`
- **Spring**: `F = -k·(r - r₀)`
- **Electrostatic**: `F = k·q₁·q₂/r²`

### Integration

Velocity-Verlet method:
1. Compute acceleration `a(t)`
2. Update position: `x(t+dt) = x + v·dt + ½·a·dt²`
3. Compute new acceleration `a(t+dt)`
4. Update velocity: `v(t+dt) = v + ½·(a + a_new)·dt`

This conserves energy better than simple Euler integration.

## License

MIT
