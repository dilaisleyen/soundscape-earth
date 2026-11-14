# Earth Jukebox

Explore NASA's sea surface temperature map by sound. Move over the map with a mouse, a finger or the keyboard, and the value under the pointer is turned into sound in real time, so Earth science can be heard as well as seen.

Made for the NASA International Space Apps Challenge 2026, challenge **The Earth Information Jukebox**.

> Earth Jukebox is a prototype. It is not an official NASA website, and NASA does not endorse this project.

## What it does

- Shows a NASA Earth Information Center (EIC) visualization: the **Sea Surface Temperature (SST) Anomaly** map (NASA SVS #5176).
- Lets you move through time: a slider under the map steps through 30 pictures of the same NASA series, the first available day of each month from June 2024 to October 2026 and the latest frame (11 November 2026). Moving the slider over the same spot lets you hear how a place changed.
- Reads the colour under the pointer and converts it back to a value in degrees Celsius (warmer or colder than normal) with the colour scale NASA published for the map.
- Turns that value into sound **in real time with the Web Audio API**. There are no recorded audio files: every sound is synthesised in the browser.
- Works without a mouse and without sight: full keyboard control, a spoken guide, screen reader announcements and place names.
- Keeps everything in view: on a desktop the map screen fits the window without scrolling, with the colour scale and the value under the pointer in a side panel (on a phone they sit in a bar under the map that stays at the bottom of the window). A small label next to the pointer shows the value, and the long source notes are under "About & sources".
- Gets finer detail and the latest day from NASA when you are online: a moment after you stop zooming or moving, the page asks NASA's GIBS service for just the area on screen (down to about 1 km, up to the newest day, about 250 KB to 1 MB) and paints it over the saved picture. Offline, or with the **Live detail** button off, the saved pictures are used.
- Runs in the browser from a single `index.html` plus the pictures in `data/`: no build step, no framework. The only requests it makes to another server are the ones to NASA GIBS described above.

## How the sound works

The value of the pixel under the pointer decides what you hear:

| Under the pointer | Theme | Sound |
|---|---|---|
| Normal water (within 0.25 °C of 0) | **calm** | A soft, steady, neutral chord. |
| Warmer than normal | **heartwarming** | The chord opens up, gets brighter and louder, and a high shimmering layer joins in. The warmer, the livelier. |
| Colder than normal | **melancholy** | The chord gets darker and weaker, and a distant, hollow wind takes over. The colder, the emptier. |
| Land | **grounded** | A dull, rough knock, like a step on wood or stone. |
| Ice / no data | **solitude** | A single lonely, cold glass note far away. |
| Longitude | | The sound moves from the left speaker (180° W) to the right speaker (180° E). |
| Always | | A very quiet ambient bed that slowly breathes (one breath about every 7 seconds), with a tiny rising note now and then. It stands for rebirth, life and vitality. |

The five themes are the team's names for the character of each kind of place. The name of the current theme is shown in the side panel and spoken with every position. The 0.25 °C "calm" limit only chooses the label: the sound has no dead zone and follows the value from 0 onwards, so +0.5 °C sounds slightly warm and +4 °C very warm. The sound design was described and decided by the team; the mapping lives in `soundFor()`, `hitLand()`, `hitIce()` and the ambient code in `index.html`.

## Controls

| Action | Mouse / touch | Keyboard |
|---|---|---|---|
| Hear a place | Hover (mouse) or slide one finger | Tab to the map, then arrow keys (Shift = bigger steps) |
| Zoom | Wheel, pinch with two fingers, `+` / `-` buttons | `+`, `-`, `0` (whole map) |
| Move the zoomed map | Drag (mouse), two fingers (touch) | Arrow keys follow the ring |
| Where am I? | | `W` |
| Repeat the last message | | `R` |
| Help | | `H` |
| Start / stop the sound | Start sound button | `Space` |
| Grid on / off | Grid button | `G` |
| Live NASA detail on / off | Live detail button next to the time slider | |
| Move through time | Time slider under the map | Arrow keys, `Home`, `End`, `PageUp`, `PageDown` while the slider has focus |
| Country names on / off | Labels button | `L` |
| Interface sounds on / off | UI sounds button | `U` |
| Why does it sound like this? | "Why does it sound like this?" panel | `E` (short reason), `D` (all details) |
| Accessibility options | Accessibility options button | `Ctrl` + `Alt` + `B` |

The page has two separate screens. The **landing screen** opens first and asks whether you want blind assistance (`F` = yes, `J` = no). You can choose the built-in voice (the page speaks by itself) or your own screen reader, and hear a short spoken guide. Then the **map screen** opens. "Accessibility options" (or `Ctrl` + `Alt` + `B`) takes you back to the landing screen; the sound keeps playing while you move between the screens.

## "Why does it sound like this?"

A panel next to the map (a collapsible section in the bar under the map on a phone) explains the sound under the pointer: the value, which sound features it changes (brightness, loudness, shimmer, wind, rhythm, stereo and so on), the theme and what it means. It states the unit (°C anomaly: degrees warmer or colder than normal) and that 0 °C means normal. The text is generated from the same rules and numbers the sound uses, so it cannot describe something the sound does not do. Listeners can press `E` for a one-sentence reason and `D` for the details.

## Interface sounds

Buttons, zoom and the change between the two screens answer with very soft notes from the same A and E family as the chords (a tick for buttons, a small rise or fall for zoom, a rising or falling pair for the screens). They are much quieter than the data sounds, which always stay in front, and they are only heard while the sound is running. The **UI sounds** button (or `U`) switches them off without touching the data sounds.

## Accessibility

- Fully usable with the keyboard; visible focus; a logical tab order.
- Positions are announced as, for example, "North Atlantic, plus 2.3 degrees", either spoken by the built-in voice or sent to a screen reader through an `aria-live` region.
- When the screen changes, keyboard focus moves to the new screen's heading and the new screen is announced.
- Motion is small and short (only fades and a slight slide). If your system asks for reduced motion, the slide is removed and the fades get shorter.
- Country names are drawn on the map as a label layer (bigger countries on the whole map, smaller ones as you zoom in, never overlapping). The label layer is separate from the picture the values are read from, so it cannot change the sound or the values.
- The country named for the pointer comes from label points only, so it is approximate: a country is named only when it is clearly the closest one (in a test against Natural Earth's real borders it named about 4 in 10 land points and was right 98 times in 100 of those); otherwise the continent is named.
- Place names for oceans, seas and continents are rough rectangles and can be a little off near coasts.
- High contrast: the main text and controls measure above 8:1 (WCAG AA asks for 4.5:1).

## Data and accuracy

- Map: NASA's Scientific Visualization Studio, *Sea Surface Temperature (SST) Anomaly - Near Real Time*, SVS #5176 (the version without date stamps, equirectangular, 1024 x 512). The picture is kept as a copy in this project: the map opens on the most recent frame that was available when it was downloaded, on 14 November 2026 (it is the frame of 11 November 2026; we checked this by comparing it with NASA's frames of 9, 10 and 11 November), and it does **not** update by itself. The copy is also in `data/nasa/sst/`.
- Live detail (NASA GIBS): GIBS serves the *MUR sea surface temperature anomaly* layer (`GHRSST_L4_MUR_Sea_Surface_Temperature_Anomalies`) in classes of 0.1 °C from -3 to +3 °C, and the page turns each colour back into its class with GIBS's own colour table (all 287,594 data pixels of a test picture matched the table exactly) and repaints it in the page's colours, so the colour scale stays right. It is **not the same product** as the saved SVS picture: for the same day (11 November 2026) the two differ by 0.32 °C on average (median 0.22 °C, 55% of ocean points within 0.25 °C), and GIBS stops at ±3 °C while the SVS scale goes to ±4 °C, so the hottest El Niño water sounds a little less extreme with live detail. It lines up with the saved picture (we tried shifts of 1 to 2 pixels: none fits better). The live picture asked for is the day the time slider is on (the newest day GIBS has, 13 November 2026 at the time of writing, for the last position). Land, ice and places without data come from the saved picture.
- Time slider frames: NASA publishes the frames of this series only as 4096 x 2048 EXR files (half-float, ZIP compressed). For the slider we downloaded the first available frame of each month from June 2024 to October 2026, reduced each one to 1024 x 512 (average of 4 x 4 pixels), converted it to 8-bit colour with the standard sRGB curve and saved it as a JPEG in `data/nasa/sst/frames/` (about 240 KB each, 7 MB in all). The conversion reproduces NASA's colour bar to within 0.5 of 255 on average, and the 11 November frame read with our colour table differs from NASA's own 1024 x 512 picture by 0.06 °C on average (98.7% of ocean pixels within 0.25 °C). The JPEG compression itself adds about the same 0.06 °C, as it does for NASA's picture, so differences smaller than about 0.1 °C should not be read as real. The frames are loaded from the page's own web address, so the slider works on the hosted page or a local web server; opened as a plain file, the browser does not let a page read the pixels of other files, and the slider is switched off with a note (the rest of the page works).
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
- Natural Earth (public domain), *Admin 0 - Countries*, 1:50m. https://www.naturalearthdata.com/ Used only to draw country names and to name the country under the pointer; a reduced copy (names, label points, sizes) is inside `index.html`.
- Web Audio API and Web Speech API (built into browsers; no files or libraries are included).
- NASA GIBS (Global Imagery Browse Services), layer `GHRSST_L4_MUR_Sea_Surface_Temperature_Anomalies`, https://gibs.earthdata.nasa.gov/ (used live, nothing is stored). "We acknowledge the use of imagery provided by services from NASA's Global Imagery Browse Services (GIBS), part of NASA's Earth Science Data and Information System (ESDIS)."
- The frames for the time slider were prepared once, offline, with Python (NumPy and Pillow). None of that is part of the page.
- No other libraries, fonts, images or sound files are used, and NASA GIBS is the only external service. No NASA logo is used.

## Data & image credits

All NASA pictures live in `data/nasa/`, and `data/nasa/SOURCES.json` lists every file with its original URL, download date, data date, SVS ID, dataset name, the credit NASA asks for and the people credited. The "About & sources" dialog of the page is built from that file. `scripts/fetch_nasa_data.py` (Python standard library only) downloads the files again and updates the size, checksum and date in `SOURCES.json`. The pictures are copies kept in this project because NASA's server does not send CORS headers, so a page cannot read the pixels of a picture loaded straight from it.

- **NASA's Scientific Visualization Studio**, *Sea Surface Temperature (SST) Anomaly - Near Real Time*, SVS #5176, https://svs.gsfc.nasa.gov/5176/
  - Visualizer: Kel Elkins (USRA). Scientist: Atousa Saberi (NASA/GSFC). Technical support: Laurence Schuler and Ian Jones (ADNET Systems, Inc.).
  - Underlying data: JPL MUR SST analysis (Multi-scale Ultra-high Resolution Sea Surface Temperature), PO.DAAC; SVS dataset ID 845.
  - In this project (31 files): the map picture of 11 November 2026 and NASA's colour bar (both as downloaded on 14 November 2026), and 29 time slider pictures (the first available day of each month from June 2024 to October 2026) that we converted from NASA's EXR frames.
- **Natural Earth** (public domain), *Admin 0 - Countries*, 1:50m, https://www.naturalearthdata.com/ (used for the country names only; a reduced copy is inside `index.html`).
## AI use

The code in this project was written with the help of an AI assistant (Claude, by Anthropic), working from the team's instructions. The project idea, the sound design (what each kind of place should sound like and feel like) and the decisions about the interface were made by the team.

## License

The code in this project is by the Earth Jukebox team and is released under the [MIT License](LICENSE).

NASA imagery and data in `data/nasa/` are not covered by this license. They are provided by NASA and used under [NASA's Media Usage Guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/). NASA does not endorse this project.
