# telestrator

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/telestrator/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. 1. **Watch it, then take it apart.** Every piece of action is seen moving before it is explained. A freeze always follows play; the explanation never comes
2. 2. **One freeze, one finding.** Each freeze says one thing (the ball wasn't cleared; nobody stepped out; he struck it from outside the box) with one label and at most two groups of lines. The same few seconds of footage are reused, each pass going one layer…

Frame and layout (1920×1080):
1. **Full-frame footage** most of the time. The packaging lives in the
2. **Labels** (black card, coloured left bar, Chinese line + small spaced English line) sit in empty grass or crowd, never over the action they

Editing grammar:
1. **Order inside one piece of action:** live at 1× (original sound) → rewind (0.6 s, reversed with tracking bars and ◀◀) → freeze ① → slow play (0.6–0.85×, frame-blended) → freeze ② → slow play with a stopwatch → freeze ③ → ball flight with a comet trail →…
2. **Lighter variants** for secondary pieces of action, so the deep breakdown stays

Type:
1. **No handwriting fonts** anywhere: printed type on a dark card belongs to the same packaging; handwriting reads as a school

Motion and drawing:
1. **Freeze entry**: white flash 0.1 s (0.55) + punch 1.035 → 1.0 in 0.35 s (ease-out) + desaturate 42 % + a cool cast + heavier vignette; then a slow 1.2 % creep. Overlays use the same transform as the picture, or they slide off the
2. **Spotlight**: everything outside a focus ellipse darkens to 0.42 (even-odd hole), 0.3 s

Sound palette:
1. **Layers**: English voice-over (one line per freeze, ≈2.5–3 s) → match sound (commentary + crowd at full level in live play; under freezes only a low-passed crowd bed, looped; the goal roar on the goal frame) → score → foley. Voice ducks everything else to…
2. **Score**: sampled band (drum kit, electric bass, staccato trumpet and trombone, timpani, horn, cellos, glockenspiel), about 120 BPM. The groove restarts at the head of each played segment, so cuts don't need a global bar grid. **On a freeze the drums stop**:…

Native moves (and how the code does them):
1. 1. **Freeze and draw** — a freeze segment = one source frame + flash + punch + desaturate + spotlight; overlays drawn by progress (the implementation, the implementation in the
2. 2. **Tracked ring** — hand keyframes of the feet point in source pixels every ~3–6 frames, linearly interpolated (the implementation, the implementation); check them with the implementation, which paints every tracked point in

Material:
1. 1. **Ask the user first** whether they have their own footage (club or academy video, their own camera, a licensed broadcast clip), line-ups, event data or photos, and the rights to use them. Their material comes
2. 2. **Where to look** (judge every file on its own

Pitfalls:
1. **Wrong tracking points** are the biggest risk: reading coordinates off a scaled contact sheet is easily 20–50 px off. Read them on full-resolution crops with a pixel ruler, then check with the
2. **Overlays not under the punch transform** slide off the players during a

