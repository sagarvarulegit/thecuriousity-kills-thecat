"""
Builds and formats the comprehensive documentation for Episode 2:
1. episode-02-the-inferno-in-the-trenches.md (Complete 80 Micro-Beat Bible & Pacing Blueprint)
2. episode-02-youtube-publish-kit.md (High-CTR Titles, Description, Tags <500 chars, Pinned Comment, Thumbnail Concepts)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EPISODES_DIR = BASE_DIR / "episodes"
EPISODES_DIR.mkdir(parents=True, exist_ok=True)

EP02_STORYBOARD_FILE = EPISODES_DIR / "episode-02-the-inferno-in-the-trenches.md"
EP02_PUBLISH_KIT_FILE = EPISODES_DIR / "episode-02-youtube-publish-kit.md"

EP02_STORYBOARD_CONTENT = """# Episode 2: The Inferno in the Trenches
### *Excavating 400,000 Tons: Fire-Setting, Thermal Shock & The Three Perimeter Trenches*
**Target Duration**: 07:45 – 08:15 mins (465 – 495 seconds)  
**Total Production Micro-Beats**: 80 Granular Cinematic Cuts (Average 5.8s – 6.2s per cut)  
**Retention Target**: 55%+ Average Percentage Viewed (YouTube Mid-roll Monetization Optimized)  
**Format**: 16:9 1080p Full HD Master (Series) | 9:16 Vertical (2x Companion Funnel Shorts)

---

## The Video Pacing & Cut Architecture

Holding any single visual shot longer than 6 seconds causes catastrophic viewer drop-off on YouTube. Episode 2 maintains the rigorous **5.5 to 6.5 second average cut pace**:

```
+---------------------------------------------------------------------------------------------------------+
|                                    8-MINUTE RETENTION PACING MATRIX                                     |
+-------------------+---------------------+----------------+-----------------------+----------------------+
| Act / Sequence    | Duration (Seconds)  | Micro-Beats    | Avg Cut Speed         | Narrative Energy     |
+-------------------+---------------------+----------------+-----------------------+----------------------+
| Act 1: The Mobil  | 00:00 - 01:05 (65s) | Beats 01 to 10 | 6.5s (Epic, Ominous)  | Vast Army, Scale     |
| Act 2: Trenches   | 01:05 - 02:15 (70s) | Beats 11 to 21 | 6.3s (Architectural)  | Geometry, U-Trench   |
| Act 3: Iron Limit | 02:15 - 03:15 (60s) | Beats 22 to 31 | 6.0s (Visceral/Crisis)| Tool Destruction     |
| Act 4: Agni-Karma | 03:15 - 04:25 (70s) | Beats 32 to 42 | 6.3s (Mysterious/Heat)| Fire-Setting Science |
| Act 5: Shock Flash| 04:25 - 05:35 (70s) | Beats 43 to 53 | 6.3s (Violent/Explosiv| Steam, Fracturing    |
| Act 6: Excavation | 05:35 - 06:35 (60s) | Beats 54 to 63 | 6.0s (Kinetic Energy) | Levers, Sledges      |
| Act 7: 100k Tons  | 06:35 - 07:35 (60s) | Beats 64 to 72 | 6.6s (Engineering)    | Gravity Chutes       |
| Act 8: Monolith   | 07:35 - 08:15 (40s) | Beats 73 to 80 | 5.0s (Accelerating)   | The Island Emerges   |
+-------------------+---------------------+----------------+-----------------------+----------------------+
| TOTALS            | ~490 Seconds        | 80 Shots       | ~6.1s Average / Cut   | High YouTube Binge   |
+-------------------+---------------------+----------------+-----------------------+----------------------+
```

---

## The Smart Production Pyramid (API Budget Optimization)

**80 Micro-beats does NOT mean 80 separate AI image or video calls.**
To maintain strict cost control and zero credit waste ($3.50 – $5.00 total API budget):
* **Strict 1080p Resolution Constraint (No 4K)**: All generations and preview outputs target standard 1080p Full HD (`1920x1080`).
* **Generate only 22 Master Hero Images**:
  * **8 Video Targets** explicitly tagged `_GENERATE_VIDEO.jpg` (cold strike sparks, bonfires roaring, cold water splashing glowing stone with steam explosion, crowbars prying rock slabs, sledgehammers pulverizing stone, gravity timber chutes, elephant haulage, summit cliffhanger) isolated in `assets/episode-02/google_flow_input_images/`.
  * **14 Still Targets** explicitly tagged `_PAN_ZOOM.jpg` animated via 1-to-3 multi-cam Ken Burns pan/zoom/tilt crops.
* **2 Vertical Shorts Images (9:16)**: Dedicated visual prompts for the two funnel Shorts.
* **1 Master YouTube Thumbnail**: Designed for maximum CTR with high-contrast color grading.

---

### Master Image Generation Batch Sheet (Only 22 Images to Generate)

| # | Master Image Filename | Prompt Focus | Satisfies Beats | Multi-Cam Motion | Google Flow Video? |
| :- | :--- | :--- | :--- | :--- | :--- |
| **IMG-01** | `ep02_01_trench_sunrise_PAN_ZOOM.jpg` | Dawn over Charanandri ridge, red chalk lines | Beats 01, 02, 09 | Wide panoramic sunrise $\\rightarrow$ punch-in on ridge | Static Ken Burns |
| **IMG-02** | `ep02_02_surveyor_plummet_PAN_ZOOM.jpg`| Kokasa inspecting water leveling troughs | Beats 03, 04 | Medium architects $\\rightarrow$ 160% punch-in on trough | Static Ken Burns |
| **IMG-03** | `ep02_03_quarrymen_army_PAN_ZOOM.jpg` | Thousands of quarrymen with sledges | Beats 05, 06, 08 | Wide army panorama $\\rightarrow$ punch-in on faces | Static Ken Burns |
| **IMG-04** | `ep02_04_chisel_fracture_test_GENERATE_VIDEO.jpg` | Steel punch striking cold unheated basalt | Beats 07, 10, 22, 23 | Sledge strike, metallic spark & vibration | **YES (Cold strike sparks)** |
| **IMG-05** | `ep02_05_dulled_iron_pile_PAN_ZOOM.jpg` | Heaps of blunted, mushroomed chisel tips | Beats 24, 25, 26, 27 | Wide metal heap $\\rightarrow$ macro ruined chisel head | Static Ken Burns |
| **IMG-06** | `ep02_06_hardwood_convoys_PAN_ZOOM.jpg` | Bullock cart convoys hauling dried Acacia logs| Beats 28, 29, 30, 31, 32 | Wide convoy climbing ridge $\\rightarrow$ cart wheels | Static Ken Burns |
| **IMG-07** | `ep02_07_stacking_pyres_PAN_ZOOM.jpg` | Workers stacking dry timber pyres in trench | Beats 33, 34, 35 | Trench perspective $\\rightarrow$ stacking logs | Static Ken Burns |
| **IMG-08** | `ep02_08_bonfire_ignited_GENERATE_VIDEO.jpg`| Roaring 600°C bonfire flames in trench | Beats 36, 37, 38 | Blazing orange fire, roaring flame sheets | **YES (Roaring fire/sparks)** |
| **IMG-09** | `ep02_09_superheated_bedrock_PAN_ZOOM.jpg`| Glowing cherry-red basalt face with heat haze| Beats 39, 40, 41, 42 | Medium glowing face $\\rightarrow$ extreme heat shimmer | Static Ken Burns |
| **IMG-10** | `ep02_10_water_carriers_rushing_GENERATE_VIDEO.jpg` | Double line of water carriers with clay pots | Beats 43, 44, 45 | Wide running line $\\rightarrow$ close-up clay pots | **YES (Water carriers)** |
| **IMG-11** | `ep02_11_thermal_shock_explosion_GENERATE_VIDEO.jpg`| Cold water doused on red basalt, steam blast| Beats 46, 47, 48 | Massive violent white steam explosion | **YES (Steam explosion)** |
| **IMG-12** | `ep02_12_microfracture_cracks_PAN_ZOOM.jpg`| Macro spiderweb fractures splitting basalt | Beats 49, 50, 51, 52 | Extreme macro fracturing stone $\\rightarrow$ zoom-in | Static Ken Burns |
| **IMG-13** | `ep02_13_crowbar_levering_GENERATE_VIDEO.jpg`| Workers prying loose 2-ton basalt plate | Beats 53, 54, 55 | Crowbars levering, rock slab crashing | **YES (Prying rock slab)** |
| **IMG-14** | `ep02_14_sledgehammer_crush_GENERATE_VIDEO.jpg`| Heavy sledge crushing weakened rock crust | Beats 56, 57, 58 | Sledge impact, explosive dust & rock blast | **YES (Sledge impact)** |
| **IMG-15** | `ep02_15_three_trenches_depth_PAN_ZOOM.jpg` | 3D aerial isometric cutaway of U-trench | Beats 11, 12, 13, 14, 59 | Wide U-trench cutaway $\\rightarrow$ schematic zoom | Motion Graphics / Pan |
| **IMG-16** | `ep02_16_timber_gravity_chute_GENERATE_VIDEO.jpg`| Boulders sliding down greased timber chute | Beats 64, 65, 66 | Boulders hurtling down timber slide | **YES (Rock slide & dust)** |
| **IMG-17** | `ep02_17_elephant_haulage_PAN_ZOOM.jpg` | War elephants dragging massive stone sledges | Beats 67, 68, 69 | Wide haulage staging plain $\\rightarrow$ elephant legs | Static Ken Burns |
| **IMG-18** | `ep02_18_dust_and_sweat_PAN_ZOOM.jpg` | Close-up weathered quarryman covered in dust | Beats 70, 71, 72 | Hero portrait, dust-streaked sweat, determination | Static Ken Burns |
| **IMG-19** | `ep02_19_depth_marker_checking_PAN_ZOOM.jpg` | Surveyor checking plumb bob along 25m wall | Beats 15, 16, 17, 60 | Vertical sheer rock wall $\\rightarrow$ weighted string | Static Ken Burns |
| **IMG-20** | `ep02_20_the_back_scarp_wall_PAN_ZOOM.jpg`| 33-meter vertical back scarp cliff face | Beats 18, 19, 20, 21, 61 | Massive basalt precipice towering over trench | Static Ken Burns |
| **IMG-21** | `ep02_21_isolated_monolith_dusk_PAN_ZOOM.jpg`| 33m isolated central monolith island at dusk | Beats 62, 63, 73, 74, 75 | Golden sunset on towering free-standing block | Static Ken Burns |
| **IMG-22** | `ep02_22_cliffhanger_spire_summit_GENERATE_VIDEO.jpg`| Kokasa at top of isolated block staring at sky| Beats 76, 77, 78, 79, 80 | Wind blowing robes, camera orbiting summit | **YES (Summit wind & sky)** |

