## Controls:
- W, Up or Space - Jump
- Down - Crouch
- Left or A/Right or D - Move Left/Right
- L - Level toggle (debug/test feature, remove before completion)

## Bugs
- Infinite jump
- Platform collision only snaps to top or bottom (no wall cling/wall jump)
- Crouch only shifts the sprite, it does not resize it
- Enemy is not affected by gravity for some reason. Also unaffected by level switching.
- Player has no i-frames when hit by an enemy, so their health gets melted really quickly.

## Things to add
- HUD for player stats, points, whatever else
- Custom sprites
- Larger levels
- More than just 2 levels
- Proper level start/end triggers. Currently, the level switch is bound to "L".
- Invisible wall at the start of the level.
- Different enemy types, as well as repositioning enemies in between levels
- Invulnerability period after the player gets hit, in which their sprite (until a proper sprite is made) will change color. This will eventually be replaced by a stagger sprite.
- Ways to attack/remove the enemies
- Other platform types (potentially things like lava, ice, etc.)
