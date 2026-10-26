# charts — Mozhi chart library

Render chart types as SVG/HTML markup from simple numeric data, written in
pure Mozhi.

## Install

```bash
mz add charts        # from the registry
mz add @crossberry-in/charts   # from git
```

## Use

```mozhi
import charts from "charts"
svg = charts.bar(["a", "b", "c"], [1.0, 2.0, 3.0])
echo(svg)
```

## Chart functions

`bar`, `hbar`, `line`, `area`, `donut`, `pie`, `scatter`, `histogram`,
`gauge`, `funnel`, `radar`, `lollipop`, `sparkline`, `page`.

## Example

`examples/demo.mz` writes a 14-chart HTML gallery to `/tmp/mozhi_charts.html`.