---

## Universal Style Anchor (Consistent Historical Realism)

All visual generations use the pinned photorealistic documentary anchor:
> `hyper-realistic 8k historical documentary photograph, 756 CE Rashtrakuta India, cinematic lighting, volcanic tholeiitic basalt texture, authentic ancient metallurgy and tools, photorealistic chiaroscuro, Hasselblad 50mm f/2.8 lens, 1080p Full HD --ar 16:9`

---

## Complete 80 Micro-Beat Storyboard & Visual Prompt Bible

### ACT I: THE SOUND OF WAR IN STONE (00:00 – 01:05)

#### **Beat 01 (00:00 - 00:07)**
* **Shot**: Extreme Wide Establishing Shot — Dawn over Charanandri Ridge (Cut A: Full Wide).
* **Narration**: *"Before you can carve a cathedral out of a mountain, you must perform an act of sheer violence against the earth itself."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Epic wide-angle dawn vista of Charanandri ridge at Ellora, western India, 756 CE. Golden morning sunlight piercing misty Deccan valley. Red cinnabar chalk lines glowing on flat dark basalt summit. Thousands of stonecutters assembling along the escarpment in historical Rashtrakuta attire. Cinematic atmospheric depth, authentic ancient Indian geology, 8k`
* **Motion Prompt**: `Slow panoramic pan right across rugged basalt cliffs as dawn mist lifts from Deccan plain.`
* **SFX**: Deep low orchestral war drum pulse; cold mountain wind whispering across stone.

#### **Beat 02 (00:07 - 00:14)**
* **Shot**: Medium Low-Angle Tilt — The Red Cinnabar Baseline (Cut B: 160% Punch-in).
* **Narration**: *"In the winter of 756 CE, ten thousand stonecutters climbed the Charanandri ridge."*
* **Visual Prompt**: `ep02_01_trench_sunrise_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Tilt up slowly from glowing red mineral chalk line on dark basalt to silhouetted quarrymen holding iron tools.`
* **SFX**: Rhythmic crunch of thousands of bare feet ascending gravel slopes.

#### **Beat 03 (00:14 - 00:20)**
* **Shot**: Medium Close-up — Master Architect Kokasa Inspecting Water Level (Cut A: Medium).
* **Narration**: *"They did not begin by carving gods."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Ancient Indian master architect Kokasa kneeling on dark volcanic basalt, inspecting a stone groove filled with water for leveling. A senior surveyor holds a lead plumb bob on a twisted cord over a sheer rock edge. Dawn light reflecting in water trough, extreme tactile texture of basalt stone and weathered hands, 8k`
* **Motion Prompt**: `Slow, deliberate push-in on Kokasa's weathered fingers testing surface tension in stone water trough.`
* **SFX**: Gentle splash of water ripples in stone channel; distant camp murmur.

#### **Beat 04 (00:20 - 00:27)**
* **Shot**: Close-Up Macro — Plumb Bob & Water Groove (Cut B: 180% Crop).
* **Narration**: *"They began by cutting three colossal trenches straight down into the crust of India."*
* **Visual Prompt**: `ep02_02_surveyor_plummet_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Macro focus pull from lead plumb weight swaying over cliff rim to Kokasa's intense, focused eyes.`
* **SFX**: Ominous metallic chime; taut hemp string vibrating in wind.

#### **Beat 05 (00:27 - 00:33)**
* **Shot**: Wide Panoramic Ranks of Quarrymen (Cut A: Wide).
* **Narration**: *"Two side trenches eighty-four meters long."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Panoramic wide shot of hundreds of muscular ancient Indian quarrymen standing in disciplined ranks along the mountain summit. They hold iron sledgehammers and steel punch chisels over shoulders. Morning mist rising from Deccan plain below, golden sun flare, epic historical scale, photorealistic, 8k`
* **Motion Prompt**: `Fast lateral tracking shot past disciplined ranks of stonecutters standing along perimeter guidelines.`
* **SFX**: Clatter of heavy bronze and iron tools resting against rock.

#### **Beat 06 (00:33 - 00:40)**
* **Shot**: Medium Tracking — Sledges and Chisels on Shoulders (Cut B: 150% Punch-in).
* **Narration**: *"One back scarp trench forty-seven meters wide."*
* **Visual Prompt**: `ep02_03_quarrymen_army_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Tracking profile alongside workers marching forward with massive iron sledgehammers.`
* **SFX**: Deep synchronized exhalation of marching laborers; horn signal blast.

#### **Beat 07 (00:40 - 00:47)**
* **Shot**: Action Close-up Video — Steel Chisel Tip on Bedrock (Video Target).
* **Narration**: *"Together, they formed a massive U-shaped chasm thirty-three meters deep."*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. Macro action close-up of a pointed high-carbon steel punch chisel being struck by a thirty-pound basalt hammer against cold, unyielding black basalt bedrock. Bright golden sparks flying on impact, steel tip visibly resisting without penetrating the ultra-dense volcanic stone. Photorealistic high-speed capture, 8k`
* **Motion Prompt**: `High-speed 120fps video of 30lb sledge crashing into steel punch; shower of brilliant orange sparks.`
* **SFX**: Piercing metallic CLANG; bone-jarring sonic crack.

#### **Beat 08 (00:47 - 00:53)**
* **Shot**: Low Angle — Ranks of Workers Staring into Chasm (Cut C: Pan/Scan).
* **Narration**: *"Inside that chasm sat four hundred thousand tons of suffocating volcanic basalt."*
* **Visual Prompt**: `ep02_03_quarrymen_army_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Dramatic low-angle pan across resolute faces caked in mineral dust gazing into the excavation pit.`
* **SFX**: Low brass horn drone building in tension.

