# Changelog

## 1.0.1 - stable release packaging (on-device expression retest pending)
- Fix reported stock-white half-moon during excited/happy reactions by adding a red `happy-glow-01.png` animation override
- Add original HAL-red expression textures for stock `eye_shape_03/04/05/06/08.png` animation names
- Preserve all three proven v1.0.0 face textures byte-for-byte
- Add explicit animation-coverage limits and regression checks for fun facts, laughter, thinking and exit/recovery
- Published as stable at maintainer request; do not claim all possible stock eye assets are covered or full production hardware approval before testing v1.0.1 on physical Jibo

## 1.0.0 — initial test candidate
- Original red optical HAL-inspired eye with transparent silhouette
- Distinct native red listening texture
- Matching closed/slit blink texture
- Native eye scale set at 125%; black background
- BEam v3.1.8 / jibo-tbd 3.1.8 compatibility target
- Deterministic ZIP build, automated validation, hardware sign-off checklist
