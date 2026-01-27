# ShadugrMarinesTwo - CM-SS13-PVE Project Description

> **A comprehensive technical reference document for AI assistants and developers**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Directory Structure](#directory-structure)
4. [Core Systems](#core-systems)
5. [Game Mechanics](#game-mechanics)
6. [Development Workflow](#development-workflow)
7. [Code Standards & Best Practices](#code-standards--best-practices)
8. [Key Files Reference](#key-files-reference)
9. [Common Tasks](#common-tasks)

---

## Project Overview

### What Is This?

**CM-SS13-PVE** (Colonial Marines - Space Station 13 - Player Versus Environment) is a fork of [CM-SS13](https://github.com/cmss13-devs/cmss13), which itself is based on the multiplayer game [Space Station 13](https://spacestation13.com). The game is built using **BYOND** (Build Your Own Net Dream), a platform for creating and playing multiplayer online games.

### Core Concept

This is a **tactical roleplay-based players-versus-AI game** set in a sci-fi universe inspired by the Aliens franchise. The game features:

- **Colonial Marines (USCM)**: Human military forces with realistic military structure
- **Xenomorphs**: AI-controlled alien creatures (adapted from [cw-ss13](https://github.com/Watermelon914/cw-ss13))
- **Various factions**: PMCs, Yautja (Predators), colonists, and more

### Gameplay Loop

1. Marines deploy from their ship (typically the USS Almayer)
2. Ground operations on various planetary maps
3. Combat against AI-controlled xenomorph hives
4. Objective completion, survival, and extraction

---

## Technology Stack

### Primary Language: DM (Dream Maker)

- **Extension**: `.dm` files
- **Compiled Output**: `.dmb` (binary), `.rsc` (resources)
- **Paradigm**: Object-oriented, prototype-based inheritance

### Frontend UI: TGUI

- **Framework**: React-based
- **Location**: `/tgui/` directory
- **Documentation**: [tgui/README.md](tgui/README.md)
- **All new UIs must use TGUI** (NanoUI and HTML UIs are deprecated)

### Supporting Technologies

| Component | Technology |
|-----------|------------|
| UI Framework | TGUI (React/Preact) |
| Rust Extensions | `rust_g.dll`, `rustlibs.dll` |
| Database | SQL-based (BSQL) |
| Communication | Redis (pub/sub) |
| Build System | Node.js + Custom build scripts |
| Version Control | Git |

### Build Requirements

> **IMPORTANT**: The project cannot be compiled using BYOND alone!

Build using the provided build tool:
```bash
bin/build.cmd    # Windows
```

See [tools/build/README.md](tools/build/README.md) for complete build instructions.

---

## Directory Structure

```
ShadugrMarinesTwo/
├── bin/                    # Build scripts and server executables
├── cfg/                    # Server configuration (runtime)
├── code/                   # ★ MAIN SOURCE CODE
│   ├── __DEFINES/          # Global preprocessor definitions
│   ├── __HELPERS/          # Utility/helper procs
│   ├── _globalvars/        # Global variables
│   ├── _onclick/           # Click handling and HUD systems
│   ├── controllers/        # Subsystems and game controllers
│   │   ├── mc/             # Master controller
│   │   ├── subsystem/      # All game subsystems (SSxxx)
│   │   └── configuration/  # Configuration management
│   ├── datums/             # Non-atom data structures
│   │   ├── ammo/           # Ammunition types
│   │   ├── components/     # DCS components
│   │   ├── effects/        # Effect datums
│   │   ├── emergency_calls/# ERT definitions
│   │   ├── skills/         # Skill systems
│   │   └── ...
│   ├── defines/            # Additional defines
│   ├── game/               # Core game logic
│   │   ├── area/           # Area definitions
│   │   ├── gamemodes/      # Game mode logic (CM, extended, etc.)
│   │   ├── jobs/           # Job definitions
│   │   ├── machinery/      # Machine objects
│   │   ├── objects/        # Game objects
│   │   └── turfs/          # Floor/wall tiles
│   └── modules/            # ★ FEATURE MODULES
│       ├── cm_aliens/      # Xenomorph structures
│       ├── cm_marines/     # Marine equipment
│       ├── cm_preds/       # Yautja/Predator content
│       ├── cm_tech/        # Tech/research systems
│       ├── gear_presets/   # Loadout presets
│       ├── lighting/       # Lighting system
│       ├── mob/            # ★ CREATURE/CHARACTER CODE
│       │   ├── living/
│       │   │   ├── carbon/
│       │   │   │   ├── human/     # Human mobs
│       │   │   │   └── xenomorph/ # Xeno mobs
│       │   │   └── simple_animal/ # NPCs
│       │   └── dead/       # Ghost/observer code
│       ├── projectiles/    # Weapons and bullets
│       ├── reagents/       # Chemistry system
│       ├── shuttle/        # Shuttle systems
│       ├── surgery/        # Medical surgery
│       ├── tgui/           # TGUI integration
│       └── vehicles/       # Vehicle systems
├── config/                 # Default configuration files
├── html/                   # Static web assets
├── icons/                  # ★ SPRITE FILES (.dmi)
├── interface/              # BYOND interface definitions
├── maps/                   # ★ MAP FILES
│   ├── map_files/          # Actual .dmm map files
│   ├── Nightmare/          # Nightmare (procedural) inserts
│   ├── shuttles/           # Shuttle maps
│   └── *.json              # Map configuration files
├── modular/                # Modular/optional content packs
├── nano/                   # Legacy NanoUI (deprecated)
├── sound/                  # Audio files
├── strings/                # String data files (JSON/txt)
├── tgui/                   # ★ TGUI SOURCE (React)
│   ├── packages/tgui/     # Main TGUI package
│   └── docs/              # TGUI documentation
└── tools/                  # Development tools
```

---

## Core Systems

### Subsystem Architecture

The game uses a **Master Controller (MC)** pattern with dedicated subsystems. Each subsystem handles a specific domain and runs on its own schedule.

| Subsystem | File | Purpose |
|-----------|------|---------|
| `SSatoms` | `atoms.dm` | Atom initialization |
| `SSmobs` | `mob.dm` | Mob processing |
| `SShuman` | `human.dm` | Human-specific processing |
| `SSxeno` | `xeno.dm` | Xenomorph processing |
| `SSxeno_ai` | `xeno_ai.dm` | Xeno AI behavior |
| `SShuman_ai` | `human_ai.dm` | Human AI (NPCs) |
| `SSmachinery` | `machinery.dm` | Machine processing |
| `SSlighting` | `lighting.dm` | Dynamic lighting |
| `SSprojectiles` | `projectiles.dm` | Bullet/projectile handling |
| `SSticker` | `ticker.dm` | Round state management |
| `SSshuttle` | `shuttle.dm` | Shuttle movement |
| `SSpathfinding` | `pathfinding.dm` | A* pathfinding |
| `SSminimap` | `minimap.dm` | Minimap rendering |
| `SStgui` | `tgui.dm` | TGUI state management |
| `SSweather` | `weather.dm` | Weather effects |

### Component System (DCS)

Uses a **Datum Component System** for modular behavior attachment:

- Components in: `code/datums/components/`
- Signals defined in: `code/__DEFINES/dcs/signals/`
- Register signals with `RegisterSignal()`
- Send signals with `SEND_SIGNAL()`

### Lifecycle Hooks

```dm
// For atoms, prefer Initialize() over New()
/obj/item/example/Initialize(mapload, ...)
    . = ..()  // Always call parent
    // Your initialization code

// For cleanup
/obj/item/example/Destroy()
    // Cleanup code
    return ..()  // Always return parent
```

---

## Game Mechanics

### Mob Hierarchy

```
/mob
├── /mob/dead
│   └── /mob/dead/observer         # Ghosts
├── /mob/living
│   ├── /mob/living/carbon
│   │   ├── /mob/living/carbon/human
│   │   │   ├── /mob/living/carbon/human/species/*  # Species variants
│   │   │   └── ...
│   │   └── /mob/living/carbon/xenomorph
│   │       ├── /mob/living/carbon/xenomorph/larva
│   │       ├── /mob/living/carbon/xenomorph/runner
│   │       ├── /mob/living/carbon/xenomorph/drone
│   │       ├── /mob/living/carbon/xenomorph/warrior
│   │       ├── /mob/living/carbon/xenomorph/queen
│   │       └── ...
│   └── /mob/living/simple_animal  # NPCs
└── /mob/new_player                # Lobby state
```

### Factions System

Key factions defined in `code/datums/factions/`:

- **USCM** (United States Colonial Marines)
- **UPP** (Union of Progressive Peoples)
- **PMC** (Weyland-Yutani PMCs)
- **CLF** (Colonial Liberation Front)
- **Contractors**
- **CMB** (Colonial Marshals)

### Skills System

Skills defined in `code/datums/skills/`:

- Medical, Engineering, Construction
- Firearms, Heavy Weapons, Melee
- Leadership, Intel, Police
- And more...

### Equipment & Weapons

- Weapons: `code/modules/projectiles/`
- Ammo: `code/datums/ammo/`
- Gear presets: `code/modules/gear_presets/`
- Marine equipment: `code/modules/cm_marines/`

---

## Development Workflow

### Setting Up

1. Install [BYOND](https://www.byond.com/download/)
2. Clone the repository
3. Run `bin/build.cmd` to build the project

### Making Changes

1. Create a feature branch
2. Make your changes following code standards
3. Test locally
4. Submit a pull request with:
   - Description of changes
   - Testing performed
   - Changelog entry (if player-facing)

### Testing

```bash
# Run the game locally
bin/server.cmd

# Connect via BYOND Dream Seeker
# Default address: localhost:port
```

### TGUI Development

```bash
cd tgui
npm install
npm run dev     # Development with hot reload
npm run build   # Production build
```

---

## Code Standards & Best Practices

### General Rules

1. **Object-Oriented Design**: Use inheritance and override procs
2. **No Hacky Code**: Avoid specific hardcoded checks
3. **Use `Initialize()`**: Prefer over `New()` for atoms
4. **No Duplicate Code**: DRY principle
5. **Frame Independence**: Use `delta_time` in `process()` procs

### Signal Handlers

```dm
/type/path/proc/signal_callback()
    SIGNAL_HANDLER  // Required annotation
    // Code here - must not sleep!
    // Use INVOKE_ASYNC() for sleeping behavior
```

### Parent Calling

```dm
/obj/item/example/Initialize(mapload)
    . = ..()  // Call parent
    SHOULD_CALL_PARENT(TRUE)  // Lint enforcement
```

### Proc References (Callbacks)

```dm
// Same type or ancestor
RegisterSignal(x, COMSIG_FAKE, PROC_REF(my_proc))

// Different type
RegisterSignal(x, COMSIG_FAKE, TYPE_PROC_REF(/other/type, their_proc))

// Global proc
addtimer(CALLBACK(GLOBAL_PROC, GLOBAL_PROC_REF(global_function)), 100)
```

### Type Safety

```dm
// GOOD - Explicit type cast
var/obj/item/I = something
I.some_proc()

// BAD - Override type safety
something:some_proc()
```

### Loop Optimization

```dm
// Preferred - Faster DM syntax
for(var/i in 1 to some_value)

// For typed lists - Skip type check when safe
for(var/atom/A as anything in atom_list)
```

---

## Key Files Reference

### Entry Point
- `colonialmarines.dme` - Main project file (all includes)

### Core Definitions
- `code/__DEFINES/` - All preprocessor macros
- `code/_globalvars/` - Global variables
- `code/global.dm` - Core global definitions

### Game Modes
- `code/game/gamemodes/game_mode.dm` - Base game mode
- `code/game/gamemodes/cm_initialize.dm` - CM initialization
- `code/game/gamemodes/colonialmarines/` - CM-specific modes

### Player Code
- `code/modules/mob/living/carbon/human/` - Human players
- `code/modules/mob/living/carbon/xenomorph/` - Xeno players/AI

### Maps
- `maps/map_files/` - All .dmm map files
- `maps/*.json` - Map configurations
- `map_config/` - Map rotation settings

### Configuration
- `config/` - Default server config
- `cfg/` - Runtime configuration (gitignored)

---

## Common Tasks

### Adding a New Item

1. Create in appropriate `code/game/objects/` or `code/modules/` directory
2. Add icon to `icons/` (create .dmi sprite)
3. If vendor item, add to vendor lists
4. Test in-game

### Adding a New Weapon

1. Define gun in `code/modules/projectiles/guns/`
2. Define magazine in `code/modules/projectiles/magazines/`
3. Define ammo datum in `code/datums/ammo/`
4. Add sprites to `icons/obj/items/weapons/guns/`
5. Add to appropriate vendor/loadout

### Modifying Xenomorph Behavior

1. Xeno AI: `code/controllers/subsystem/xeno_ai.dm`
2. Xeno abilities: `code/modules/mob/living/carbon/xenomorph/abilities/`
3. Xeno castes: `code/modules/mob/living/carbon/xenomorph/castes/`

### Creating a TGUI Interface

1. Create React component in `tgui/packages/tgui/interfaces/`
2. Create backend datum in `code/modules/tgui/`
3. Follow [TGUI Tutorial](tgui/docs/tutorial-and-examples.md)

### Adding a New Map

1. Create .dmm in `maps/map_files/`
2. Create JSON config in `maps/`
3. Add Nightmare inserts in `maps/Nightmare/` if needed
4. Add to map rotation in `map_config/`

---

## Additional Resources

- **Wiki**: [https://cm-ss13.com/wiki](https://cm-ss13.com/wiki)
- **Code Documentation**: [https://docs.cm-ss13.com](https://docs.cm-ss13.com)
- **Contributing Guide**: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)
- **Code Standards**: [.github/guides/STANDARDS.md](.github/guides/STANDARDS.md)
- **Code Style**: [.github/guides/STYLES.md](.github/guides/STYLES.md)
- **TGUI Documentation**: [tgui/README.md](tgui/README.md)

---

## License

- **Code**: [AGPL v3](LICENSE-AGPLv3.txt)
- **Assets**: [CC BY-SA 3.0](LICENSE-CC-BY-NC-SA-3.0.txt)
- **Legacy Code**: [GPL v3](LICENSE-GPLv3.txt) (commits before Sept 2020)

---

*Document generated for AI/Developer reference. Last updated: January 2026*
