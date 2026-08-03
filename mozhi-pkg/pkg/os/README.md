# os

Full operating system control library for Mozhi. Cross-platform: Linux, Windows, macOS, Android/Termux.

## Install

```bash
pkg install os
```

## Quick Start

```mozhi
import mod from "os"

# System info
echo(mod.system_info())

# Process management
echo(mod.proc_list())
mod.proc_kill(1234)

# Filesystem
mod.fs_mkdir("mydir")
mod.fs_copy("a.txt", "b.txt")
echo(mod.fs_walk("."))

# Network
echo(mod.net_primary_ip())
echo(mod.net_ping("google.com", "1"))
echo(mod.net_port_scan("localhost"))

# Power
echo(mod.power_battery_status())
# mod.power_shutdown()  # ⚠ actually shuts down!

# Package manager
echo(mod.pkg_detect())  # "apt", "dnf", "pacman", "brew", "winget"
mod.pkg_install("htop")
mod.pkg_update()

# Services
echo(mod.svc_list())
mod.svc_restart("nginx")

# Cron
mod.cron_daily_at(2, 0, "backup.sh")
```

## 9 Modules, 100+ Functions

### system.mz — System Information
| Function | Description |
|----------|-------------|
| `os_type()` | "linux", "windows", "macos", "android" |
| `os_version()` | Kernel version |
| `distro()` | Linux distribution name |
| `hostname()` | System hostname |
| `arch()` | CPU architecture |
| `cpu_count()` | Number of CPU cores |
| `cpu_model()` | CPU model name |
| `uptime_formatted()` | Uptime as "Xd Xh Xm" |
| `total_memory_mb()` | Total RAM in MB |
| `free_memory_mb()` | Available RAM in MB |
| `disk_usage(path)` | Disk usage for path |
| `get_env(name)` | Environment variable |
| `system_info()` | Full system summary |
| `is_linux()` / `is_windows()` / `is_macos()` / `is_android()` | OS checks |

### process.mz — Process Management
| Function | Description |
|----------|-------------|
| `list()` | List all processes |
| `pid_of(name)` | Get PID by name |
| `is_running(name)` | Check if process is running |
| `kill(pid)` | Kill by PID |
| `kill_force(pid)` | SIGKILL |
| `kill_all(name)` | Kill all by name |
| `spawn(cmd)` | Background process |
| `exec(cmd)` | Run and wait |
| `top_cpu(n)` | Top N by CPU |
| `top_memory(n)` | Top N by memory |
| `children(pid)` | Child processes |
| `kill_tree(pid)` | Kill process tree |

### filesystem.mz — File Operations
| Function | Description |
|----------|-------------|
| `mkdir(path)` | Create directory (recursive) |
| `copy(src, dst)` | Copy file |
| `copy_dir(src, dst)` | Copy directory |
| `move(src, dst)` | Move/rename |
| `delete(path)` | Delete file |
| `rmdir(path)` | Remove directory |
| `walk(path)` | List all files recursively |
| `list_files(path)` | Files only |
| `list_dirs(path)` | Directories only |
| `file_size(path)` | Size in bytes |
| `chmod(path, mode)` | Change permissions |
| `is_dir(path)` / `is_file(path)` | Type checks |
| `find(path, pattern)` | Find by name |
| `dir_size(path)` | Directory size |
| `disk_usage_all()` | All filesystems |
| `abs_path(path)` | Absolute path |
| `symlink(target, name)` | Create symlink |

### network.mz — Network Operations
| Function | Description |
|----------|-------------|
| `interfaces()` | All network interfaces |
| `primary_ip()` | First non-loopback IP |
| `mac_address(iface)` | MAC address |
| `gateway()` | Default gateway |
| `dns_servers()` | DNS server list |
| `ping(host, count)` | Ping check (true/false) |
| `port_open(host, port)` | Port check |
| `port_scan(host)` | Scan common ports |
| `listening_ports()` | List listening ports |
| `connections()` | All connections |
| `download(url, output)` | Download file |

### user.mz — User Management
| Function | Description |
|----------|-------------|
| `current()` | Current username |
| `home()` | Home directory |
| `shell()` | Current shell |
| `is_root()` | Check root/admin |
| `groups()` | User groups |
| `list_users()` | All users |
| `logged_in()` | Logged-in users |
| `add_user(name)` | Create user (root) |
| `delete_user(name)` | Remove user (root) |

### power.mz — Power Management
| Function | Description |
|----------|-------------|
| `shutdown()` | Power off |
| `reboot()` | Restart |
| `sleep()` | Suspend |
| `hibernate()` | Hibernate |
| `lock_screen()` | Lock screen |
| `battery_status()` | Battery info |
| `battery_percent()` | Battery percentage |
| `on_ac_power()` | AC adapter check |
| `get_brightness()` | Screen brightness |
| `set_brightness(pct)` | Set brightness |

### package_manager.mz — Package Management
| Function | Description |
|----------|-------------|
| `detect()` | Auto-detect: apt/dnf/pacman/brew/winget/choco/pkg |
| `install(pkg)` | Install package |
| `remove(pkg)` | Remove package |
| `update()` | Update all packages |
| `search(query)` | Search packages |
| `list_installed()` | List installed |
| `is_installed(pkg)` | Check installed |
| `autoremove()` | Clean unused |

### service.mz — Service Management
| Function | Description |
|----------|-------------|
| `list_all()` | All services |
| `list_running()` | Running services |
| `start(name)` | Start service |
| `stop(name)` | Stop service |
| `restart(name)` | Restart service |
| `enable(name)` | Enable at boot |
| `disable(name)` | Disable at boot |
| `status(name)` | Service status |
| `logs(name, n)` | Recent logs |

### cron.mz — Scheduled Tasks
| Function | Description |
|----------|-------------|
| `cron_list()` | List crontab |
| `cron_add(schedule, cmd)` | Add cron job |
| `cron_clear()` | Remove all |
| `every_minutes(n, cmd)` | Run every N minutes |
| `daily_at(h, m, cmd)` | Run daily |
| `weekly_on(day, h, m, cmd)` | Run weekly |
| `on_boot(cmd)` | Run at boot |
| `at(cmd, time)` | One-time schedule |

## Cross-Platform Support

| Feature | Linux | Windows | macOS | Android |
|---------|-------|---------|-------|---------|
| System info | ✓ | ✓ | ✓ | ✓ |
| Process mgmt | ✓ | ✓ | ✓ | ✓ |
| Filesystem | ✓ | ✓ | ✓ | ✓ |
| Network | ✓ | ✓ | ✓ | ✓ |
| User mgmt | ✓ | ✓ | ✓ | partial |
| Power | ✓ | ✓ | ✓ | partial |
| Package mgr | apt/dnf/pacman | winget/choco | brew | pkg |
| Services | systemd | sc | launchd | rc |
| Cron | crontab | schtasks | crontab | crontab |

## License

MIT
