#!/usr/bin/env python3
"""
embed_visuals_in_storyboard.py — Embeds all 62 corresponding image stills directly into the script & storyboard.
Channel: thecuriousity-kills-thecat
"""

import sys
import re
from pathlib import Path

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
sys.path.append(str(WORKSPACE_ROOT / "ajanta-ellora" / "scripts"))
import assemble_episode_08_full as a
import synthesize_episode_08_narration as s

manifest = a.get_manifest()

md_path = WORKSPACE_ROOT / "ajanta-ellora" / "episode08" / "script_and_storyboard" / "episode-08-the-silk-road-blue-and-mud-chemistry.md"

# Build the markdown content cleanly using ACTS_DATA and manifest
md_lines = [
    "# Episode 08: The Silk Road Blue & Mud Chemistry",
    "## Full Production Script, Acts Breakdown & Micro-Beat Storyboard",
    "**Series**: *Ajanta & Ellora: The Subterranean Titans* (Act II: The Lost Predecessor)  ",
    "**Channel**: `thecuriousity-kills-thecat`",
    "",
    "---",
    "",
    "## Executive Overview",
    "* **Runtime Target:** 9m 10s (~550s)",
    "* **Visual Pacing:** 62 Micro-Beats (Avg ~8.8s per cut, strictly respecting the micro-cut standard)",
    "* **Google Flow Kinetic Action Targets:** 16 Dedicated Action Shots (`ep08_gf_01` to `ep08_gf_16`)",
    "* **Infographic Ceiling:** Exactly 2 Structural Diagrams (0% Text Slides, Law 9 Compliant)",
    "* **Companion Shorts:** 2 Vertical Funnels (`short_01` and `short_02`, Law 12 & Retention Calibrated)",
    "* **Narrator Profile:** Adam Stone (`auq43ws1oslv0tO4BDa7`, `eleven_multilingual_v2`, `stability=0.55`, `similarity_boost=0.80`, `style=0.15`, `use_speaker_boost=True`)",
    "* **Audio Loudness Standard:** EBU R128 (-16.0 LUFS $\pm 1$, True Peak < -1.5 dBFS)",
    "* **Channel Operational Laws:** Law 1 & 2 (Google Flow Video Gate), Law 3 (Zero Duplicate Media Invariant), Law 9 (Max 1–2 Technical Diagrams, 0 Text Slides), Law 11 (Zero Content ID Audio Claims), Law 12 (Related Video Cliffhangers), Law 18 (In-Situ Visual Storyboards), Law 19 (Plain English Opening), Law 20 (Historical Realism)",
    "",
    "---",
    "",
    "## Part 1: The Master 5-Act Script & In-Situ Visual Storyboard",
    ""
]

cut_idx = 0

for act in s.ACTS_DATA:
    md_lines.append(f"### {act['title']}")
    md_lines.append("")
    for sentence in act["sentences"]:
        num = cut_idx + 1
        media_type, filename, motion = manifest[cut_idx]
        
        # Determine classification badge
        if "real_ajanta" in filename or "real_painting" in filename:
            badge = "🏛️ **Authentic Ajanta-Ellora Painting / Rock-Cut Cave**"
        elif "GENERATE_VIDEO" in filename or "ep08_gf_" in filename:
            badge = "🎬 **Google Flow Action Video Candidate Still**"
        elif "infographic" in filename:
            badge = "📊 **Structural Engineering Diagram**"
        elif "museum_scan" in filename or "archive" in filename:
            badge = "🏛️ **Authentic Museum Scan / Historical Archive**"
        else:
            badge = "🖼️ **Hero Still (4K Zoompan)**"
            
        md_lines.append(f"{num}. **{sentence}**")
        md_lines.append("")
        md_lines.append(f'   <div class="storyboard-card" style="background:#131b2e; border:1px solid #2a3754; border-radius:8px; padding:12px; margin:10px 0 16px 0; max-width:760px;">')
        md_lines.append(f'     <img src="../images/{filename}" alt="{filename}" style="width:100%; border-radius:6px; aspect-ratio:16/9; object-fit:cover; display:block; border:1px solid #1e293b;" />')
        md_lines.append(f'     <div style="font-size:0.82rem; color:#94a3b8; font-family:monospace; margin-top:8px;">{badge}: <code>{filename}</code> | Motion: <em>{motion}</em></div>')
        md_lines.append(f'   </div>')
        md_lines.append("")
        cut_idx += 1