#### **Beat 09 (00:53 - 00:59)**
* **Shot**: Drone Pull-Back — The Mountain Ridge at Dawn (Cut C: Wide Pan).
* **Narration**: *"To free the temple, every single pebble had to be excavated by hand."*
* **Visual Prompt**: `ep02_01_trench_sunrise_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `High altitude drone pull-back revealing the immense ridge dwarfs the tiny human workers.`
* **SFX**: Sweeping orchestral string swell; wind rushing past mountain peaks.

#### **Beat 10 (00:59 - 01:05)**
* **Shot**: Extreme Macro — Basalt Bedrock Surface (Cut B: 200% Punch-in).
* **Narration**: *"And their enemy was not time. Their enemy was the hardest rock on planet Earth."*
* **Visual Prompt**: `ep02_04_chisel_fracture_test_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Slow digital zoom into dense crystalline grain of black basalt stone.`
* **SFX**: Deep bass sub-drop; sudden silence before Act II.

---

### ACT II: THE GEOMETRY OF THE THREE TRENCHES (01:05 – 02:15)

#### **Beat 11 (01:05 - 01:11)**
* **Shot**: Aerial Isometric 3D Cutaway — The U-Trench Scheme (Cut A: Full Diagram).
* **Narration**: *"Kokasa’s master plan demanded geometric perfection."*
* **Visual Prompt**: `Cinematic 16:9 1080p conceptual still. Breathtaking aerial isometric view of Ellora Cave 16 excavation site showing the vast U-shaped trench reaching fifteen meters deep into the Charanandri ridge. The central uncarved block of mountain stands isolated on three sides. Scale figures working like ants in the trench bottoms. Architectural clarity, 8k`
* **Motion Prompt**: `Smooth 3D orbit around isometric cutaway diagram revealing the three perimeter trenches.`
* **SFX**: Architectural drafting pencil scratch; crisp wooden compass click.

#### **Beat 12 (01:11 - 01:18)**
* **Shot**: 3D Schematic Angle — Trench Wall Incline (Cut B: 150% Punch-in).
* **Narration**: *"If the trench walls leaned inward by even a fraction of a degree, the working space below would become a claustrophobic death trap."*
* **Visual Prompt**: `ep02_15_three_trenches_depth_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Animated glowing red guideline illustrating danger of inward slope narrowing to a bottleneck.`
* **SFX**: Tense warning cello drone; creak of shifting rock.

#### **Beat 13 (01:18 - 01:24)**
* **Shot**: 3D Schematic Angle — Trench Wall Outward Error (Cut C: Pan/Scan).
* **Narration**: *"If they leaned outward, they would carve away rock needed for the temple’s sacred outer courtyards."*
* **Visual Prompt**: `ep02_15_three_trenches_depth_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Animated blue guideline showing outward error slicing through virtual boundary of temple courtyard.`
* **SFX**: Sharp digital whoosh; glass-like ping.

#### **Beat 14 (01:24 - 01:31)**
* **Shot**: Isometric Trench Depth Metric Callout — 33 Meters Down (Cut D: Vertical Pan).
* **Narration**: *"To keep the cuts perfectly vertical thirty-three meters down, the Sutradharas used lead plumb-bobs and water leveling troughs."*
* **Visual Prompt**: `ep02_15_three_trenches_depth_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Animated vertical depth meter counting downward: 0m ... 10m ... 20m ... 33m.`
* **SFX**: High-tech caliper click; fluid water trickle sound.

#### **Beat 15 (01:31 - 01:37)**
* **Shot**: Low Angle Looking Up Sheer Trench Wall (Cut A: Low Angle).
* **Narration**: *"Every morning, water was poured into stone grooves etched along the summit rim."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Low-angle view looking straight up a smooth, twenty-five-meter sheer vertical trench wall. A surveyor at the summit leans over to inspect a weighted hemp plumb line hanging perfectly flush against the rock face. Golden afternoon light grazing tool marks, 8k`
* **Motion Prompt**: `Slow tilt upward along thirty meters of sheer black basalt cliff to silhouette of surveyor on summit.`
* **SFX**: Distant water splashing into stone reservoir; echo bouncing between rock walls.

#### **Beat 16 (01:37 - 01:43)**
* **Shot**: Macro Plumb Bob Cord Against Basalt Face (Cut B: 180% Crop).
* **Narration**: *"If the water drifted to the left, the cut was corrected."*
* **Visual Prompt**: `ep02_19_depth_marker_checking_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Extreme macro focus on taut braided hemp string vibrating 2 millimeters from stone face.`
* **SFX**: Sharp wooden chalk click; subtle wind whistle.

#### **Beat 17 (01:43 - 01:50)**
* **Shot**: Medium Close-up — Surveyor Checking Alignment (Cut C: Pan/Scan).
* **Narration**: *"Millimeter by millimeter, the plumblines ensured the abyss descended true."*
* **Visual Prompt**: `ep02_19_depth_marker_checking_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Horizontal pan across surveyor's squinting eye, measuring stick held parallel to plumb cord.`
* **SFX**: Soft scrape of bone measuring rod against basalt.

#### **Beat 18 (01:50 - 01:57)**
* **Shot**: Monumental Wide Shot — The 33-Meter Back Scarp (Cut A: Monumental Wide).
* **Narration**: *"Behind the temple site rose the sheer, terrifying back scarp: a single vertical wall of solid basalt taller than a ten-story building."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Monumental wide shot of the monolithic back scarp of Kailasa: A staggering 33-meter (108-foot) vertical wall of solid basalt towering over the excavated trench floor. Dramatic scale with tiny human workers at the base, emphasizing megalithic volume of stone cleared, 8k`
* **Motion Prompt**: `Slow, sweeping pedestal crane shot rising from trench floor up the towering vertical basalt monolith.`
* **SFX**: Resonant orchestral brass fanfare; monumental acoustic reverb.

#### **Beat 19 (01:57 - 02:03)**
* **Shot**: Low-Angle Upward Pan — Towering Dark Cliff (Cut B: 160% Punch-in).
* **Narration**: *"A monolithic precipice carved cleanly out of the mountain crest."*
* **Visual Prompt**: `ep02_20_the_back_scarp_wall_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Rapid vertical tilt looking straight into the dizzying height of the sheer rock wall.`
* **SFX**: Gust of mountain wind echoing against stone cliff face.

#### **Beat 20 (02:03 - 02:09)**
* **Shot**: Medium Detail — Chisel Grooves on Scarp Face (Cut C: Pan/Scan).
* **Narration**: *"From the valley below, it looked as though the empire had declared war on the mountain."*
* **Visual Prompt**: `ep02_20_the_back_scarp_wall_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Lateral slide along rhythmic vertical pick grooves scored into basalt face.`
* **SFX**: Distant chorus of thousands of iron tools clinking in syncopated rhythm.

#### **Beat 21 (02:09 - 02:15)**
* **Shot**: Wide Valley Perspective — The Excavation Scar (Cut D: Panoramic).
* **Narration**: *"A titanic wound opened in the earth to birth a monument of stone."*
* **Visual Prompt**: `ep02_20_the_back_scarp_wall_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Extreme wide pull back revealing the vast square trench carved into the green Deccan hillside.`
* **SFX**: Deep ominous drone fade-out.

---

### ACT III: THE PHYSICAL LIMIT OF IRON & STEEL (02:15 – 03:15)

#### **Beat 22 (02:15 - 02:21)**
* **Shot**: Macro Action Video — Sledgehammer Striking Cold Basalt (Video Target).
* **Narration**: *"The first week of excavation was a catastrophe."*
* **Visual Prompt**: `ep02_04_chisel_fracture_test_GENERATE_VIDEO.jpg`
* **Motion Prompt**: `High-speed 120fps video of sledgehammer impact on cold stone; zero penetration, shockwave ripples.`
* **SFX**: Harsh, jarring metallic strike followed by dull thud.

#### **Beat 23 (02:21 - 02:27)**
* **Shot**: Extreme Close-up — Chisel Tip Bouncing Off Bedrock (Cut D: Macro Action).
* **Narration**: *"The stone of Ellora is tholeiitic basalt: cooled prehistoric lava packed with dense pyroxene and plagioclase crystals."*
* **Visual Prompt**: `ep02_04_chisel_fracture_test_GENERATE_VIDEO.jpg (Cut D)`
* **Motion Prompt**: `Super-macro shot of iron chisel tip rebounding off crystalline basalt surface.`
* **SFX**: High-pitched ringing chime (*pinggg*); sound of steel bending.

#### **Beat 24 (02:27 - 02:33)**
* **Shot**: Motion Graphic Callout — 140 MPa Compressive Strength (Cut A: Graphic Overlay).
* **Narration**: *"Its compressive strength exceeds one hundred and forty megapascals."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Grim close-up of a large heap of ruined, blunted, and mushroomed iron chisel heads piled next to an ancient charcoal forge. In the background, blacksmiths hammer glowing metal under bamboo thatch awnings. Smoke, embers, intense contrast, historical realism, 8k`
* **Motion Prompt**: `Animated HUD graphic: "140 MPa Compressive Strength — 2x Modern Concrete" stamped over stone.`
* **SFX**: Heavy electronic data thud; low bass pulse.

#### **Beat 25 (02:33 - 02:39)**
* **Shot**: Medium Action — Quarryman Straining with Sledge (Cut B: 150% Punch-in).
* **Narration**: *"When a quarryman swung a thirty-pound sledgehammer against the cold bedrock, the steel chisel did not bite."*
* **Visual Prompt**: `ep02_05_dulled_iron_pile_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Slow motion push-in on strained neck muscles and clenched jaw of quarryman.`
* **SFX**: Heavy grunt of muscular exertion; dull bounce of hammer.

#### **Beat 26 (02:39 - 02:45)**
* **Shot**: Close-up — Shockwave Vibration in Striker's Arms (Cut C: Pan/Scan).
* **Narration**: *"It bounced."*
* **Visual Prompt**: `ep02_05_dulled_iron_pile_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Subtle high-speed shudder effect on striker's wrists and forearm tendons.`
* **SFX**: Sudden complete audio silence except for a dull reverberating ringing.

