# Educational template catalog

Each JSON is a complete, runnable film. Edit content rather than inventing scene fields. Defaults include heuristic reading holds; review them for your audience.

| Template | Purpose | Example JSON | QA clips |
|---|---|---|---|
| `title` | Lesson opener with a visual concept and subtitle | [JSON](title.json) | [Python](../examples/education/templates/title/python.mp4) / [Canvas](../examples/education/templates/title/canvas.mp4) |
| `concept` | A central idea connected to explanatory cards | [JSON](concept.json) | [Python](../examples/education/templates/concept/python.mp4) / [Canvas](../examples/education/templates/concept/canvas.mp4) |
| `process` | Ordered steps with directional connections | [JSON](process.json) | [Python](../examples/education/templates/process/python.mp4) / [Canvas](../examples/education/templates/process/canvas.mp4) |
| `cycle` | A closed sequence with curved directional connections | [JSON](cycle.json) | [Python](../examples/education/templates/cycle/python.mp4) / [Canvas](../examples/education/templates/cycle/canvas.mp4) |
| `comparison` | Two sides with aligned points of comparison | [JSON](comparison.json) | [Python](../examples/education/templates/comparison/python.mp4) / [Canvas](../examples/education/templates/comparison/canvas.mp4) |
| `timeline` | Dated milestones placed in supplied order | [JSON](timeline.json) | [Python](../examples/education/templates/timeline/python.mp4) / [Canvas](../examples/education/templates/timeline/canvas.mp4) |
| `bar-chart` | Zero-baseline bars whose lengths encode supplied values | [JSON](bar-chart.json) | [Python](../examples/education/templates/bar-chart/python.mp4) / [Canvas](../examples/education/templates/bar-chart/canvas.mp4) |
| `line-chart` | A labelled numeric series with a shared linear scale | [JSON](line-chart.json) | [Python](../examples/education/templates/line-chart/python.mp4) / [Canvas](../examples/education/templates/line-chart/canvas.mp4) |
| `donut-chart` | Nonnegative values normalized to a complete whole | [JSON](donut-chart.json) | [Python](../examples/education/templates/donut-chart/python.mp4) / [Canvas](../examples/education/templates/donut-chart/canvas.mp4) |
| `equation` | Restricted arithmetic expression, verified substitutions and result | [JSON](equation.json) | [Python](../examples/education/templates/equation/python.mp4) / [Canvas](../examples/education/templates/equation/canvas.mp4) |
| `number-line` | Numeric values positioned on an explicit number line | [JSON](number-line.json) | [Python](../examples/education/templates/number-line/python.mp4) / [Canvas](../examples/education/templates/number-line/canvas.mp4) |
| `fraction` | Exact numerator out of denominator as equal-area cells | [JSON](fraction.json) | [Python](../examples/education/templates/fraction/python.mp4) / [Canvas](../examples/education/templates/fraction/canvas.mp4) |
| `labeled-diagram` | Central illustration with explicit callouts and leaders | [JSON](labeled-diagram.json) | [Python](../examples/education/templates/labeled-diagram/python.mp4) / [Canvas](../examples/education/templates/labeled-diagram/canvas.mp4) |
| `solar-energy` | Simplified sunlight → PV DC → inverter AC → home flow | [JSON](solar-energy.json) | [Python](../examples/education/templates/solar-energy/python.mp4) / [Canvas](../examples/education/templates/solar-energy/canvas.mp4) |
| `water-cycle` | Evaporation, condensation, precipitation and collection | [JSON](water-cycle.json) | [Python](../examples/education/templates/water-cycle/python.mp4) / [Canvas](../examples/education/templates/water-cycle/canvas.mp4) |
| `recap` | A readable summary with numbered takeaways | [JSON](recap.json) | [Python](../examples/education/templates/recap/python.mp4) / [Canvas](../examples/education/templates/recap/canvas.mp4) |
| `quiz` | Question, delayed reveal and an explicit correct option | [JSON](quiz.json) | [Python](../examples/education/templates/quiz/python.mp4) / [Canvas](../examples/education/templates/quiz/canvas.mp4) |
| `code-walkthrough` | Literal code with line numbers and explanatory notes | [JSON](code-walkthrough.json) | [Python](../examples/education/templates/code-walkthrough/python.mp4) / [Canvas](../examples/education/templates/code-walkthrough/canvas.mp4) |

Run `python renderer-py/render.py --template equation --profile production --out artifacts/equation`. The QA clips intentionally last only five seconds and may be shorter than recommended reading holds. See [EDUCATION.md](../gpt/knowledge/EDUCATION.md) for content fields and limitations.
