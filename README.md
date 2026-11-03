# HAL Red Eye for Jibo

An original **HAL-inspired** cinematic red-lens eye for Jibo robots using the 5x1 BEam/BEacon theme system. Deep-red optical glass, metallic concentric rings, a red listening iris, a matching closed-eye texture, and original crimson replacements for common happy and expression-animation textures. Developed by **[Matt87c](https://github.com/Matt87c)**.

> **Status: v1.0.1 stable GitHub release requested by the maintainer; the new expression override still awaits real Jibo retesting on BEam v3.1.8.** Automated validation is not proof of live robot compatibility or store approval. Community project; not associated with the movie creators or the Jibo/5x1 maintainers.

- Theme title: **HAL Red Eye**
- Package version: **1.0.1**
- Minimum jibo-tbd: **3.1.8** (conservative target for the updated build)
- Eye size: **125%** of stock, subject to on-device visual acceptance
- Developer: **Matt87c**
- Type: visual-only declarative BEacon theme (no executables or credentials)

## Installation

1. Back up your currently working theme and confirm your Jibo finished the BEam v3.1.8 update.
2. In BEacon open **Store → Themes → ⋯ → Upload ZIP** and select `jibo-hal-eye-theme.zip` from `dist/`.
3. Select **HAL Red Eye → Apply**. Installation itself does not activate the theme.
4. To restore stock appearance, select **None**, or apply the last known-good theme.

Do **not** upload the GitHub source ZIP; choose the built package from the release or `dist/` folder.

## Theme-wide visual consistency

The v1.0.1 **expression-coverage fix** adds six optional 5x1 animation-texture overrides in `atex/`. It responds to a physical-device report of a brief **stock-white half-moon eye during a fun fact/excitement animation**. The BEam animation database uses `happy-glow-01.png` as an overlay for `eye_happy_in_00`, `eye_happy_out_00`, and `eye_happy_pose_01`; `eye_shape_03.png` is also used in a native laughing-eye animation. These overrides supply original HAL-red textures **without changing animation timing or native eye movement**.

| Animation override | Intent |
| --- | --- |
| `atex/happy-glow-01.png` | Replaces the native white happy/excitement glow with a crimson halo |
| `atex/eye_shape_03.png` | HAL-red smiling/crescent eye |
| `atex/eye_shape_04.png` | HAL-red squint |
| `atex/eye_shape_05.png` | HAL-red arched expression |
| `atex/eye_shape_06.png` | HAL-red narrow slit |
| `atex/eye_shape_08.png` | HAL-red intensified lens |

These are **theme-only, stock-filename-matched overrides** supported by 5x1's `atex/` mechanism; no 5x1 system files are overwritten. An animation asset used by a different skill, or a texture not covered here, may still have its original appearance. **Do not promise every Jibo animation is HAL-colored without full hardware coverage and/or broader 5x1 runtime support.** See [Animation coverage](docs/ANIMATION_COVERAGE.md).

## Native eye behaviors

| Supported theme asset | Role |
| --- | --- |
| `face/eye.png` | Red open/idle eye with native gaze and face geometry |
| `face/eyeListening.png` | Brighter, distinct red listening eye; preserve original color during native listening |
| `face/eyeClosed.png` | Red slit/blink image, blended and compressed by native blink/pet/sleep motion |
| `face/face.json` | Black background, 125% eye scale |
| `manifest.json` | Theme compatibility/version |
| `banner.png` | BEacon Store preview |

**Speaking and thinking:** BEam v3.1.8 does not expose `eyeSpeaking.png` or `eyeThinking.png` as theme face assets. Native expression animations remain responsible for those states. `preview/states/speaking.png` documents the approved visual concept but is **not applied** as a live speaking texture by this theme. Do not claim standalone custom speaking/thinking animations in store listings without a separately implemented, tested runtime change.

## Build and validate

Python 3.9+ and Pillow 11.3.0 are needed for image source regeneration. `scripts/build_release.py` and `scripts/validate_release.py` use the Python standard library plus Pillow to check PNGs.

```bash
python -m pip install Pillow==11.3.0
python scripts/generate_theme_art.py  # Optional: regenerate from the approved concept
python scripts/generate_expression_art.py  # Build the red expression overrides
python scripts/build_release.py
python scripts/validate_release.py
```

A deterministic ZIP contains the seven original theme files and six optional supported animation-texture overrides. Checks cover manifest shape, RGBA images, red-only effects, native-listening artwork difference, ZIP path safety, CRC, reproducibility and file sizes. Before claiming full on-device acceptance, complete `docs/HARDWARE_TEST.md` on the exact ZIP and record its SHA-256. A non-prerelease GitHub release does not by itself certify animation coverage.

## Distribution

Public repository: `https://github.com/Matt87c/jibo-hal-eye-theme`. Attach `dist/jibo-hal-eye-theme.zip` to the tagged GitHub release. 5x1's current store behavior requires a **stable GitHub release** for catalog indexing; merely pushing a main branch is insufficient. Store publication is controlled by the store maintainers.

## License

See [LICENSE](LICENSE). The repository contains original generated artwork and hand-authored layout/build tooling, not ripped movie frames or 5x1/Jibo runtime binaries. The HAL-inspired theme name references a fictional AI aesthetic; no affiliation is asserted.