#### **Beat 27 (02:45 - 02:51)**
* **Shot**: Macro — Mushroomed and Blunted Chisel Tip (Cut D: Extreme Macro).
* **Narration**: *"Shockwaves reverberated through the bones of the strikers’ arms, shattering wrists and blunting steel tips in minutes."*
* **Visual Prompt**: `ep02_05_dulled_iron_pile_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Macro camera orbit around deformed, flattened, mushroomed steel chisel head.`
* **SFX**: Sickening metallic crunch; groans of injured workers.

#### **Beat 28 (02:51 - 02:57)**
* **Shot**: Wide Shot — Massive Scrap Pile of Ruined Iron Tools (Cut A: Full Wide).
* **Narration**: *"By midday, piles of ruined, mushroomed iron chisels littered the camp."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Wide shot of an endless convoy of heavy wooden bullock carts hauling thick logs of dark Acacia and Teak hardwood up the steep rocky slope of the Charanandri ridge. Dust clouds kicked up by wooden wheels, harsh Deccan sunlight, monumental supply line logistics, 8k`
* **Motion Prompt**: `Slow tilt down from sweltering blacksmith smoke to heaps of mangled black iron tools.`
* **SFX**: Clattering metal heap; hiss of red-hot iron dumped in water.

#### **Beat 29 (02:57 - 03:03)**
* **Shot**: Medium — Exhausted Blacksmiths at Sweltering Forges (Cut B: 160% Punch-in).
* **Narration**: *"At this rate, simply excavating the three perimeter trenches would take forty years."*
* **Visual Prompt**: `ep02_06_hardwood_convoys_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Tracking shot past sweat-drenched smiths frantically reheating dull chisel points on anvils.`
* **SFX**: Hissing steam, bellows wheezing, fast anvil tapping.

#### **Beat 30 (03:03 - 03:09)**
* **Shot**: Close-up — Kokasa's Troubled, Calculating Gaze (Cut C: Portrait).
* **Narration**: *"The queen had only days. Kokasa knew that iron alone could never defeat the mountain."*
* **Visual Prompt**: `ep02_06_hardwood_convoys_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Slow push-in on Kokasa’s eyes narrowing as he studies the unyielding black rock shelf.`
* **SFX**: Tension-building violin tremolo; slow dramatic heartbeat.

#### **Beat 31 (03:09 - 03:15)**
* **Shot**: Silhouette of Sun Blazing Over Mountain Ridge (Cut D: Skyward Tilt).
* **Narration**: *"He needed a weapon hotter than the sun."*
* **Visual Prompt**: `ep02_06_hardwood_convoys_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Tilt up to blinding midday Deccan sun flaring directly over the rugged cliff crest.`
* **SFX**: Sudden orchestral crescendo; deep whoosh of rising heat.

---

### ACT IV: THE ANCIENT SCIENCE OF THERMAL SHOCK (*AGNI-KARMA*) (03:15 – 04:25)

#### **Beat 32 (03:15 - 03:21)**
* **Shot**: Wide Convoy — Heavy Bullock Carts Hauling Hardwood (Cut E: Wide Landscape).
* **Narration**: *"Kokasa turned to an ancient technique recorded in the Artha-Shastra and the Shilpa Shastras: Agni-Karma, the art of fire-setting."*
* **Visual Prompt**: `ep02_06_hardwood_convoys_PAN_ZOOM.jpg (Cut E)`
* **Motion Prompt**: `Slow lateral pan following endless line of bullock carts laden with timber logs winding up ridge.`
* **SFX**: Creaking wooden cart axles; bellowing of draft oxen; whip cracks.

#### **Beat 33 (03:21 - 03:27)**
* **Shot**: Medium Shot — Unloading Logs of Acacia and Khair Hardwood (Cut A: Medium).
* **Narration**: *"Convoys of bullock carts hauled thousands of tons of dense hardwood from the surrounding Deccan forests: Acacia, Khair, and ancient Teak."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Dramatic perspective looking down into a freshly cut five-meter deep trench in volcanic rock. Dozens of laborers carefully stacking dry timber logs and cow dung cakes tightly against the sheer vertical basalt rock face. Dust, dramatic shadows, authentic ancient quarry work, 8k`
* **Motion Prompt**: `Tracking shot of workers hoisting heavy dark acacia logs off carts and carrying them to the trench rim.`
* **SFX**: Heavy thud of hardwood logs tumbling to ground; shouted commands.

#### **Beat 34 (03:27 - 03:34)**
* **Shot**: Trench Perspective — Stacking Timber Pyres Against Bedrock (Cut B: 150% Punch-in).
* **Narration**: *"Quarrymen stacked the timber tightly against the basalt face in the trench, packing it with dried cow dung and sesame oil."*
* **Visual Prompt**: `ep02_07_stacking_pyres_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Low-angle tracking looking down the trench as laborers stack crisscrossed wooden pyres flush against stone.`
* **SFX**: Rustling dry straw and timber; slapping of dung fuel cakes.

#### **Beat 35 (03:34 - 03:40)**
* **Shot**: Close-up — Pouring Jars of Combustible Oil Over Pyres (Cut C: Pan/Scan).
* **Narration**: *"Every square meter of the rock was primed for combustion."*
* **Visual Prompt**: `ep02_07_stacking_pyres_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Close-up of golden sesame oil pouring in thick stream over dried firewood logs.`
* **SFX**: Rich glug of oil pouring from earthen vessel; crackle of dry kindling.

#### **Beat 36 (03:40 - 03:47)**
* **Shot**: Action Wide Video — Torches Hurled into Trench at Sunset (Video Target).
* **Narration**: *"At sunset, they set the trench ablaze."*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. Terrifying and spectacular night scene inside an ancient rock-cut trench. Roaring 600-degree Celsius bonfires blazing furiously against a massive vertical black basalt cliff wall. Intense orange and yellow flames leaping twenty feet high, swirling sparks, glowing embers, photorealistic fire dynamics, 8k`
* **Motion Prompt**: `Flaming torch arches through twilight air and lands on oil-soaked pyre; immediate wall of fire ignites.`
* **SFX**: Sudden explosive WHOOSH of ignition; roar of spreading flames.

#### **Beat 37 (03:47 - 03:53)**
* **Shot**: Roaring Fire Video — Sixty-Foot Flames Leaping Into Night Sky (Cut B: Medium Video).
* **Narration**: *"An inferno roared along the perimeter. Flames reached sixty feet into the night sky, turning the mountain ridge into a blazing volcanic ring."*
* **Visual Prompt**: `ep02_08_bonfire_ignited_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Camera dollies past towering sheets of yellow-orange flame roaring inside the rock-cut channel.`
* **SFX**: Raging, deafening bonfire rumble; snapping of burning acacia branches.

#### **Beat 38 (03:53 - 04:00)**
* **Shot**: Swirling Sparks and Embers Rising Over Charanandri (Cut C: Macro Embers).
* **Narration**: *"The heat was felt miles away across the plains."*
* **Visual Prompt**: `ep02_08_bonfire_ignited_GENERATE_VIDEO.jpg (Cut C)`
* **Motion Prompt**: `Upward pan following thousands of glowing red sparks swirling up into star-filled midnight sky.`
* **SFX**: Crackle of sparks; distant rumble of mountain winds.

#### **Beat 39 (04:00 - 04:06)**
* **Shot**: Medium — Glowing 600°C Bedrock Behind Dying Embers (Cut A: Medium).
* **Narration**: *"The basalt absorbed the terrifying heat. Its internal temperature soared past six hundred degrees Celsius."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Macro view of basalt bedrock glowing dull cherry-red through dying charcoal embers at extreme 600°C temperature. Intense heat distortion shimmering in the air, deep thermal stress visible in the mineral surface of the volcanic stone. Chiaroscuro lighting, 8k`
* **Motion Prompt**: `Slow forward push-in through dying embers toward the cherry-red radiant glow of the basalt wall.`
* **SFX**: Low pulsating thermal drone; gentle hiss of smoldering coals.

#### **Beat 40 (04:06 - 04:12)**
* **Shot**: Heat Shimmer Distortion Over Cherry-Red Basalt Face (Cut B: 170% Punch-in).
* **Narration**: *"Inside the rock, individual mineral crystals began to expand at violently different rates."*
* **Visual Prompt**: `ep02_09_superheated_bedrock_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Warping heat distortion waves rippling across the frame as radiant infrared heat bakes the lens.`
* **SFX**: High-frequency thermal whine; microscopic snapping sounds.

