# Soundscape Earth

Explore NASA's sea surface temperature map by sound. Move over the map with a mouse, a finger or the keyboard, and the value under the pointer is turned into sound in real time, so Earth science can be heard as well as seen.

Made for the NASA International Space Apps Challenge 2026, challenge **The Earth Information Jukebox**.

> Soundscape Earth is a prototype. It is not an official NASA website, and NASA does not endorse this project.

## What it does

- Shows a NASA Earth Information Center (EIC) visualization: the **Sea Surface Temperature (SST) Anomaly** map (NASA SVS #5176).
- Has two data views under the map. **Latest (NASA EIC)** is the picture the page opens with (NASA SVS #5176, 11 November 2026) with its own colour scale, sharpened by the live detail when you are online. **Through the years (2002–today)** is a slider with 25 steps: 13 November of every year from 2002 to 2025, and **Today** (the newest day the GIBS layer had when the picture was downloaded; the page shows the date that is written in `data/nasa/SOURCES.json` and never looks for a newer day by itself). Moving the slider changes the map, the value, the sound and the theme, with a short cross-fade (none with *reduce motion* set in the system), and a small line chart shows the value of the spot you are on in all 25 steps, with the 0 °C line marked as normal and a sentence for screen readers (for example "Lowest 2007 −1.4 °C, highest today +3.0 °C, today +3.0 °C."). The colour scale, the notes and the "normal" definition change with the view.
- Has three sound layers that can be switched on and off one by one (all on at the start): **Ocean temperature** (the sound the page always had), **Human presence** (theme *chaotic*) and **Wildlife diversity** (theme *alive & peaceful*). The last two sound over land only; the sea stays with the ocean temperature, and the dull land knock stays far in the background while they are on. More people (people per km², logarithmic scale) means a busier, more chaotic sound: crowd murmur, traffic rumble, horns and clatter, from a hush in an empty place to constant chaos at 1000 people per km² and more. More mammal species (logarithmic) means a livelier but always peaceful sound: soft chirps on a calm scale, a warm slow chord and fine air. Where both are high they mix in proportion to their own values. The right panel shows *Human presence: … people/km²* and *Wildlife diversity: … mammal species* with their themes, the "Why does it sound like this?" panel explains them from the real mapping, and each layer can also be shown over the land on the map ("on map", Data view, half see-through; nothing changes on the map by default).
- Reads the colour under the pointer and converts it back to a value in degrees Celsius (warmer or colder than normal) with the colour scale NASA published for the map.
- Turns that value into sound **in real time with the Web Audio API**. There are no recorded audio files: every sound is synthesised in the browser.
- Works without a mouse and without sight: full keyboard control, a spoken guide, screen reader announcements and place names.
- Keeps everything in view: on a desktop the map screen fits the window without scrolling, with the colour scale and the value under the pointer in a side panel (on a phone they sit in a bar under the map that stays at the bottom of the window). A small label next to the pointer shows the value, and the long source notes are under "About & sources".
- Gets finer detail and the latest day from NASA when you are online: a moment after you stop zooming or moving, the page asks NASA's GIBS service for just the area on screen (down to about 1 km, up to the newest day, about 250 KB to 1 MB) and paints it over the saved picture. Offline, or with the **Live detail** button off, the saved pictures are used.
- Shows a real map under the temperature picture: NASA GIBS's Blue Marble (shaded relief and sea floor) is drawn with [Leaflet](https://leafletjs.com/), and the temperature picture is laid over it with the land and the ice see-through, so land shows more and more detail as you zoom in (up to 64 times). Two views: **Earth view** (the default: only the NASA base map) and **Data view** (the temperature colours over it, as solid as the **Data opacity** slider says, 75 % at the start). The colour scale stays in Earth view with a note that says to switch to Data view to see its colours on the map. Leaflet only draws: every value, sound and spoken text is still read from the original, unchanged picture. Without the network, or if the tiles do not load, the page goes back to the saved picture alone and says so in a small note.
- Runs in the browser from a single `index.html` plus the pictures in `data/` and a copy of Leaflet in `vendor/leaflet/`: no build step, no framework. The only requests it makes to another server are the ones to NASA GIBS described above.

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
|---|---|---|
| Hear a place | Hover (mouse) or slide one finger | Tab to the map, then arrow keys (Shift = bigger steps) |
| Zoom | Wheel, pinch with two fingers, `+` / `-` buttons | `+`, `-`, `0` (whole map) |
| Switch Earth view / Data view | View button (next to Labels) | `V`; the button and the slider can also be reached with `Tab` |
| Data opacity (Data view) | Data opacity slider under the map | Arrow keys, `Home`, `End` while the slider has focus |
| Lock the sound on one spot | Left click (mouse) | Right click releases it; arrow keys or a finger also take over |
| Move the zoomed map | Drag (mouse), two fingers (touch) | Arrow keys follow the ring |
| Where am I? | | `W` |
| Repeat the last message | | `R` |
| Help | | `H` |
| Start / stop the sound | Start sound button | `Space` |
| Grid on / off | Grid button | `G` |
| Live NASA detail on / off (Latest view) | Live detail button under the map | |
| Choose Latest or Through the years | The two buttons under the map | `Tab` to a button, `Enter` |
| Move through the years | Year slider under the map (Through the years view) | `Left` / `Right` arrow while the slider has focus (the map keeps its own arrow keys), `Home` = 2002, `End` = Today |
| Read the chart of the spot | | `C` |
| Sound layers on / off | The three check boxes under "Sound layers" | `T` ocean temperature, `P` human presence (people), `M` wildlife diversity (mammals); each announces the new state |
| Show a land layer on the map | "on map" check box beside Human presence / Wildlife diversity (Data view, needs the base map) | `Tab` to the check box, `Space` |
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
- Live detail (NASA GIBS): GIBS serves the *MUR sea surface temperature anomaly* layer (`GHRSST_L4_MUR_Sea_Surface_Temperature_Anomalies`) in classes of 0.1 °C from -3 to +3 °C, and the page turns each colour back into its class with GIBS's own colour table (all 287,594 data pixels of a test picture matched the table exactly) and repaints it in the page's colours, so the colour scale stays right. It is **not the same product** as the saved SVS picture: for the same day (11 November 2026) the two differ by 0.32 °C on average (median 0.22 °C, 55% of ocean points within 0.25 °C), and GIBS stops at ±3 °C while the SVS scale goes to ±4 °C, so the hottest El Niño water sounds a little less extreme with live detail. It lines up with the saved picture (we tried shifts of 1 to 2 pixels: none fits better). The live picture asked for is the newest day GIBS has (13 November 2026 at the time of writing). It belongs to the Latest view; the Through the years view does not use it. Land, ice and places without data come from the saved picture.
- Base map (NASA GIBS): the layer `BlueMarble_ShadedRelief_Bathymetry` (a still picture, tile matrix set `500m`, levels 0 to 7, about 300 m per pixel at the finest) is shown under the temperature picture. It is for looking only: no value, sound or text is read from it. The temperature picture is shown over it as a copy in which the land and ice pixels are see-through (decided with the same rule as the reading code, `readPixel`); the reading itself always uses the original picture, through the same point -> longitude/latitude -> pixel path as before. The base map uses the same geographic coordinates (EPSG:4326, longitude and latitude laid out flat) as the picture; Leaflet's `L.CRS.EPSG4326` is used with the pixel grid of GIBS's tiles (NASA's own Leaflet example does this with proj4leaflet), and the map is placed where the page's own view says (the two agree to about one screen pixel). The closest zoom is 64 times (about 5.6 degrees across the map): there the live detail (about 1 km, 0.01 degrees) is only 1 to 2 screen pixels wide, so it does not look blocky. Without the live detail the saved picture has pixels of about 39 km, so on a coast a strip of land may be coloured; the page hides the saved picture under the live detail as soon as the live detail covers the view. Without the base map the closest zoom stays 16 times.
- Earth view and Data view change only what is **shown**. The value, the sound, the theme, the value label and the spoken texts are read from the original picture (and the live detail) in both views, so you can explore the temperature by sound on the plain Earth map. Without the base map there is only the Data view (the View button is disabled and says why). The layers are always drawn smoothly (the browser blends between pixels), never as blocks, and they fade in and out when the view changes (no fade with *reduce motion* set in the system). Blend modes were compared on the dark sea floor of the base map: the plain blend at 75 % is the most faithful to the colour scale; `hard-light` at about 85 % is the richest, because it also shows the sea-floor relief through the colours, but its colours no longer match the scale. `soft-light` and `overlay` make the sea almost black. To try another one, add `?blend=hard-light` (or `screen`, `multiply`, `color`, ...) to the address.
- Through the years (NASA GIBS): the 25 pictures are GIBS's *MUR25 sea surface temperature anomaly* layer (`GHRSST_L4_MUR25_Sea_Surface_Temperature_Anomalies`, JPL MUR25 v4.2, 0.25 degrees; the 1 km layer used for the live detail only starts in 2019, so one layer is used for all years). They were downloaded with GIBS's WMS (`GetMap`, EPSG:4326, -180..180 and -90..90, 2048 x 1024 PNG, about 0.5 MB each, 13 MB in all) into `data/nasa/sst-yearly/`; every 13 November from 2002 to 2025 exists in the layer (we checked each one). Each picture is in GIBS's own colours (62 classes of 0.1 °C from -3 to +3 °C), and the page turns a colour into a value with GIBS's colour table ([GHRSST_Sea_Surface_Temperature_Anomalies.xml](https://gibs.earthdata.nasa.gov/colormaps/v1.3/GHRSST_Sea_Surface_Temperature_Anomalies.xml), a copy is in `data/nasa/sst-yearly/`; the table in `index.html` was checked against it entry by entry). All 25 steps use that one table, and GIBS stops at ±3 °C, so very warm water reads +3.0 °C. **What "normal" means here:** GIBS does not say; the PO.DAAC dataset pages say the anomaly is measured against the average of the same calendar day over 2003–2014 ([MUR25 v4.2](https://podaac.jpl.nasa.gov/dataset/MUR25-JPL-L4-GLOB-v04.2)). For the Latest (SVS) picture NASA does not state the reference period. The two views are different products and cannot be compared point by point. In the pictures land, ice and places without data are see-through; the land / ice mask of the latest picture tells which of the two a spot is, and a sea spot without data in a step reads as "ice / no data". The pictures are loaded when needed (the page opens with none of them; the step you ask for first, then the others one by one for the chart). To replace the Today picture, run `python scripts/fetch_nasa_data.py --only today`: it asks GIBS for the newest day, downloads it and writes its date into `SOURCES.json`.
- Human presence (NASA SEDAC through GIBS): the five GIBS layers `GPW_Population_Density_2000` to `_2020` (Gridded Population of the World, version 4.11, adjusted to the UN country totals, 30 arc-second cells) were downloaded as 2048 x 1024 PNG pictures (about 0.24 MB each) into `data/nasa/gpw/`, with GIBS's colour table ([GPW_Population_Density_2020.xml](https://gibs.earthdata.nasa.gov/colormaps/v1.3/GPW_Population_Density_2020.xml); it is the same file for every year; the table in `index.html` is built from it). Unit: persons / km². 37 classes of growing width (from 0.5 per class at low density to 75 per class, up to 1000); the top class is *1000 and more*, so every denser place counts as 1000 and a big city and a very dense one sound alike. The scale is not exactly logarithmic, so the sound uses the logarithm of the middle of each class (1 person per km² is silent, 1000 or more is full). Cells with fewer than 1 person per km² and water are see-through in the pictures (read as "under 1 person per km²"). The picture nearest to the year on screen is used: 2002 reads 2000, 2003–2007 read 2005, 2008–2012 read 2010, 2013–2017 read 2015, 2018 and later (and Today and the Latest view) read 2020; the panel says which GPW year it is. GIBS reduced the 1 km data to the 2048 x 1024 size, so each pixel is one cell, not an average: places smaller than about 20 km can be missed or caught at their densest.
- Mammal species richness data (IUCN Red List via NASA SEDAC/CIESIN) are used for non-commercial, educational purposes. Full citation: Center For International Earth Science Information Network-CIESIN-Columbia University & NatureServe. (2015). Gridded Species Distribution: Global Mammal Richness Grids, 2015 Release (Version 2015.00) [Data set]. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4N014G5
- Wildlife diversity (NASA SEDAC through GIBS): the GIBS layer `Mammal_Richness_Grids_All_Species_2013` (Global Mammal Richness Grids, 2015 release) was downloaded as a 2048 x 1024 PNG picture (0.43 MB) into `data/nasa/mammals/`, with GIBS's colour table (one class for every number of species from 1 to 203). The value is the **number of mammal species** whose range covers the cell, built from IUCN Red List ranges downloaded in April 2013, so it is a 2013 picture, **mammals only (no birds)**, the same in every year (the panel says so), and not a count of animals. It covers the sea too (marine mammals: 21 species in the middle of the Pacific); the page uses it over land only. Species count is read on a logarithmic scale (1 species is nearly calm, 200 is the liveliest). The same 20 km sampling remark applies. **Terms:** NASA Earthdata says both datasets are openly shared without restriction (EOSDIS Data Use and Citation Guidance). The mammal grids are built from IUCN Red List ranges; the SEDAC dataset page could not be opened from the computer this was built on, so whether IUCN's own terms add a condition for keeping a copy of this derived picture in the project has **not been checked**: read the "Use constraints" at the SEDAC page before the copy is shared more widely.
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
- NASA GIBS, layer `GHRSST_L4_MUR25_Sea_Surface_Temperature_Anomalies` (Sea Surface Temperature Anomalies, L4, MUR25, GHRSST), WMS, https://gibs.earthdata.nasa.gov/ (the 25 pictures of the years view, downloaded once and kept in `data/nasa/sst-yearly/`), and its colour table. The same acknowledgement applies.
- Center for International Earth Science Information Network (CIESIN), Columbia University. (2017). Gridded Population of the World, Version 4 (GPWv4): Population Density, Revision 11 (Version 4.11) [Data set]. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H49C6VHW (GIBS layers `GPW_Population_Density_2000` to `_2020`; the sound layer Human presence.)
- Center For International Earth Science Information Network-CIESIN-Columbia University & NatureServe. (2015). Gridded Species Distribution: Global Mammal Richness Grids, 2015 Release (Version 2015.00) [Data set]. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4N014G5 (GIBS layer `Mammal_Richness_Grids_All_Species_2013`; the sound layer Wildlife diversity. Input: IUCN Red List species ranges, downloaded in April 2013.)
- NASA GIBS, layer `BlueMarble_ShadedRelief_Bathymetry` (Blue Marble Shaded Relief and Bathymetry, MODIS), WMTS tiles of the EPSG:4326 grid, https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/ (base map, used live, nothing is stored). The same acknowledgement applies, and the page shows it in a corner of the map:
  "We acknowledge the use of imagery provided by services from NASA's Global Imagery Browse Services (GIBS), part of NASA's Earth Science Data and Information System (ESDIS)."
- [Leaflet](https://leafletjs.com/) 1.9.4, BSD 2-Clause licence, copyright Volodymyr Agafonkin and CloudMade (`vendor/leaflet/`, with its licence file). Only used to draw the base map.
- No other libraries, fonts, images or sound files are used, and NASA GIBS is the only external service. No NASA logo is used.

## Data & image credits

All NASA pictures live in `data/nasa/`, and `data/nasa/SOURCES.json` lists every file with its original URL, download date, data date, SVS ID, dataset name, the credit NASA asks for and the people credited. The "About & sources" dialog of the page is built from that file. `scripts/fetch_nasa_data.py` (Python standard library only) downloads the files again and updates the size, checksum and date in `SOURCES.json`. The pictures are copies kept in this project because NASA's server does not send CORS headers, so a page cannot read the pixels of a picture loaded straight from it.

- **NASA's Scientific Visualization Studio**, *Sea Surface Temperature (SST) Anomaly - Near Real Time*, SVS #5176, https://svs.gsfc.nasa.gov/5176/
  - Visualizer: Kel Elkins (USRA). Scientist: Atousa Saberi (NASA/GSFC). Technical support: Laurence Schuler and Ian Jones (ADNET Systems, Inc.).
  - Underlying data: JPL MUR SST analysis (Multi-scale Ultra-high Resolution Sea Surface Temperature), PO.DAAC; SVS dataset ID 845.
  - In this project (2 files): the map picture of 11 November 2026 and NASA's colour bar (both as downloaded on 14 November 2026).
- **NASA GIBS**, *Sea Surface Temperature Anomalies (L4, MUR25, GHRSST)*, https://www.earthdata.nasa.gov/engage/open-data-services-software/earthdata-developer-portal/gibs-api
  - Underlying data: JPL MUR25 SST analysis (MUR25-JPL-L4-GLOB-v04.2), PO.DAAC.
  - In this project (26 files in `data/nasa/sst-yearly/`): 24 pictures (13 November 2002 to 2025), the Today picture, and the colour table.
- **NASA SEDAC / CIESIN, Columbia University**, *Gridded Population of the World, Version 4 (GPWv4): Population Density, Revision 11*, https://doi.org/10.7927/H49C6VHW, through NASA GIBS. In this project: 5 pictures (2000, 2005, 2010, 2015, 2020) and the colour table in `data/nasa/gpw/`.
  - Please cite: Center for International Earth Science Information Network (CIESIN), Columbia University. (2017). Gridded Population of the World, Version 4 (GPWv4): Population Density, Revision 11 (Version 4.11) [Data set]. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H49C6VHW
- **NASA SEDAC / CIESIN, Columbia University and NatureServe**, *Gridded Species Distribution: Global Mammal Richness Grids, 2015 Release*, https://doi.org/10.7927/H4N014G5, through NASA GIBS (input: IUCN Red List species ranges, April 2013). In this project: 1 picture and the colour table in `data/nasa/mammals/`.
  - Please cite: Center For International Earth Science Information Network-CIESIN-Columbia University & NatureServe. (2015). Gridded Species Distribution: Global Mammal Richness Grids, 2015 Release (Version 2015.00) [Data set]. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4N014G5
- **Natural Earth** (public domain), *Admin 0 - Countries*, 1:50m, https://www.naturalearthdata.com/ (used for the country names only; a reduced copy is inside `index.html`).
## AI use

The code in this project was written with the help of an AI assistant (Claude, by Anthropic), working from the team's instructions. The project idea, the sound design (what each kind of place should sound like and feel like) and the decisions about the interface were made by the team.

## License

The code in this project is by the Soundscape Earth team and is released under the [MIT License](LICENSE).

NASA imagery and data in `data/nasa/` are not covered by this license. They are provided by NASA and used under [NASA's Media Usage Guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/). NASA does not endorse this project.
