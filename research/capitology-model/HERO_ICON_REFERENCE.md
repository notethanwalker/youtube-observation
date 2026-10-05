# Capitology Hero Icon Reference

Canonical HUD hero-icon source:
https://github.com/drippinghere/overwatch-hero-icons

Use the `3d/` directory for spectator HUD / hero portrait cross-reference.

Why this source:
- contains current OW2 3D hero portraits, including newer heroes such as Venture and Juno;
- icons visually match the style used in OW2 HUD/spectator hero portraits much better than splash art;
- easy to fetch by exact hero filename.

Required analysis rule:
1. Crop the player hero portrait from the HUD.
2. Compare it directly against the canonical `3d/` icon set.
3. Do not declare a hero identity unless the visual match is high-confidence.
4. If uncertain, mark the hero as uncertain and stop hero-specific reasoning until verified.
5. Never substitute memory-based hero identification when the icon reference can be checked.

Validated example:
- Quartz in the New Junk City fight around 39:00 = Sojourn, confirmed by direct comparison to `3d/sojourn.png`.

Source note:
The repository is a mirror/reference collection; hero art and game assets are Blizzard Entertainment property.
