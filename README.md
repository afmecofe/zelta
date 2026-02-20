# Zelta Embedded SDK

This is the embedded SDK for Zelta, containing firmware and embedded system components for IoT devices.

## Repository Information

This repository is a submodule of the main [Zelta](https://github.com/didavie/Zelta) project.

## Technology Stack

- **RTOS**: Zephyr RTOS
- **Build System**: CMake
- **Hardware Support**: ESP32, nRF52, STM32, and other platforms

## Getting Started

For development instructions, see the main Zelta repository documentation.

## Submodule Usage

This repository should be cloned as part of the main Zelta workspace:

```bash
git clone --recursive https://github.com/didavie/Zelta.git
```

Or if you've already cloned the parent repository:

```bash
cd Zelta
git submodule update --init --recursive
```

## License

See the main Zelta repository for license information.
