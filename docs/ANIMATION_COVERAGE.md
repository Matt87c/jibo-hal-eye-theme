# HAL expression coverage and limits

## Observed regression

On physical Jibo, during a fun-fact / excitement response, a white, crescent-shaped stock eye temporarily replaced HAL before returning to the red lens. This is a **real hardware-reported visual regression** in v1.0.0.

## Root-cause evidence

- 5x1 BEam `@be/be/beacon/lib/theme-runtime.js` applies custom `face/eye.png` to stock default eye textures, but deliberately lets other explicitly named animation textures render normally.
- In `jibo-anim-db-animations`, the native `emotions/eye_expressions/happy/eye_happy_in_00.keys` / `eye_happy_out_00.keys` files reference `animations/textures/happy-glow-01.png` as a *secondary overlay texture*. That overlay is not one of HAL v1.0.0's `face/` assets. It is a credible explanation for the white half-moon during an excited/happy animation, although precise matching to the user's event has not yet been logged.
- `eye-globals/eye-laugh-01.keys` references `animations/textures/eye_shape_03.png` as a special eye texture.
- The 5x1 official theme documentation supports `atex/<exact-stock-file>.png` replacements, validated against the installed animation texture catalog, without modifying the system package.

Sources (BEam repository):
- https://github.com/Jibo-Revival-Group/BEam/blob/master/docs/themes.md
- https://github.com/Jibo-Revival-Group/BEam/blob/master/@be/be/beacon/lib/theme-runtime.js
- https://github.com/Jibo-Revival-Group/BEam/blob/master/@be/be/node_modules/jibo-anim-db-animations/animations/emotions/eye_expressions/happy/eye_happy_in_00.keys
- https://github.com/Jibo-Revival-Group/BEam/blob/master/@be/be/node_modules/jibo-anim-db-animations/animations/eye-globals/eye-laugh-01.keys

## Scope of v1.0.1

`atex/happy-glow-01.png` and `atex/eye_shape_03,04,05,06,08.png` are included. All are original red artwork derived from the approved HAL design; **no stock art is redistributed**. The three face PNGs have not changed from v1.0.0. The deterministic package builds from source.

**Not guaranteed:** every built-in animation, an overlay outside the six targeted filenames, a skill-supplied texture (5x1 deliberately preserves separate skill assets), unusual transitions, custom non-theme renderers. A theme-only ZIP cannot currently enforce a global policy of re-coloring every eye renderer. An upstream `force-the-eye-theme` policy or additional targeted stock-filename-matched overrides would be needed for complete coverage.

## Hardware signoff

1. Upload the new ZIP through BEacon > Store > Upload ZIP and Apply (v1.0.1).
2. Repeat the **same fun fact** and excitement reaction that caused the white half-moon. Watch the full eye transition, not only the settled pose.
3. Trigger happy/excited expressions again, natural laughing animations, curious/thinking animations, short and long blinking, petting, and listening.
4. Confirm each stays HAL-red or uses a deliberately themed red expression. If a stock eye appears, record the exact spoken phrase, approximate timestamp and, if possible, video. Do not claim all animations pass until repeated.
5. Confirm the selected HAL eye returns after exiting Agent Mode and Talk to NOVA; verify "Hey Jibo" remains functional.
6. Switch to None and back to HAL to verify stock restoration is deliberate and clean; no file modifications or reboot required.

## Standard for other NOVA themes

Before publishing a theme, inventory eye/overlay asset references in its target BEam version and run a physical expression matrix. Any uncovered special eye textures should be intentionally overridden or explicitly documented. Do not claim "no stock eyes" from static ZIP validation alone.
