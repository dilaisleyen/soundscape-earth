# Earth Jukebox

Explore NASA's sea surface temperature map by sound. Move over the map with a mouse, a finger or the keyboard, and the value under the pointer is turned into sound in real time, so Earth science can be heard as well as seen.

Made for the NASA International Space Apps Challenge 2026, challenge **The Earth Information Jukebox**.

> Earth Jukebox is a prototype. It is not an official NASA website, and NASA does not endorse this project.

## What it does

- Shows a NASA Earth Information Center (EIC) visualization: the **Sea Surface Temperature (SST) Anomaly** map (NASA SVS #5176).
- Reads the colour under the pointer and converts it back to a value in degrees Celsius (warmer or colder than normal) with the colour scale NASA published for the map.
- Turns that value into sound **in real time with the Web Audio API**. There are no recorded audio files: every sound is synthesised in the browser.
- Works without a mouse and without sight: full keyboard control, a spoken guide, screen reader announcements and place names.
- Runs entirely in the browser from a single `index.html`: no build step, no framework, and the page itself makes no network requests.

## How the sound works

The value of the pixel under the pointer decides what you hear:

| Under the pointer | Sound |
|---|---|
| Normal water (about 0 °C) | A soft, steady, neutral chord. |
| Warmer than normal | The chord opens up, gets brighter and louder, and a high shimmering layer joins in. The warmer, the livelier. |
| Colder than normal | The chord gets darker and weaker, and a distant, hollow wind takes over. The colder, the emptier. |
| Land | A dull, rough knock, like a step on wood or stone. |
| Ice / no data | A single lonely, cold glass note far away. |
| Longitude | The sound moves from the left speaker (180° W) to the right speaker (180° E). |
| Always | A very quiet ambient bed that slowly breathes (one breath about every 7 seconds), with a tiny rising note now and then. It stands for rebirth, life and vitality. |

The sound design was described and decided by the team; the mapping lives in `soundFor()`, `hitLand()`, `hitIce()` and the ambient code in `index.html`.

## Controls

| Action | Mouse / touch | Keyboard |
|---|---|---|
| Hear a place | Hover (mouse) or slide one finger | Tab to the map, then arrow keys (Shift = bigger steps) |
| Zoom | Wheel, pinch with two fingers, `+` / `-` buttons | `+`, `-`, `0` (whole map) |
| Move the zoomed map | Drag (mouse), two fingers (touch) | Arrow keys follow the ring |
| Where am I? | | `W` |
| Repeat the last message | | `R` |
| Help | | `H` |
| Start / stop the sound | Start sound button | `Space` |
| Grid on / off | Grid button | `G` |
| Accessibility options | Accessibility options button | `Ctrl` + `Alt` + `B` |

The page has two separate screens. The **landing screen** opens first and asks whether you want blind assistance (`F` = yes, `J` = no). You can choose the built-in voice (the page speaks by itself) or your own screen reader, and hear a short spoken guide. Then the **map screen** opens. "Accessibility options" (or `Ctrl` + `Alt` + `B`) takes you back to the landing screen; the sound keeps playing while you move between the screens.

## Accessibility

- Fully usable with the keyboard; visible focus; a logical tab order.
- Positions are announced as, for example, "North Atlantic, plus 2.3 degrees", either spoken by the built-in voice or sent to a screen reader through an `aria-live` region.
- When the screen changes, keyboard focus moves to the new screen's heading and the new screen is announced.
- Motion is small and short (only fades and a slight slide). If your system asks for reduced motion, the slide is removed and the fades get shorter.
- Place names (oceans, seas and continents) are rough rectangles and can be a little off near coasts.
- High contrast: the main text and controls measure above 8:1 (WCAG AA asks for 4.5:1).

## Data and accuracy

- Map: NASA's Scientific Visualization Studio, *Sea Surface Temperature (SST) Anomaly - Near Real Time*, SVS #5176 (the version without date stamps, equirectangular, 1024 x 512). The picture is kept as a copy in this project: it shows the most recent frame available when it was downloaded, on 14 November 2026, and it does **not** update by itself. The copy is also in `data/`.
- The values are **read back from the colours** of the picture, not from the original data files. We checked the conversion against NASA's colour bar: across the whole scale the average error is 0.012 °C and the largest 0.052 °C. The picture itself adds more uncertainty (image compression, blending at coasts), so treat values as approximate.
- The colour scale ends at -4 °C and +4 °C; anything beyond is shown as the end of the scale.
- 0 °C means "same as normal". The source page does not state which reference period "normal" is based on, so we do not claim one.
- The SVS item is tagged "Earth Information Center" on NASA's site. It is not one of the maps listed in the challenge resources; the event team confirmed that it is acceptable.

## Run it

Open `index.html` in a modern browser (Chrome, Edge, Firefox or Safari). Sound starts after your first click or key press, because browsers do not allow sound before that.

For a local web server: `python -m http.server`, then open `http://localhost:8000`.

## References

- NASA Scientific Visualization Studio. *Sea Surface Temperature (SST) Anomaly - Near Real Time*, ID 5176. https://svs.gsfc.nasa.gov/5176/ Visualizer: Kel Elkins (USRA). Scientist: Atousa Saberi (NASA/GSFC). Credit: NASA's Scientific Visualization Studio.
- Dataset behind the visualization: JPL Multi-scale Ultra-high Resolution (MUR) SST analysis, NASA JPL / PO.DAAC (MUR-JPL-L4-GLOB-v4.1). https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1
- Web Audio API and Web Speech API (built into browsers; no files or libraries are included).
- No other libraries, fonts, images, sound files or external services are used. No NASA logo is used.

## AI use

The code in this project was written with the help of an AI assistant (Claude, by Anthropic), working from the team's instructions. The project idea, the sound design (what each kind of place should sound like and feel like) and the decisions about the interface were made by the team.

## License

NASA's visualization is credited to NASA's Scientific Visualization Studio. All other code in this project is by the Earth Jukebox team.