# Append Parts 2, 3, 4
md_lines.extend([
    "---",
    "",
    "## Part 2: The 16 Google Flow Kinetic Action Shots Specification",
    "",
    "| Cut # | Action Identifier | Key Spoken Line / Beat | Kinetic Video Action Prompt (Google Flow / Veo / Runway) | Camera Movement | Target Duration |",
    "| :--- | :--- | :--- | :--- | :--- | :--- |",
    '| **02** | `ep08_gf_11_jungle_vines_monsoon_chaitya_flood` | "For four hundred years, thick jungle vines..." | Ancient ruins nature documentary. Heavy monsoon rainwater cascading down dark volcanic basalt cliffs into the Ajanta horseshoe gorge. Thick wild jungle creepers, banyan roots, and green moss wrapping around the carved horseshoe arch of an ancient rock chaitya facade. Water trickling over silted stone floors, misty jungle humidity, overcast rainy daylight. Raw authentic tropical wilderness. | Slow downward tilt tracking rainwater | 5.5s |',
    '| **06** | `ep08_gf_01_harishena_imperial_cavalry` | "Emperor Harishena united the Deccan..." | Historical documentary footage. 5th-century ancient Indian royal cavalry and armored war elephants walking along a dusty Deccan canyon cliff trail at late afternoon. Real cotton banners fluttering in natural dry wind, dust clouds rising realistically from heavy horse hooves and elephant feet, warm authentic golden sunlight raking over worn metal armor and hand-stitched fabrics. Ultra-realistic documentary style, 35mm film grain, 0% CGI fantasy glow, physically accurate dust and cloth dynamics. | Low-angle smooth forward tracking shot | 5.5s |',
    '| **07** | `ep08_gf_12_cliffside_bamboo_scaffolding_army` | "Master stonecutters carved twenty colossal new sanctuaries..." | Ancient construction historical documentary. Enormous, multi-level bamboo scaffolding structures lashed with thick hemp ropes clinging to a vertical black basalt canyon cliff face. Dozens of ancient Indian stonecutters climbing ladders, hauling timber beams and wicker baskets of rock debris. Chipping sounds of iron against stone, dust rising in morning sunbeams. A bustling 5th-century engineering site, totally realistic. | Slow vertical crane up along scaffolding | 5.0s |',
    '| **11** | `ep08_gf_13_basalt_weeping_water_droplets_macro` | "The walls were carved out of dense, volcanic flood basalt..." | Macro geological science documentary. Close-up of cold, dark, porous volcanic basalt rock face inside a deep cave. Tiny clear droplets of subterranean water slowly seeping through micro-fissures in the stone, swelling and trickling down the glassy black rock surface. Raking cool side light revealing the slick wet surface texture. Realistic macro fluid physics, high detail. | Macro slow pan downward following droplet | 4.5s |',
    '| **15** | `ep08_gf_05_chipping_basalt_key_sparks` | "Laborers rapidly pecked thousands of mechanical dimples..." | Authentic historical action. A skilled ancient stonecutter striking a pointed iron pick chisel against dark volcanic basalt wall. Rapid, precise hammer strikes pecking small pit dimples across the stone face. Tiny sharp rock chips fly off, momentary bright orange sparks flick off the dark igneous rock, fine basalt dust puffs in raking sunlight. Intense focus, sweat on the craftsman\'s brow, raw tactile stonecraft. | Macro side-profile push-in with sparks | 4.5s |',
    '| **18** | `ep08_gf_04_plaster_kneading_cowdung_matrix` | "A fermented plaster of red clay, cow dung, and rice husks..." | Historical reenactment documentary. Barefoot ancient Indian craftsmen in coarse dhoti waistcloths rhythmically treading and kneading thick organic reddish-brown mud plaster inside a rough wooden mixing pit. Golden rice husks, dry plant fibers, and dense wet clay squishing between toes with real physical weight and viscous mud resistance. Splashes of muddy water, realistic organic texture, warm natural daylight outside the rock shelter. | Low-angle panning shot across mud trough | 5.5s |',
    '| **23** | `ep08_gf_06_agate_burnishing_intonaco` | "A smooth, banded agate pebble burnishing the lime..." | Tactile macro craftsmanship. An artisan\'s strong, steady hand pressing a banded river agate stone against a fresh white slaked lime wall. Steady, circular rubbing strokes burnishing the wet plaster, visibly compressing the chalky surface into a smooth, glossy porcelain-like ivory sheen. Natural light glinting across the newly polished plaster surface. Intimate, authentic, zero digital effects. | Close-up steady tracking following stone | 5.0s |',
    '| **26** | `ep08_gf_14_mustard_oil_lamp_soot_smoke` | "For black, they gathered pure soot from burning mustard oil lamps..." | Traditional ancient chemistry craft. A small terracotta oil diya lamp burning with a steady golden flame fed by mustard oil. An inverted earthenware bowl held just above the flame collecting dense, velvety black carbon soot. A thin curl of realistic dark smoke rises gently against dark clay walls. Authentic craftsmanship, warm firelight reflections on clay vessels. | Macro focus shifting to black soot | 4.5s |',
    '| **32** | `ep08_gf_02_caravan_silkroad_lapis` | "Pack camels carried sacks of raw lapis lazuli..." | Historical realism. A Silk Road pack camel caravan slowly navigating a rugged rocky mountain pass in ancient India. Coarse woven hemp saddlebags packed tightly on camel humps, leather ropes creaking. Rough, unpolished electric-blue lapis lazuli rocks peeking out from coarse burlap bags. Natural daylight, gritty gravel slipping under camel footpads, realistic wind blowing mountain dust. Authentic National Geographic documentary feel, raw historical truth. | Smooth tracking shot alongside pack camels | 5.0s |',
    '| **34** | `ep08_gf_03_mortar_grinding_lapis_powder` | "Grinding blue crystals into priceless ultramarine..." | Macro documentary realism. Weathered, clay-stained hands of an ancient Indian artisan holding a heavy granite pestle, grinding raw deep-blue crystalline lapis lazuli minerals inside a stone mortar. Solid stone-on-stone crushing friction, blue mineral shards fracturing into intense azure powder, clear water poured from an earthenware jug creating swirling deep-blue paint paste. Natural raking daylight through cave archway, 100% tangible physical textures. | Slow macro push-in on mortar | 5.0s |',
    '| **45** | `ep08_gf_07_bronze_mirror_sunlight_beam` | "Large, circular cast-bronze mirrors caught the blazing sun..." | Historical optical engineering. An ancient Indian apprentice adjusting a large, circular cast-bronze mirror mounted on a heavy timber tripod on the sunlit cave veranda. The mirror\'s hand-polished golden metal catches the blazing midday tropical sun, casting a powerful, solid beam of reflected natural sunlight cutting straight through the dusty air into the dark cavern doorway. Physically accurate optics, dust motes drifting through the solar ray. | Dynamic pan from mirror down the sunbeam | 5.5s |',
    '| **48** | `ep08_gf_15_wet_linen_diffuser_light_beam` | "The wet fabric diffused the harsh solar glare..." | Ancient optical demonstration. Two young Indian apprentice boys holding a stretched sheet of bleached, wet white cotton fabric inside a dark rock cave. A concentrated beam of reflected sunlight strikes the wet cloth, instantly diffusing into a bright, glowing lantern effect that bathes the surrounding dark stone pillars and carved wall reliefs in soft, even, shadowless white light. Pure practical physics, tangible wet cloth weave. | Smooth tracking from beam to glowing wall | 5.0s |',
    '| **49** | `ep08_gf_09_cave_interior_sunlit_murals` | "Illuminating vibrant gold and turquoise ceiling mandalas..." | Subterranean architectural reveal. Moving smoothly forward between colossal carved stone columns inside Cave One. Gentle, soft, diffused golden sunlight sweeps across the painted ceiling mandalas and wall murals, revealing vibrant turquoise lapis blues, terracotta reds, and golden figures glowing in natural daylight deep inside the rock cave. Ancient monks and painters quietly working along scaffolding in background. Majestic, quiet, authentic. | Slow forward dolly between stone pillars | 6.0s |',
    '| **50** | `ep08_gf_08_brush_applying_lapis_eyelash` | "A delicate brush loaded with ultramarine blue..." | Extreme macro art restoration footage. A thin bamboo brush tipped with ultra-fine squirrel hair gently painting a razor-sharp, flowing black eyeliner contour on the smooth ivory plaster face of Bodhisattva Padmapani. Hand trembles slightly with human breath, liquid pigment soaking smoothly into plaster pores, soft diffused natural daylight softly illuminating the artwork. Intimate historical masterwork in progress. | Extreme macro slow push-in tracking brush | 5.0s |',
    '| **61** | `ep08_gf_16_abandoned_chisel_dropped_brush` | "Brushes were laid down wet, and terrified monks fled..." | Poignant historical stillness. Close-up on the stone floor of an unfinished cave. A fine bamboo paintbrush with wet ultramarine blue paint lying dropped across a terracotta pigment bowl, blue paint slowly seeping into the stone dust. Nearby, an iron chisel rests against a half-carved column base. Wind blows dry dust across the floor as footsteps hurry away in the distant corridor. Chilling, realistic historical abandonment. | Slow low-angle tilt up to silent hall | 5.0s |',
    '| **62** | `ep08_gf_10_harishena_shadow_cliffhanger` | "In 477 CE, a violent storm gathered outside the canyon..." | Dramatic historical cinema. Solitary back silhouette of Emperor Harishena in royal silks standing at the entrance of a rock-cut cave, looking out over the winding Ajanta horseshoe gorge under dramatic, dark monsoon storm clouds. Cold canyon wind whipping through heavy silk garments, lightning flashes softly illuminating wet volcanic rocks in the far distance. Foreboding, historical drama, realistic atmosphere. | Dramatic slow pull-back into darkness | 5.5s |',
    "",
    "---",
    "",
    "## Part 3: The 2 Structural Engineering Diagrams (Zero Cost, Law 9 Compliant)",
    "",
    "1. **Infographic 01: The 3-Layer Bio-Chemical Plaster Stratigraphy** (`ep08_infographic_01_plaster_stratigraphy.jpg`)",
    "   * Technical elevation cross-section showing:",
    "     * Layer 0: Raw Cretaceous Flood Basalt with Chipped Pick Dimples (Mechanical Key).",
    "     * Layer 1: Fermented Mud Bio-Matrix (5–15mm: Clay + Fermented Cow Dung Cellulose + Rice Husks + Neem Resin).",
    "     * Layer 2: Slaked Lime Intonaco (1–2mm: Chuna + Crushed Oyster Shell + Gypsum).",
    "     * Layer 3: Agate Burnished Surface & Mineral Pigment Layer (0.1mm: Ultramarine Lapis Lazuli).",
    "     * Micro-annotations with moisture-breathing arrows and antibacterial callouts.",
    "2. **Infographic 02: Bronze Mirror Optical Ray-Tracing Array** (`ep08_infographic_02_bronze_mirror_optics.jpg`)",
    "   * Architectural plan & ray-tracing diagram of Cave 1:",
    "     * Solar Azimuth (45° Incident Sunbeam) striking external Bronze Mirror (`Ø 80cm`).",
    "     * Primary collimated beam entering through pillared Veranda (`35m` penetration).",
    "     * Secondary reflection off suspended wet white linen diffuser sheet.",
    "     * Ambient scattered daylight (`~350 Lux`) reaching Padmapani sanctum with 0% carbon soot.",
    "",
    "---",
    "",
    "## Part 4: Companion Shorts Funnels (Law 12 & Retention Calibrated)",
    "",
    "### Short 01: The Mud Chemistry Secret",
    "* **Target Duration**: 48.4 seconds (5 cuts, 4.0s–12.0s per cut)",
    "* **High-Conflict Hook (0:00–0:09)**:",
    '  *"How did paintings made of fermented mud and cow dung survive fifteen hundred years in a damp volcano canyon without rotting?"*',
    "* **The Geological Paradox (0:09–0:18)**:",
    '  *"Ancient volcanic basalt sweats moisture constantly. In Europe, damp cave walls destroy paintings within decades."*',
    "* **The Bio-Chemical Solution (0:18–0:30)**:",
    '  *"Indian craftsmen mixed clay with digested cow dung fibers and rice husks, creating a living plaster that breathed humidity instead of trapping it."*',
    "* **The Agate Polish (0:30–0:40)**:",
    '  *"They sealed it with crushed sea shells, burnishing the wall with agate river stones until it shone like polished porcelain."*',
    "* **The Law 12 Unresolved Cliffhanger (0:40–0:48)**:",
    '  *"But what they used for the blue color broke every law of ancient trade. Tap the linked documentary below to see where they got it."*',
    "* **Native Directive**: Points directly to YouTube\'s mobile \"Related Video\" pill linking Episode 08.",
    "",
    "---",
    "",
    "### Short 02: The Bronze Mirror Secret",
    "* **Target Duration**: 52.2 seconds (5 cuts, 4.5s–12.0s per cut)",
    "* **High-Conflict Hook (0:00–0:10)**:",
    '  *"Ancient artists painted microscopic details forty meters inside a pitch-black mountain cave—without using a single fire torch."*',
    "* **The Mystery of Zero Soot (0:10–0:20)**:",
    '  *"Step inside Cave One, and you are in total subterranean darkness. Yet scientists found zero smoke or oil soot on the ceiling."*',
    "* **The Optical Engineering Solution (0:20–0:32)**:",
    '  *"How did they see? In the blazing sun outside, assistants angled massive polished cast-bronze mirrors toward the entrance."*',
    "* **Diffused Sunlight (0:32–0:42)**:",
    '  *"They bounced beams of blinding sunlight onto wet white linen sheets, filling pitch-black caverns with soft, shadowless daylight."*',
    "* **The Law 12 Unresolved Cliffhanger (0:42–0:52)**:",
    '  *"They were literally painting with captured sunlight. But in 477 CE, every painter dropped their brush and ran. Tap the linked documentary below to see why."*',
    "* **Native Directive**: Points directly to YouTube\'s mobile \"Related Video\" pill linking Episode 08."
])

md_path.write_text("\n".join(md_lines), encoding="utf-8")
print(f"[OK] Cleanly generated {md_path.name} with {cut_idx} visual cuts!")
