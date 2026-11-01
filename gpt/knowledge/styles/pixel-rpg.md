# pixel-rpg

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/pixel-rpg/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Renderer-supported compact port.

Essence, and what it is not:
1. **320×180 native pixels**, scaled ×6 nearest-neighbour to 1080p; everything, text included, lives in the
2. **A limited, indexed palette**; gradients are **ordered dither**, never

Materials & rendering:
1. **Indexed framebuffer** (the implementation of palette indices) presented through a **lookup table** (index → RGB), so a whole palette can change in one frame. Camera moves are **integer pixels**; each parallax layer rounds its own
2. **Master palette** of ~32 colours (a free palette such as ENDESGA-32), plus **protected duplicates** of a few indices that no palette effect

Colour logic:
1. **Palette = feeling.** Colour depth, fades and swaps are story tools; change the whole palette by table, never by
2. **Colour depth can stand for time**: older = fewer colours, lower

Type & subtitles:
1. **The dialog box is the subtitle**, drawn in the framebuffer at the bottom quarter: a layered rounded border (ink / white / silver), a dithered dark-blue fill, a 32×32 portrait on the left, an **original** variable-width pixel font (cap ~7 px) with a 1-px…
2. **Skins follow the era** (light box for 4-colour, black box with white frame for 8-bit, blue for

Motion quality:
1. **Game-native acting**: hop forward to act, cast pose, knockback recoil, kneel, KO blink (12 fps on/off) and vanish; breath = shoulders up 1
2. **UI motion**: windows slide in over ~0.3 s (ease-out, integer px); a hand cursor bobs 1 px at 4 fps and **stops when the character

Sound palette:
1. **Chiptune voices**: pulse waves at 12.5/25/50 % duty, 4-bit triangle bass, LFSR noise drums, wavetable leads, SNES-style echo (a few taps ~180–370 ms, feedback ~0.4, low-pass in the loop). Original melodies
2. **Fidelity follows colour depth** (option): 4-colour = mono, 4-bit volume steps, low sample rate; 8-bit = NES-like mono; 16-bit = stereo with echo; a faded present = the same music

Native moves:
1. **Palette collapse / flood.** Colour depth drops one level per beat, or full colour floods back through a dither wave. *Fits content like:* a city blackout and recovery; a company in crisis; burnout and
2. **Protected colour match cut.** One exempt colour links two eras in the same screen position. *Fits content like:* a family heirloom; a brand colour across decades; a team

