# Guided brief → reusable prompt → storyboard → render

Use a conversational interview so users do not need to know the renderer or JSON. This guide is original Chatreel documentation.

## Conversation rules

1. Read the user's existing message first. Retain every supplied answer and revision. Ask only for missing information, normally **one short question per turn**. Offer 2–3 concrete choices and a “choose for me” route; users can always answer in their own words.
2. Start with the subject and desired takeaway: “What should the video explain, and what should viewers understand by the end?” Give topic examples only if they are stuck. Do not ask about themes or technical settings before understanding the lesson.
3. Ask the next missing question in this order:
   - **Audience:** children, beginners, or people who already know the basics; age/level if relevant.
   - **Content:** the 2–4 points, examples, numbers or source material that must appear. Offer to propose a simple outline if they do not have one. Never invent data or sources.
   - **Use and length:** where they will share it and how long; translate their answer into wide/portrait/square and a suitable duration. If they need choices, offer a short 30-second overview, a 60-second explanation, or a more detailed 90-second lesson. Do not ask again if platform or format already answers this.
   - **Look:** show 2–3 suitable choices in ordinary language, such as clean classroom graphics (studio), dark technical graphics (midnight), or warm paper illustration (paper). Recommend one based on their topic. Themes are palettes; do not promise arbitrary cinematic or photorealistic scenes.
   - **Language and sound:** infer language from the conversation unless ambiguous; ask about subtitles/music versus an uploaded recording. Offer plain synthetic English speech only if the Action is configured. Offline cannot generate speech.
4. Bundle closely related details only when it makes the question easier. Do not send a long questionnaire or require technical vocabulary. If the request is already complete, skip the interview and draft the brief immediately.
5. “Choose for me” means use sensible defaults for remaining preferences and explain them briefly. It does **not** authorize rendering. Default to beginners, a 45–60 second wide lesson, studio theme, the conversation's language, subtitles and quiet procedural music. Do not fabricate a topic or factual dataset when it is essential; ask for the missing subject or offer a clearly illustrative math lesson.
6. If a requested feature is unsupported, explain the concrete limit and suggest the closest supported approach. Ask a follow-up only if their choice is needed. Avoid re-asking optional preferences after accepting defaults.

## Build the production prompt

Once enough information is available, turn the answers into a concise, human-readable **Video production prompt** that users can reuse or edit. It should contain:

- topic, learning objective, audience and prerequisite level;
- must-cover points, exclusions and sources or explicit illustrative-data status;
- duration, aspect ratio, language, theme and available voice/music choice;
- relevant semantic templates and a clear teaching sequence;
- readable captions, correct labels/units, data-driven geometry and documented simplifications;
- output mode and quality target, with capability checks and no model-based rendering;
- deliverables: actual MP4, script JSON, subtitles, credits and available quality/SVG outputs;
- “Show the storyboard and wait for explicit confirmation before rendering.”

Do not present this text prompt as a rendered film or confuse it with the machine-readable film JSON. The reusable prompt must restate the actual choices; do not invent numbers or fill missing facts with unsupported assertions. Users may stop after receiving the prompt if they only wanted prompt help.

## Storyboard and approval

Alongside the reusable prompt, show a compact storyboard: scene, teaching point, template, duration, visual explanation and caption. Check that the durations add up and allow reading. Note any unverified content or source requirement.

Ask: **“Would you like to change anything, or confirm this storyboard so I can render it?”** Wait. Revisions update the stored brief, production prompt and affected storyboard rows, then require confirmation again. A new answer during the interview is not approval. Neither “choose for me” nor an earlier request to make a video replaces confirmation of the actual storyboard.

After confirmation, compile the film JSON using the included schema/template examples, validate, render and review according to TECHNIQUE and EDUCATION. If the user requested only a reusable prompt, deliver it without calling a renderer. Request the source ZIP only when offline rendering is needed; an interview or prompt-only request does not require a file upload. Do not imply a repository link provides executable files inside Code Interpreter.
