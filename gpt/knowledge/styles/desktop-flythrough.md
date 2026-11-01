# desktop-flythrough

Adapted from Lemomo/LemoLab, Lemo-Opuscar styles/desktop-flythrough/STYLE.md. CC BY 4.0; see ATTRIBUTION.md.

Reference only: unavailable in this renderer. Never submit this style to /render. Real-footage styles are excluded from this project.

Essence, and what it is not:
1. **The desk is the world.** A matte paper mat with a regular dot grid lies on a light wooden desk, lit by one low warm sun through a window. Everything sits on it and casts a long, soft shadow. A few everyday desk things (a pen, sticky notes, a mug, earbuds)…
2. **Interfaces are paper cards.** Phones, tools and dashboards are rounded slabs a few millimetres thick with the interface printed on top. They are places: characters stand and hop on them, and parts of the interface rise out of them as small 3D

Materials & rendering:
1. **Light**: one directional sun low from the back-left (about 20° up, so a toy's shadow is two or three times its height), a 4096 soft shadow map that follows the camera target and resizes with distance; a cool-sky / warm-ground hemisphere fill, so shadows…
2. **Desk**: a dotted paper mat (a thin rounded slab whose size is a multiple of two dot spacings, so the printed dots line up with any 3D dots) on a procedural light-oak plane (planks, long soft grain). Soft window-light patches (blurred four-pane shapes, warm,…

Colour logic:
1. **One light ground** (the mat) with a slightly darker dot, cool-tinted so the warm sun leaves it fresh; a warm wooden desk around it; cards in a near-white of the same temperature; **one dark ink** for print; **one accent reserved for what matters now**: the…

Type & subtitles:
1. **In the world, only keywords and numbers**: step badges (a camera-facing accent pill with a digit and one word), sizes, a name on a screen, a banner, a title card. Text meant to be read is framed above the subtitle area, held still for its reading time, and…
2. **Titles are objects on the desk**: an opening tent card beside the first stop; at the end a large paper card dropped onto open desk in the final frame. Where depends on the layout: wherever it covers no station, route or character and sits clear of the…

Motion quality:
1. **Hops**: an arc with squash and stretch (stretch about 14 % in the air, squash about 30 % for 0.2 s on landing, a small anticipation squash before take-off). Groups move follow-the-leader, each a 16th behind the one ahead, so they never close
2. **Characters act**: they blink every couple of seconds, bounce on the beat while they wait, squint when they are squashed, lean towards what they look

Sound palette:
1. **Score**: bright and warm, acoustic in feel: marimba (with vibraphone under long notes), plucked bass, a soft synthetic kick (a short sine sweep), claps, shaker, a quiet string pad. One key, diatonic chords, about one chord per bar. Under a voice the score…
2. **Foley**: every action has a sound. Pop: a marimba note from the current chord plus an upward sweep. Hop: a soft tick. Landing: a felt thump. Press or stamp: a low thump with a crumble. Typing: dry key clicks. Ding: two bell notes from the chord. Camera…

Native moves:
1. **Sticker pop.** A flat pixel sticker on a card stands up and extrudes into a toy on a 16th. *Fits content like:* a new user, file or job appearing; a feature switched on; an order
2. **Reverse pop.** A toy lies back down into a sticker or a print. *Fits content like:* a photo delivered into a chat; a snapshot saved; a task

Pitfalls of the medium:
1. **Softness**: depth of field and motion blur easily turn a subject or its words to mush. Blur only what lies behind a focus plane set a little beyond the subject, lightly (≤ 5 px), never anything in front; let the shutter shrink with camera speed so a streak…
2. **Flat print read at a low angle**: text on a card seen from 20° is unreadable. Rise to 55–70° to read a card; put text the low camera must read on a standing

