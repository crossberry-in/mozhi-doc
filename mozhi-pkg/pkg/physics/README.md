# Mozhi Physics Library

A production-ready physics library for the Mozhi programming language. Implements mechanics, motion, energy, gravity, fluids, thermodynamics, electricity, magnetism, waves, optics, relativity, quantum mechanics, astronomy, and unit conversions.

## Installation

Libraries auto-download on first use. Just import and run:

```mozhi
import constants from "physics/constants.mz"
import mechanics from "physics/mechanics.mz"

echo(mechanics.force(10, 5))  # 50 N
```

## Quick Start

```bash
# Run the examples
cd pkg/physics
mozhi-interpreter examples.mz
```

## Modules

| Module | Description | Functions |
|--------|-------------|-----------|
| [`constants`](constants.mz) | Physical constants (SI) | 14 core + 16 extended |
| [`mechanics`](mechanics.mz) | Force, weight, momentum, torque, pressure, density | 9 |
| [`motion`](motion.mz) | Velocity, acceleration, displacement, distance | 8 |
| [`energy`](energy.mz) | Work, power, kinetic/potential/spring energy | 8 |
| [`gravity`](gravity.mz) | Gravitational force, escape/orbital velocity | 6 |
| [`fluids`](fluids.mz) | Buoyancy, Bernoulli, viscosity, surface tension | 10 |
| [`thermodynamics`](thermodynamics.mz) | Heat, ideal gas, efficiency, radiation | 14 |
| [`electricity`](electricity.mz) | Ohm's law, power, capacitance, Coulomb | 12 |
| [`magnetism`](magnetism.mz) | Magnetic force, flux, Faraday, solenoid | 10 |
| [`waves`](waves.mz) | Frequency, wavelength, Doppler, SHM | 12 |
| [`optics`](optics.mz) | Refraction, focal length, magnification, diffraction | 11 |
| [`relativity`](relativity.mz) | E=mc², time dilation, length contraction | 9 |
| [`quantum`](quantum.mz) | Photon energy, de Broglie, Bohr, uncertainty | 11 |
| [`astronomy`](astronomy.mz) | Orbital period, luminosity, Schwarzschild radius | 10 |
| [`units`](units.mz) | 60+ unit constants + 80+ conversions | 80+ |
| [`errors`](errors.mz) | Error handling helpers | 8 |

**Total: 15 modules, 230+ functions, 30+ constants**

## Usage

### Physical Constants

```mozhi
import constants from "physics/constants.mz"

echo(constants.SPEED_OF_LIGHT)        # 299792458 m/s
echo(constants.GRAVITATIONAL_CONSTANT) # 6.67430e-11
echo(constants.PLANCK_CONSTANT)       # 6.62607e-34 J·s
echo(constants.STANDARD_GRAVITY)      # 9.80665 m/s²
```

### Mechanics

```mozhi
import mechanics from "physics/mechanics.mz"

echo(mechanics.force(10, 5))          # F = ma → 50 N
echo(mechanics.weight(70))            # W = mg → 686.47 N
echo(mechanics.momentum(2, 8))        # p = mv → 16 kg·m/s
echo(mechanics.torque(0.5, 20, 90))   # τ = rFsinθ → 10 N·m
echo(mechanics.pressure(100, 2))      # P = F/A → 50 Pa
echo(mechanics.density(5, 0.002))     # ρ = m/V → 2500 kg/m³
```

### Motion

```mozhi
import motion from "physics/motion.mz"

echo(motion.velocity(100, 5))         # v = Δx/Δt → 20 m/s
echo(motion.acceleration(30, 5))      # a = Δv/Δt → 6 m/s²
echo(motion.displacement(0, 2, 5))    # s = ut + ½at² → 25 m
echo(motion.free_fall_distance(9.81, 3)) # h = ½gt² → 44.145 m
```

### Energy

```mozhi
import energy from "physics/energy.mz"

echo(energy.kineticEnergy(2, 8))      # KE = ½mv² → 64 J
echo(energy.potentialEnergy(5, 10, 9.81)) # PE = mgh → 490.5 J
echo(energy.springEnergy(200, 0.1))   # PE = ½kx² → 1 J
echo(energy.power(1000, 10))          # P = W/t → 100 W
```

### Gravity

```mozhi
import gravity from "physics/gravity.mz"

# Earth-Moon gravitational force
echo(gravity.gravitationalForce(5.972e24, 7.348e22, 3.844e8)) # ≈ 1.98e20 N

# Earth escape velocity
echo(gravity.escapeVelocity(5.972e24, 6371000)) # ≈ 11186 m/s

# Orbital velocity at Earth surface
echo(gravity.orbitalVelocity(5.972e24, 6371000)) # ≈ 7907 m/s
```

### Electricity

```mozhi
import electricity from "physics/electricity.mz"

echo(electricity.voltage(2, 10))      # V = IR → 20 V
echo(electricity.current(12, 4))      # I = V/R → 3 A
echo(electricity.resistance(12, 2))   # R = V/I → 6 Ω
echo(electricity.power(12, 2))        # P = VI → 24 W
echo(electricity.capacitance(0.01, 5)) # C = Q/V → 0.002 F
echo(electricity.electricField(1e-9, 0.1)) # E = kQ/r² → 898.76 N/C
```

### Magnetism