#### **Beat 41 (04:12 - 04:19)**
* **Shot**: Scientific 3D Micro-Animation — Expanding Mineral Lattice (Cut C: Pan/Scan).
* **Narration**: *"Quartz, feldspar, and pyroxene pushed against one another, turning the solid mountain into a compressed bomb."*
* **Visual Prompt**: `ep02_09_superheated_bedrock_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `3D cross-section diagram showing mineral crystal grains swelling and shearing against each other.`
* **SFX**: Deep mechanical grinding sound; building tectonic groan.

#### **Beat 42 (04:19 - 04:25)**
* **Shot**: Close-up Glowing Stone Surface with Stressed Mineral Lattice (Cut D: Macro).
* **Narration**: *"The rock was superheated to the verge of catastrophic fracture."*
* **Visual Prompt**: `ep02_09_superheated_bedrock_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Macro static shot of glowing red stone surface trembling under internal pressure.`
* **SFX**: Tense silence; single sharp mineral ping.

---

### ACT V: QUENCHING THE MOUNTAIN: THE THERMAL EXPLOSION (04:25 – 05:35)

#### **Beat 43 (04:25 - 04:31)**
* **Shot**: Dramatic Silhouette — Kokasa Raising Hand on Trench Rim (Cut A: Low Angle).
* **Narration**: *"Then came the flash."*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. Dynamic medium tracking shot of a continuous human chain of Indian laborers rushing forward carrying unglazed terracotta water jars and leather water skins (mashak). Sweat glistening on skin, motion blur on splashing water droplets, night firelight illumination, 8k`
* **Motion Prompt**: `Low-angle silhouette of Kokasa silhouetted against glowing trench smoke, arm slashing downward in command.`
* **SFX**: Sharp, piercing conch shell war signal blast.

#### **Beat 44 (04:31 - 04:38)**
* **Shot**: Wide Tracking Video — Human Chain of 500 Water Carriers Rushing (Video Target).
* **Narration**: *"As the bedrock glowed a dull cherry-red, Kokasa gave the signal."*
* **Visual Prompt**: `ep02_10_water_carriers_rushing_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Fast tracking dolly beside line of 500 runners sprinting toward the fiery trench with water jars.`
* **SFX**: Roar of hundreds of sprinting footsteps; water sloshing violently in clay jars.

#### **Beat 45 (04:38 - 04:44)**
* **Shot**: Close-up — Terracotta Pots and Leather Mashak Skins Splashing (Cut C: Macro Splash).
* **Narration**: *"A human chain of five hundred water carriers rushed forward, carrying leather water skins and cold terracotta pots filled from the mountain spring."*
* **Visual Prompt**: `ep02_10_water_carriers_rushing_GENERATE_VIDEO.jpg (Cut C)`
* **Motion Prompt**: `Close-up slow-motion shot of water sloshing out of wide-mouthed clay pots, catching firelight highlights.`
* **SFX**: Rapid water splashing; shouts of runners: "Jai Shiva!"

#### **Beat 46 (04:44 - 04:51)**
* **Shot**: Explosive Action Video — Cold Water Smashing Glowing Basalt (Video Target).
* **Narration**: *"In a single synchronized motion, hundreds of gallons of ice-cold water struck the six-hundred-degree stone face."*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. Violent explosive impact of cold mountain spring water splashing against a glowing cherry-red 600°C basalt rock face. Massive sudden eruption of thick white steam, exploding thermal vapor, tiny spitting shards of fractured stone flying through the air. Cinematic high-speed explosion capture, 8k`
* **Motion Prompt**: `High-speed 120fps capture of wall of water hitting glowing cherry stone; violent boiling shockwave.`
* **SFX**: Violent, explosive STEAM DETONATION (*TSSSSSSSS-BOOOOM*).

#### **Beat 47 (04:51 - 04:57)**
* **Shot**: Massive Boiling White Steam Geyser Erupting in Trench (Cut B: Medium Steam).
* **Narration**: *"The reaction was deafening."*
* **Visual Prompt**: `ep02_11_thermal_shock_explosion_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Camera shakes violently as volcanic white steam billows upward, blanketing the entire trench.`
* **SFX**: Overwhelming roar of pressurized steam venting into the night air.

#### **Beat 48 (04:57 - 05:04)**
* **Shot**: Cloud of Vapor Swallowing the Camera and Trench Walls (Cut C: Engulfing Mist).
* **Narration**: *"A violent explosion of superheated white steam engulfed the trench."*
* **Visual Prompt**: `ep02_11_thermal_shock_explosion_GENERATE_VIDEO.jpg (Cut C)`
* **Motion Prompt**: `Thick blinding white mist rolls across camera lens, turning the world into a ghostlike whiteout.`
* **SFX**: Muffled rushing wind; hissing drops hitting superheated stone.

#### **Beat 49 (05:04 - 05:10)**
* **Shot**: Macro Crack Snap — Spiderweb Fissures Splitting Basalt (Cut A: Macro).
* **Narration**: *"The sudden, brutal drop in temperature caused the outer layer of basalt to contract violently while the interior remained molten hot."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Extreme macro photorealistic shot of freshly cooled black basalt rock showing a dense network of micro-fractures and spiderweb fissures snapping open across the surface. Steam whispering from cracks, crystalline mineral grain boundaries tearing apart under thermal contraction, 8k`
* **Motion Prompt**: `Macro shot zooming into basalt surface as sudden hairline cracks branch open in real-time.`
* **SFX**: Rapid, sharp acoustic snapping sounds like breaking porcelain plates.

#### **Beat 50 (05:10 - 05:16)**
* **Shot**: Extreme Close-up — Deep Fractures Running Along Mineral Boundaries (Cut B: 180% Crop).
* **Narration**: *"With deafening snaps like gunshot fire, the mountain gave up."*
* **Visual Prompt**: `ep02_12_microfracture_cracks_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Super-macro tracking along a 2-inch wide fracture tearing across basalt bedrock.`
* **SFX**: LOUD GUNSHOT CRACK (*CLACCKKKK!*); deep subterranean groan.

#### **Beat 51 (05:16 - 05:23)**
* **Shot**: Whisper of Steam Escaping From Fresh Deep Fissures (Cut C: Pan/Scan).
* **Narration**: *"Millions of micro-fractures tore through the rock, turning diamond-hard basalt into brittle, shattered crust."*
* **Visual Prompt**: `ep02_12_microfracture_cracks_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Delicate plumes of residual white steam curling up from jagged stone fissures.`
* **SFX**: Soft whispering hiss; cooling stone ticking sounds.

#### **Beat 52 (05:23 - 05:29)**
* **Shot**: Stone Crust Peeling Naturally from Bedrock (Cut D: Macro Tilt).
* **Narration**: *"Where steel chisels had shattered, water and fire had conquered."*
* **Visual Prompt**: `ep02_12_microfracture_cracks_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Slow tilt revealing a 4-inch thick sheet of basalt completely detached from the substrate.`
* **SFX**: Crumbling gravel rattle; triumphant low brass chord.

#### **Beat 53 (05:29 - 05:35)**
* **Shot**: Smoke Clearing Revealing Crumbled Trench Walls (Cut A: Wide).
* **Narration**: *"The impenetrable shield of Charanandri was broken."*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. Action shot of four muscular ancient Indian quarrymen ramming long forged-iron crowbars into deep thermal fissures in a sheer trench wall. With coordinated muscle strain, a massive two-ton slab of fractured basalt breaks free and crashes downward in a plume of stone dust, 8k`
* **Motion Prompt**: `Mist parts to reveal the charred, spiderweb-cracked vertical face ready for the pry bars.`
* **SFX**: Swelling orchestral strings; echoing bootsteps of approaching quarrymen.

---

### ACT VI: THE CHISEL STORM & LEVER CREWS (05:35 – 06:35)

#### **Beat 54 (05:35 - 05:41)**
* **Shot**: Action Shot — Takshaka Quarrymen Charging Through Smoke (Cut B: Action Medium).
* **Narration**: *"The steam had barely cleared before the Takshakas charged into the smoking trench."*
* **Visual Prompt**: `ep02_13_crowbar_levering_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Handheld running camera following muscular Indian stonecutters charging into the damp trench.`
* **SFX**: Resounding war cries; heavy forged iron crowbars clattering against stone.

#### **Beat 55 (05:41 - 05:47)**
* **Shot**: Medium Action Video — Four Men Wedging Crowbars into Fissure (Video Target).
* **Narration**: *"Armed with long forged-iron crowbars, teams of four wedged their levers into the gaping thermal cracks."*
* **Visual Prompt**: `ep02_13_crowbar_levering_GENERATE_VIDEO.jpg`
* **Motion Prompt**: `Quarrymen drive four thick iron pry bars into deep fissure and heave downward in unison.`
* **SFX**: Grunts of synchronized effort: "Heave! Heave!"; creaking of iron under extreme leverage.

#### **Beat 56 (05:47 - 05:53)**
* **Shot**: Sledgehammer Impact Video — Shattering 2-Ton Basalt Plate (Video Target).
* **Narration**: *"With a unified heave, massive two-ton sheets of fractured stone sheared away from the bedrock and crashed into the trench floor."*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. Impact moment: A heavy basalt sledgehammer crashing down with maximum force onto a thermally weakened rock slab. The brittle stone crust disintegrates instantly into gravel and rubble with an explosive burst of fine grey volcanic dust, 8k`
* **Motion Prompt**: `Colossal 2-ton basalt slab breaks loose, toppling forward and crashing onto trench bedrock floor.`
* **SFX**: THUNDEROUS CRASH of two tons of stone hitting floor; explosive plume of grey dust.

