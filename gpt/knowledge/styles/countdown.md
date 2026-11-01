# countdown

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/countdown/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. 1. **Real time.** One continuous stretch of the event, never cut, never re-ordered, never sped up. Slow-motion sources are played back at real speed. The clock and the picture can be checked against each other at any
2. 2. **The clock is the lead.** It ticks every whole second (sound and a falling digit), it says who is in control, and it changes state at

Materials & rendering:
1. **Three kinds of material at once**: video cameras of the same moment (2–8), documents (a fact sheet, a filing, a schedule: shown as paper, never retyped as a slide), and photographs (the people of the day). Our own type explains them; type printed in the…
2. **Data drawn by us**: checklists, bars, a flight or process profile, a second countdown to the next milestone. Every number comes from an official source

Type & subtitles:
1. **The live transcript is the subtitle.** A fixed box (bottom right, or a cell in the grid): a speaking light and the speaker type (commentary / loop / narrator — the narrator, our own voice, is marked in orange so it is never mistaken for the event's audio),…

Edit grammar:
1. **Screen time = event time.** One mapping, the implementation, for the whole film. Each camera has its own source offset (the implementation) measured once and baked into the frame extraction (the implementation): frames are named by film frame number, so the…
2. **Cut points are calls.** Each layout change starts on the first word of a real call in the native audio ("ten", "go for…", "ignition", a name) or on an event visible in the footage. The music follows; it never sets a

Sound palette:
1. 1. **Native sound** — the event's own audio (commentary, radio loops, crowd), high-pass 90 Hz, compressed, always on top; never
2. 2. **Narrator** (sparingly, only in gaps of the native sound, never over it): clean and close, a different gender or accent from the event's voices; Kokoro, every line through the

Native moves (and how to build them):
1. **Many into one.** At zero, every cell moves to its tile of the full frame (a 3×3 grid becomes nine 640×360 tiles) while each tile cross-fades to the same full-screen shot, chips and borders vanish in the first half, a warm white flash (the implementation,…
2. **Clock inversion.** At zero the clock block flips from dark with an orange T− to orange with dark T+, and its header changes (countdown → elapsed). *Fits:* polls closing, a store

Pitfalls of the medium:
1. **Unsyncable footage** (an edited "rover" reel with no clock or event to align on). Never fake it: label the cell "same window · not frame-synced", keep it out of the countdown's key seconds or use it only where nothing it shows contradicts the time, and say…
2. **Measuring zero.** Never trust metadata. Combine two independent marks: a visible event (ignition flash, a broadcast countdown bug's flip) and the spoken word timing ("booster" at zero). Re-measure on the file you actually cut: the implementation starts on…