```mozhi
import magnetism from "physics/magnetism.mz"

echo(magnetism.magneticForce(0.5, 10, 0.2, 90)) # F = BILsinθ → 1 N
echo(magnetism.magneticFlux(0.5, 0.1, 0))       # Φ = BAcosθ → 0.05 Wb
echo(magnetism.field_from_wire(10, 0.1))         # B = μ₀I/(2πr) → 2e-5 T
```

### Waves

```mozhi
import waves from "physics/waves.mz"

echo(waves.frequency(340, 2))         # f = v/λ → 170 Hz
echo(waves.wavelength(340, 170))      # λ = v/f → 2 m
echo(waves.period(50))                # T = 1/f → 0.02 s
echo(waves.speed_of_sound(20))        # v ≈ 331 + 0.6T → 343 m/s
echo(waves.pendulum_period(1, 9.81))  # T = 2π√(L/g) → 2.006 s
```

### Optics

```mozhi
import optics from "physics/optics.mz"

echo(optics.refractiveIndex(2e8))         # n = c/v → 1.499
echo(optics.focalLength(1.5, 0.5, -0.5))  # 1/f = (n-1)(1/R₁-1/R₂) → 2 m
echo(optics.magnification(0.1, 0.2))      # m = -di/do → -0.5
echo(optics.lens_power(0.5))              # P = 1/f → 2 D
```

### Thermodynamics

```mozhi
import thermodynamics from "physics/thermodynamics.mz"

echo(thermodynamics.heat(2, 4184, 10))    # Q = mcΔT → 83680 J
echo(thermodynamics.idealGasLaw(101325, 0.0224, 1)) # PV=nRT → 273.15 K
echo(thermodynamics.carnot_efficiency(600, 300))    # η = 1-Tc/Th → 0.5
echo(thermodynamics.celsius_to_kelvin(25))          # → 298.15 K
```

### Relativity

```mozhi
import relativity from "physics/relativity.mz"

echo(relativity.massEnergy(1))            # E = mc² → 8.99e16 J
echo(relativity.timeDilation(1, 2.5e8))   # t' = γt → 1.81 s
echo(relativity.lengthContraction(10, 2.5e8)) # L' = L/γ → 5.52 m
```

### Quantum

```mozhi
import quantum from "physics/quantum.mz"

echo(quantum.photonEnergy(5e14))          # E = hf → 3.31e-19 J
echo(quantum.deBroglieWavelength(9.1e-31, 1e6)) # λ = h/mv → 7.28e-10 m
echo(quantum.hydrogen_energy_level(1))    # E₁ = -13.6 eV → -2.18e-18 J
echo(quantum.wien_wavelength(5778))       # λ_max = b/T → 5.01e-7 m
```

### Astronomy

```mozhi
import astronomy from "physics/astronomy.mz"

# Earth orbital period (1 year)
echo(astronomy.orbitalPeriod(1.989e30, 1.496e11)) # ≈ 3.156e7 s

# Sun luminosity
echo(astronomy.luminosity(6.96e8, 5778)) # ≈ 3.85e26 W

# Solar mass from luminosity
echo(astronomy.stellarMass(3.828e26))    # ≈ 1.99e30 kg

# Schwarzschild radius of Earth
echo(astronomy.schwarzschild_radius(5.972e24)) # ≈ 8.87e-3 m
```

### Units

```mozhi
import units from "physics/units.mz"

echo(units.km_to_m(5))        # → 5000 m
echo(units.h_to_s(1)          # → 3600 s
echo(units.mph_to_ms(60))     # → 26.82 m/s
echo(units.c_to_k(25))        # → 298.15 K
echo(units.c_to_f(25))        # → 77 °F
echo(units.ev_to_j(1))        # → 1.602e-19 J
echo(units.pa_to_atm(101325)) # → 1.0 atm
echo(units.lb_to_kg(150))     # → 68.04 kg
echo(units.format_si(1500000)) # → "1.5 G"
```

## SI Units

All functions use SI units throughout:

| Quantity | Unit | Symbol |
|----------|------|--------|
| Length | meter | m |
| Mass | kilogram | kg |
| Time | second | s |
| Temperature | kelvin | K |
| Current | ampere | A |
| Force | newton | N |
| Energy | joule | J |
| Power | watt | W |
| Pressure | pascal | Pa |
| Charge | coulomb | C |
| Voltage | volt | V |
| Resistance | ohm | Ω |
| Capacitance | farad | F |
| Magnetic field | tesla | T |
| Magnetic flux | weber | Wb |
| Frequency | hertz | Hz |

## Error Handling

Functions validate inputs and return descriptive error strings:

```mozhi
import mechanics from "physics/mechanics.mz"

# Division by zero
echo(mechanics.pressure(100, 0))  # "[physics] 'area' must be non-zero"

# Negative mass
echo(mechanics.force(-10, 5))     # "[physics] 'mass' must be non-negative"
```

## Performance

- Pure Mozhi — no external dependencies (except `mozhi-math-utils` for optional sqrt)
- All computations use simple arithmetic (+, -, ×, ÷)
- Newton-Raphson for sqrt, arcsin, cube root
- Taylor series for ln, exp, log10
- Minimal memory allocation

## Testing

Run the examples to verify all functions work:

```bash
mozhi-interpreter examples.mz
```

## License

MIT

## See Also

- [Mozhi Documentation](https://crossberry-in.github.io/mozhi-doc/)
- [Mozhi Libraries](https://crossberry-in.github.io/mozhi-doc/libs.html)
- [Math Library](https://github.com/crossberry-in/mozhi-doc/tree/main/libs/math_utils)