#### **Beat 57 (05:53 - 05:59)**
* **Shot**: Close-up — Thirty-Pound Hammer Pulverizing Brittle Crust (Cut B: Hammer Strike).
* **Narration**: *"Behind them came the hammer men."*
* **Visual Prompt**: `ep02_14_sledgehammer_crush_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Heavy sledge swings down in slow motion, biting deep into fractured stone with zero recoil.`
* **SFX**: Heavy CRUNCH; stone fracturing effortlessly into fist-sized chunks.

#### **Beat 58 (05:59 - 06:05)**
* **Shot**: Cloud of Grey Basalt Dust Exploding on Impact (Cut C: Dust Burst).
* **Narration**: *"Their thirty-pound sledges easily smashed the heat-weakened slabs into manageable ballast."*
* **Visual Prompt**: `ep02_14_sledgehammer_crush_GENERATE_VIDEO.jpg (Cut C)`
* **Motion Prompt**: `Shockwave of pulverized mineral powder billows outward around hammer head.`
* **SFX**: Rhythmic hammer blows echoing down trench like relentless machine fire.

#### **Beat 59 (06:05 - 06:11)**
* **Shot**: Wide Trench View — Rapid Clearing of Stone Layers (Cut E: Wide Diagram).
* **Narration**: *"What would have taken weeks of agonizing hand-chiseling was reduced to rubble in twenty minutes."*
* **Visual Prompt**: `ep02_15_three_trenches_depth_PAN_ZOOM.jpg (Cut E)`
* **Motion Prompt**: `Time-lapse style motion showing entire layers of basalt vanishing as teams systematically pry and crush.`
* **SFX**: Fast-paced tabla and percussion rhythm driving forward.

#### **Beat 60 (06:11 - 06:17)**
* **Shot**: Low Angle — Plumb Line Hanging Flawlessly Against Clean Wall (Cut D: True Vertical).
* **Narration**: *"Fire had broken the mountain's spine."*
* **Visual Prompt**: `ep02_19_depth_marker_checking_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Tilt up the freshly exposed sheer vertical wall, perfectly straight alongside the hemp plumb bob.`
* **SFX**: Crisp scrape of finishing trowel clearing loose debris.

#### **Beat 61 (06:17 - 06:23)**
* **Shot**: Vertical Tilt — Deepening Trench Passing 15 Meters (Cut E: 160% Tilt).
* **Narration**: *"The perimeter walls deepened with ruthless precision, foot by agonizing foot."*
* **Visual Prompt**: `ep02_20_the_back_scarp_wall_PAN_ZOOM.jpg (Cut E)`
* **Motion Prompt**: `Rapid vertical descent into the shadowy chasm now fifteen meters below ground level.`
* **SFX**: Deep hollow cavernous echo of voices and tools.

#### **Beat 62 (06:23 - 06:29)**
* **Shot**: Medium Wide — The Emerging Shape of Central Monolith Island (Cut A: Sunset Island).
* **Narration**: *"In the center, untouched by fire, stood the sacred stone core."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Magnificent wide panoramic sunset view of the Ellora ridge. The central uncarved mountain island stands completely isolated: a colossal monolithic block thirty-three meters high, fifty meters long, framed by the deep three perimeter trenches. Purple and orange twilight sky, 8k`
* **Motion Prompt**: `Orbit shot around the rectangular central island of uncarved rock rising high above the excavated trenches.`
* **SFX**: Inspiring orchestral horn melody; warm temple bells.

#### **Beat 63 (06:29 - 06:35)**
* **Shot**: Kokasa Watching Crews Work in Synchronized Rhythms (Cut B: Master Architect).
* **Narration**: *"The industrial choreography of ancient India was in full flight."*
* **Visual Prompt**: `ep02_21_isolated_monolith_dusk_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Slow push-in on Kokasa watching hundreds of workers operating like a living, breathing machine.`
* **SFX**: Full symphony and traditional Indian percussion swelling in unison.

---

### ACT VII: GRAVITY AS AN ENGINE (100,000 TONS CLEARED) (06:35 – 07:35)

#### **Beat 64 (06:35 - 06:42)**
* **Shot**: Action Video — Boulders Hurtling Down Greased Timber Chute (Video Target).
* **Narration**: *"Now came the next impossible challenge: where do you put four hundred thousand tons of broken rock?"*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. High-energy action shot of a steep gravity chute constructed from heavy, oil-greased timber logs descending the cliff side. Enormous rough-hewn basalt boulders hurtling down the wooden ramp at high speed, kicking up rooster-tails of stone dust as they exit toward the valley, 8k`
* **Motion Prompt**: `Fast tracking shot alongside a 500-pound boulder rocketing down a steep greased wooden slide at 40mph.`
* **SFX**: Deafening wooden roaring rumble; screech of stone sliding across greased timber logs.

#### **Beat 65 (06:42 - 06:48)**
* **Shot**: Close-up — Oil-Greased Teak Logs Grooved for Sliding Rocks (Cut B: Chute Logs).
* **Narration**: *"There were no steam cranes. No diesel dump trucks."*
* **Visual Prompt**: `ep02_16_timber_gravity_chute_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Close-up of polished teak timber rails gleaming with dark sesame oil under harsh sunlight.`
* **SFX**: Heavy whoosh of air as another rock hurtles past; creaking timber supports.

#### **Beat 66 (06:48 - 06:55)**
* **Shot**: Wide Shot — Massive Wooden Slide Spanning Cliff to Valley Floor (Cut C: Wide Cliffside).
* **Narration**: *"If the rubble accumulated inside the trenches, the workers would be buried alive in their own excavation."*
* **Visual Prompt**: `ep02_16_timber_gravity_chute_GENERATE_VIDEO.jpg (Cut C)`
* **Motion Prompt**: `High wide shot showing three massive timber slide tracks plunging down the Charanandri western cliff.`
* **SFX**: Continuous rolling thunder of falling rocks echoing across valley plain.

#### **Beat 67 (06:55 - 07:02)**
* **Shot**: Wide Staging Plain — Armored War Elephants Hauling Sledges (Cut A: Full Wide).
* **Narration**: *"Kokasa used gravity as his engine."*
* **Visual Prompt**: `Cinematic 16:9 1080p film still. Wide shot of the staging plain below Charanandri cliff. Heavy timber sledges loaded with massive stone blocks being hauled by pairs of armored Indian war elephants and oxen with thick hemp rope harnesses. Ancient supply camp with tents and fires in background, 8k`
* **Motion Prompt**: `Sweeping camera movement across valley floor showing pairs of massive Indian bull elephants in harness.`
* **SFX**: Trumpeting elephant call; deep booming footfalls shaking dust from earth.

#### **Beat 68 (07:02 - 07:08)**
* **Shot**: Medium Tracking — Elephant Feet and Heavy Hemp Ropes in Tension (Cut B: 160% Punch-in).
* **Narration**: *"He constructed massive timber chutes from polished, oil-greased logs angled directly down the natural western slope of the cliff."*
* **Visual Prompt**: `ep02_17_elephant_haulage_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Low-angle tracking on massive elephant legs dragging heavy timber sledge across dry mud plain.`
* **SFX**: Straining hemp ropes groaning under tension; mahout calls and bells.

#### **Beat 69 (07:08 - 07:15)**
* **Shot**: Fast Action — Boulder Flying Out of Chute onto Plain (Cut C: Exit Ramp).
* **Narration**: *"Day and night, boulders were rolled into the chutes, screaming down the mountainside into the staging plains below."*
* **Visual Prompt**: `ep02_17_elephant_haulage_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Massive rock ejects from wooden chute mouth onto sand berm, kicking up high spray of dust.`
* **SFX**: Explosive impact boom on sand; cheers of valley clearance teams.

#### **Beat 70 (07:15 - 07:22)**
* **Shot**: Hero Portrait — Stonecutter Caked in Grey Dust, Sweat Glistening (Cut A: Hero Face).
* **Narration**: *"Down in the valley, teams of war elephants and bullocks dragged the heaviest blocks to build defensive ramparts, roads, and village water reservoirs."*
* **Visual Prompt**: `Cinematic 16:9 1080p portrait still. Intense, dignified close-up portrait of an elderly master stonecutter (Takshaka). Face caked in white and grey stone dust, sweat channels running down weathered dark skin, sharp piercing dark eyes, holding a heavy iron chisel. National Geographic documentary photography style, 8k`
* **Motion Prompt**: `Slow, reverent push-in on veteran stonecutter’s dignified, dust-streaked face.`
* **SFX**: Distant sounds of stone rolling and elephant bells; warm emotional cello phrase.

