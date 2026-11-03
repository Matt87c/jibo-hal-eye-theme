# HAL Red Eye v1.0.1

Stable GitHub release of the original HAL-inspired red optical eye theme for 5x1/BEacon on Jibo, built for jibo-tbd 3.1.8 and later.

## Changes

- Preserve the original tested HAL idle, red listening, and red blink/closed face textures.
- Add six crimson animation overrides: `happy-glow-01.png`, `eye_shape_03.png`, `eye_shape_04.png`, `eye_shape_05.png`, `eye_shape_06.png`, and `eye_shape_08.png`.
- Address the reported stock-white crescent/happy expression that appeared briefly during a fun fact.
- Keep native Jibo movement, speech, animation timing and firmware unchanged.

## Validation and known limits

Static archive, PNG, manifest, reproducibility and asset validation: **PASS**.
The original HAL theme was visually tested on physical Jibo. The new v1.0.1 expression overrides have **not yet been retested on physical hardware**; the reported white-crescent issue is not yet confirmed resolved. Theme overrides do not guarantee every stock or skill-specific animation texture is replaced. See `docs/HARDWARE_TEST.md` and `docs/ANIMATION_COVERAGE.md`.

**Install:** Download the attached `jibo-hal-eye-theme.zip`; in BEacon use Store > Upload ZIP, then Apply HAL Red Eye. No firmware reset or 5x1 reinstall is needed. Selecting None restores stock.

Developer: [Matt87c](https://github.com/Matt87c). Original community artwork, not affiliated with the fictional HAL character's rightsholders or the Jibo/5x1 maintainers.
