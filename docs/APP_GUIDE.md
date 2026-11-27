# Mozhi App Guide

Mozhi includes an app-package workflow for creating, building, installing, and launching app packages. The commands below show the project lifecycle.

## Create an app project

```bash
mz app new counter --id in.crossberry.counter --label Counter
```

This creates an app project named `counter` with the application identifier `in.crossberry.counter` and display label `Counter`.

## Build the app package

```bash
mz app build counter
```

The build produces an installable package in the app project's output directory. For example, the following command installs a package built at `counter/dist/counter-0.1.0.pkg`:

```bash
mz app install counter/dist/counter-0.1.0.pkg
```

## Open and manage installed apps

```bash
mz app open in.crossberry.counter
mz app home
```

- `mz app open <id>` opens the installed app using its application identifier.
- `mz app home` opens the app home/launcher view.
- `mz app install <package>` installs a previously built app package.

## Complete example

```bash
mz app new counter --id in.crossberry.counter --label Counter
mz app build counter
mz app install counter/dist/counter-0.1.0.pkg
mz app open in.crossberry.counter
mz app home
```

The package filename and version in the install command should match the artifact actually produced by your build. This guide documents the CLI workflow; app runtime capabilities and platform-specific requirements depend on the installed Mozhi release.

## Related guides

- [Installation Guide](../INSTALL.md)
- [Native Build Guide](BUILD.md)
- [Package Guide](packages.md)