#### **Beat 71 (07:22 - 07:28)**
* **Shot**: Close-up Eyes of Veteran Stonecutter (Cut B: 180% Punch-in).
* **Narration**: *"Nothing was wasted. The mountain was not discarded; it was recycled into an empire."*
* **Visual Prompt**: `ep02_18_dust_and_sweat_PAN_ZOOM.jpg (Cut B)`
* **Motion Prompt**: `Extreme macro on dark weathered eyes reflecting the setting sun over the newly constructed city walls.`
* **SFX**: Gentle flute melody; wind whispering through stone quarries.

#### **Beat 72 (07:28 - 07:35)**
* **Shot**: Sun Setting Behind Valley Fortifications Built of Trench Rubble (Cut C: Rampart Sunset).
* **Narration**: *"One hundred thousand tons of earth had moved, and the real carving had not even started."*
* **Visual Prompt**: `ep02_18_dust_and_sweat_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `Golden sunset silhouette of fortress walls and reservoirs built from Kailasa's excavated basalt.`
* **SFX**: Solemn gong chime; rhythmic bass drum beat counting down time.

---

### ACT VIII: THE MONOLITHIC ISLAND & CLIFFHANGER (07:35 – 08:15)

#### **Beat 73 (07:35 - 07:40)**
* **Shot**: Magnificent Panoramic Drone Orbit — The Monolithic Island at Dusk (Cut C: Drone Orbit).
* **Narration**: *"By the end of the dry season, the impossible had been achieved."*
* **Visual Prompt**: `ep02_21_isolated_monolith_dusk_PAN_ZOOM.jpg (Cut C)`
* **Motion Prompt**: `High 360-degree drone orbit around the isolated stone block rising out of deep perimeter trenches.`
* **SFX**: Sweeping cinematic strings building to an epic crescendo.

#### **Beat 74 (07:40 - 07:45)**
* **Shot**: Wide Aerial Cutaway — U-Trench Completely Detached on Three Sides (Cut D: Top View).
* **Narration**: *"The three perimeter trenches had plunged thirty-three meters straight down into the living earth."*
* **Visual Prompt**: `ep02_21_isolated_monolith_dusk_PAN_ZOOM.jpg (Cut D)`
* **Motion Prompt**: `Overhead top-down camera looking straight into the rectangular abyss cut around the mountain island.`
* **SFX**: Wind whistling down into 100-foot deep rock chasm.

#### **Beat 75 (07:45 - 07:50)**
* **Shot**: Dimensional Callouts — 50m Long, 33m Wide, 33m High (Cut E: Metric HUD).
* **Narration**: *"And standing alone in the center of the abyss was a colossal, isolated island of solid mountain."*
* **Visual Prompt**: `ep02_21_isolated_monolith_dusk_PAN_ZOOM.jpg (Cut E)`
* **Motion Prompt**: `Holographic measurement markers snap onto monolith edges: 50m length, 33m width, 33m height.`
* **SFX**: Sharp caliper snaps; deep electronic sub-bass hum.

#### **Beat 76 (07:50 - 07:55)**
* **Shot**: Video Orbiting Kokasa Standing on Lone Summit (Video Target).
* **Narration**: *"Fifty meters long. Thirty-three meters wide. One hundred feet high. Completely detached from the cliff on three sides."*
* **Visual Prompt**: `Cinematic 16:9 1080p action still. Hero cinematic shot of master architect Kokasa standing alone at the very apex of the isolated central monolithic rock island at dusk. Wind whipping his linen shawl, gazing upward toward the evening star. The sheer vertical drop surrounds him. Cinematic cliffhanger ending, 8k`
* **Motion Prompt**: `Dynamic rotating camera orbiting Kokasa standing alone at the summit apex against purple twilight.`
* **SFX**: Wind whipping linen garments; solitary flute melody rising over strings.

#### **Beat 77 (07:55 - 08:00)**
* **Shot**: Close-up — Kokasa Looking Down at Rock Beneath His Feet (Cut B: 150% Punch-in).
* **Narration**: *"Kokasa climbed to the summit of the lonely stone monolith. Beneath his feet lay the hidden house of Shiva."*
* **Visual Prompt**: `ep02_22_cliffhanger_spire_summit_GENERATE_VIDEO.jpg (Cut B)`
* **Motion Prompt**: `Slow tilt down from Kokasa's resolute expression to his bare feet resting on virgin uncarved basalt.`
* **SFX**: Deep resonant drone; faint sacred chanting echoing from within the stone.

#### **Beat 78 (08:00 - 08:05)**
* **Shot**: Dramatic Tilt Down from Summit into 100-Foot Shadowed Abyss (Cut C: Abyss Tilt).
* **Narration**: *"The trenches were cut. The perimeter was cleared. Now came the terrifying part:"*
* **Visual Prompt**: `ep02_22_cliffhanger_spire_summit_GENERATE_VIDEO.jpg (Cut C)`
* **Motion Prompt**: `Vertigo-inducing tilt over the sheer edge straight down thirty-three meters into pitch-black trench floor.`
* **SFX**: Heart-stopping silence; single bass thud.

#### **Beat 79 (08:05 - 08:10)**
* **Shot**: Macro Action — Chisel Tip Placed on Apex of Stone Monolith (Cut D: Chisel on Spire).
* **Narration**: *"One mistake, one cracked column, and the entire temple would collapse before it was ever born."*
* **Visual Prompt**: `ep02_22_cliffhanger_spire_summit_GENERATE_VIDEO.jpg (Cut D)`
* **Motion Prompt**: `Macro extreme close-up of a pointed steel chisel tip resting gently upon the summit centerpoint.`
* **SFX**: Crisp metallic click of chisel touching virgin rock; sudden intake of breath.

#### **Beat 80 (08:10 - 08:15)**
* **Shot**: Cut to Black with Glowing Golden Sanskrit Title Card (Cut E: End Title Card).
* **Narration**: *"In Episode Three: Kokasa makes the first cut of the sacred spire. Subscribe, and descend into the stone."*
* **Visual Prompt**: `ep02_22_cliffhanger_spire_summit_GENERATE_VIDEO.jpg (Cut E)`
* **Motion Prompt**: `Screen snaps to solid black; glowing golden Sanskrit text: 'Kailasa: The First Cut — Episode 3 Next Week'.`
* **SFX**: Colossal temple gong reverberating into infinity; fade out.

---

## Companion Shorts Funnels (9:16 Vertical)

### Short 1: The Secret Engineering Weapon of Ancient India
* **File**: `ep02_short_01_thermal_shock_GENERATE_VIDEO.jpg`
* **Prompt**: `Cinematic 9:16 vertical 1080x1920 action still. Ancient Indian quarrymen dousing glowing cherry-red 600-degree basalt rock with cold mountain spring water inside a deep rock trench. Massive explosive eruption of white steam, flying stone fragments, chiaroscuro firelight, ultra-detailed, 8k`
* **Narration (52s)**:  
  *"How did 8th-century Indian builders cut three 100-foot-deep canyons through solid mountain without explosives or dynamite?  
  They used a terrifying scientific trick called Agni-Karma: thermal shock.  
  First, they stacked hundreds of tons of hardwood bonfires against the bedrock, heating the volcanic stone to six hundred degrees Celsius.  
  Then, at the peak of the heat, they threw hundreds of gallons of ice-cold spring water directly onto the glowing rock face!  
  The sudden contraction caused the mountain to literally tear itself apart at the molecular level, exploding with micro-fractures!  
  With the stone's spine broken, workers could pry off two-ton sheets of rock with simple iron crowbars in minutes instead of months!  
  Watch Episode Two of our full documentary series linked below to see how four hundred thousand tons were moved using gravity!"*
* **Pinned Comment**: *"Watch the full Episode 2 breakdown of the Kailasa Temple excavation here: [LINK]"*

### Short 2: Where Did 400,000 Tons of Mountain Go?
* **File**: `ep02_short_02_400k_tons_PAN_ZOOM.jpg`
* **Prompt**: `Cinematic 9:16 vertical 1080x1920 film still. Dramatic aerial view of the Kailasa Temple trench excavation site, showing enormous timber gravity chutes sliding tons of basalt boulders down the cliff into the valley, elephant haulage teams dragging them away, ancient Deccan landscape, documentary realism, 8k`
* **Narration (48s)**:  
  *"To build the Kailasa temple, ancient builders removed four hundred thousand tons of solid rock.  
  That’s more stone than the Great Pyramid of Giza by volume per worker!  
  So where did all the rubble go without bulldozers or dump trucks?  
  Architect Kokasa turned gravity into an engine.  
  He built massive wooden slides down the western cliff face, greased with sesame oil.  
  Workers rolled giant boulders into the chutes, and gravity shot them straight into the valley at fifty miles an hour!  
  Down below, teams of war elephants dragged the stone away to build roads, fortress walls, and reservoirs for nearby villages!  
  Nothing was wasted.  
  See how the three giant perimeter trenches were completed in Episode Two linked below!"*
* **Pinned Comment**: *"Watch the full story of the impossible Kailasa excavation in Episode 2: [LINK]"*
"""

EP02_PUBLISH_KIT_CONTENT = """# YouTube Publish Kit: Episode 2
## *The Inferno in the Trenches (Excavating 400,000 Tons: Fire, Water & The Three Trenches)*

This publish kit contains everything needed to publish and optimize **Episode 2** for maximum YouTube Click-Through Rate (CTR), Average View Duration (AVD), and subscriber conversion.

---

## 1. High-CTR Video Titles (A/B Test Options)

| # | Angle / Formula | Title | Why It Works |
| :- | :--- | :--- | :--- |
| **A** | **Curiosity / Engineering Mystery (Recommended)** | **How Ancient Indians Broke a Mountain with Fire and Water** | Irresistible primitive technology hook; exploits the physical contrast of fire & water vs diamond-hard stone. |
| **B** | **Epic Megalithic Scale** | **Where Did 400,000 Tons of Rock Go? The Kailasa Trench Excavation** | Massive quantifiable curiosity hook for engineering, archaeology, and ancient civilization fans. |
| **C** | **Cinematic Documentary** | **The Inferno in the Trenches: The 100,000-Ton Excavation of Kailasa (Ep. 2)** | High-authority episodic title for serious historical documentary audiences. |
| **D** | **Ancient Tech / Science** | **The Ancient Secret of Thermal Shock: How Kailasa Temple Was Cut** | Appeals to science, physics, geology, and technology enthusiasts searching for ancient engineering secrets. |
| **E** | **Short & Punchy (Mobile Optimized)** | **Cutting 100-Foot Trenches with FIRE: Kailasa Temple Mystery** | High visual punch on mobile recommendation feeds and push notifications. |

---

## 2. Complete YouTube Video Description (Copy & Paste)

```markdown
Before ancient builders could carve a single statue of Shiva, they had to remove 400,000 tons of the hardest rock on Earth. 

When iron chisels shattered against 140 MPa tholeiitic basalt, master architect Kokasa deployed an ancient weapon recorded in the Shilpa Shastras: Agni-Karma—the science of thermal shock. By roaring 600°C bonfires against the cliff face and violently quenching the cherry-red rock with ice-cold spring water, ancient Indian engineers forced the mountain to tear itself apart at the molecular level.

This is Episode 2 of our 10-part documentary series on the construction of the Kailasa Temple (Ellora Cave 16). Discover how 10,000 quarrymen cut three colossal perimeter trenches 33 meters deep into the bedrock, engineered 50-mph greased timber gravity chutes down the cliffside, and left a colossal 100-foot monolithic island of mountain standing isolated in the abyss.

🔔 Subscribe to follow the journey through all 10 episodes: https://youtube.com/@TheCuriosityChannel?sub_confirmation=1

--------------------------------------------------
TIMESTAMPS / CHAPTERS:
--------------------------------------------------
0:00 The Sound of War in Stone: Mobilizing 10,000 Quarrymen
1:05 The Geometry of the Three Trenches (33-Meter Vertical Abyss)
2:15 The Physical Limit of Iron: Why Steel Chisels Bounced
3:15 Agni-Karma: The Ancient Science of Thermal Shock
4:25 The Steam Flash: Quenching 600°C Basalt with Mountain Water
5:35 The Chisel Storm: Levering 2-Ton Basalt Slabs in Minutes
6:35 Gravity as an Engine: Timber Chutes & 100,000 Tons Cleared
7:35 The Monolithic Island Emerges (The Spire Cliffhanger)

--------------------------------------------------
WATCH THE COMPANION SHORTS:
--------------------------------------------------
📱 Short #1: The Ancient Fire & Water Weapon (Thermal Shock) ➡️ [LINK_TO_SHORT_1]
📱 Short #2: Where Did 400,000 Tons of Mountain Go? ➡️ [LINK_TO_SHORT_2]

--------------------------------------------------
HISTORICAL & ARCHAEOLOGICAL SOURCES:
--------------------------------------------------
• Kautilya's Artha-Shastra (Book 2, Chapter 12): Ancient mining techniques, fire-setting (Agni-Karma), and quenching.
• Shilpa Shastras & Manasara: Classical Indian treatises on deductive monolith excavation and lithological grading.
• Archaeological Survey of India (ASI): Architectural survey & volumetric measurements of Cave 16 (Kailasanatha), Ellora.
• Geological Survey of India: Mechanical testing of Deccan Traps basalt (120–140 MPa compressive strength).

--------------------------------------------------
SERIES PRODUCTION CREDITS:
--------------------------------------------------
• Series Concept & Direction: The Curiosity Production Lab
• Narration: Christopher (Studio Baritone)
• Visual Assets: Master Cinematic Suite (Gemini 2.5 Flash Image / Google Flow)
• Assembly Engine: Broadcast-Grade FFmpeg Normalization Engine

#KailasaTemple #ElloraCaves #AncientEngineering #AncientIndia #Documentary #Archaeology #Megalithic #HistoryMystery
```

---

## 3. YouTube SEO Tags (Studio Paste Ready)

### 500-Character Comma-Separated Block (Strictly Capped Under 500 Chars):
```text
Kailasa Temple,Ellora Caves,Kailasanatha Temple,How Kailasa temple was built,Ancient Indian Architecture,Ellora Cave 16,ancient engineering mysteries,thermal shock ancient quarrying,Agni Karma fire setting,ancient India documentary,King Krishna I,Rashtrakuta dynasty,top down rock cut temple,Kokasa architect,Deccan basalt,400000 tons rock,how ancient temples were carved,monolithic architecture,ancient technology,Kailasa excavation,gravity chutes ancient,Ellora caves history,megaliths
```

*(Tag character count: 489 characters — strictly within YouTube's 500-character limit).*

---

## 4. Strategic Pinned Comment (Algorithm Driver)

Pin this comment immediately upon publishing and heart it from the creator channel:

```markdown
Ancient engineers moved over 400,000 tons of solid basalt using fire-setting, water quenching, and greased gravity chutes—without a single crane or dump truck.

Do you believe ancient builders possessed lost engineering knowledge that modern science is only now rediscovering, or was this purely the triumph of 10,000 skilled workers under imperial discipline?

Drop your thoughts below! 👇

Watch Episode 3 (The First Cut: Carving the Sacred Spire from the Top Down) next Thursday!
Also check out our companion Short on the terrifying fire-setting trick: [LINK_TO_SHORT_1]
```

* **Why this works**: Directly challenges viewers with an engineering debate ("lost knowledge vs sheer discipline"), driving high comment velocity and signaling YouTube's recommendation algorithm to push the video onto browse features.

---

## 5. Master YouTube Thumbnail Concepts

### Concept A: The Fire & Steam Explosion (Recommended Master)
* **Visual Composition**: Extreme high-contrast split focus. Left side: roaring 600°C orange-yellow bonfire blazing against sheer black basalt rock face. Right side: massive explosive eruption of brilliant white steam plumes as cold water crashes against glowing cherry-red stone. In foreground silhouette, a muscular Indian master stonecutter holding an iron sledgehammer.
* **Text Overlay**: **"FIRE & WATER?!"** (Top-left, bold sans-serif, electric orange drop shadow).
* **Color Grading**: High dynamic range; fiery glowing amber (#FF7A00) contrasted against icy steam white (#FFFFFF) and obsidian volcanic basalt (#1A1A1A).

### Concept B: The 100-Foot Abyss
* **Visual Composition**: Vertigo-inducing high-angle drone perspective looking straight down into the rectangular 33-meter deep perimeter trench. Tiny human workers hauling timber slides at the bottom, emphasizing the sheer megalithic scale of the uncarved mountain island in the center.
* **Text Overlay**: **"400,000 TONS?!"** (Top-right, bold yellow with black outline).
* **Color Grading**: Golden hour sunset hitting the summit rim, fading into deep shadowed teal/obsidian in the chasm.

### Concept C: The Thermal Shock Crack
* **Visual Composition**: Extreme macro action close-up of dark basalt rock splitting open with glowing red interior stress fractures as ice-cold water splashes across it. A high-carbon steel chisel wedged into the crack as stone shatters like brittle glass.
* **Text Overlay**: **"ANCIENT WEAPON"** (Bottom-center, intense red glowing typography).
* **Color Grading**: Chiaroscuro lighting, cinematic particle sparks, and steam droplets.
"""

def main():
    print("Writing Episode 2 Comprehensive Storyboard...")
    EP02_STORYBOARD_FILE.write_text(EP02_STORYBOARD_CONTENT, encoding="utf-8")
    print(f"  -> Successfully updated: {EP02_STORYBOARD_FILE} ({len(EP02_STORYBOARD_CONTENT)} chars)")

    print("\nWriting Episode 2 YouTube Publish Kit...")
    EP02_PUBLISH_KIT_FILE.write_text(EP02_PUBLISH_KIT_CONTENT, encoding="utf-8")
    print(f"  -> Successfully created: {EP02_PUBLISH_KIT_FILE} ({len(EP02_PUBLISH_KIT_CONTENT)} chars)")

if __name__ == "__main__":
    main()
