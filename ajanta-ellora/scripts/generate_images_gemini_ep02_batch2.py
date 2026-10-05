"""
Batch 2 Image Generator for Episode 2 using Gemini Flash Image.
Generates 20 additional unique images (ep02_23 to ep02_42) to ensure
ZERO still images are repeated across the entire 7-minute documentary.
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "assets" / "episode-02" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-image"

NEW_IMAGES = [
    {
        "id": "IMG-23",
        "filename": "ep02_23_overseer_chalk_mark.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Extreme tactile close-up of a weathered ancient Indian stonecutter's hands snapping a taut hemp cord coated in powdered red cinnabar chalk onto smooth black volcanic basalt bedrock. Red dust puffs into the air, morning golden light, photorealistic, 8k"
    },
    {
        "id": "IMG-24",
        "filename": "ep02_24_trench_perimeter_aerial.jpg",
        "prompt": "Cinematic 16:9 1080p film still. High-angle bird's eye overhead perspective of the Charanandri rock mountain in Ellora, 756 CE. The huge U-shaped trench perimeter is marked with glowing red ochre lines into the stone surface around a colossal central rectangular monolith. Hundreds of tiny quarrymen assembling like ants, epic ancient engineering scale, 8k"
    },
    {
        "id": "IMG-25",
        "filename": "ep02_25_trench_depth_profile_schematic.jpg",
        "prompt": "Cinematic 16:9 1080p documentary visual. Architectural archaeological parchment drawing showing an engineering cross-section of Kailasa Temple trenches. Crisp technical cutaway lines showing the 33-meter vertical drop, the 30-meter wide courtyard floor, and the central stone mass. Sepia parchment texture with ancient Brahmi architectural notations and copper ink lines, historical blueprint, 8k"
    },
    {
        "id": "IMG-26",
        "filename": "ep02_26_workers_on_scaffolding.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Ancient Indian stonemasons working on sturdy lashed teakwood scaffolding suspended against a towering 30-meter vertical black basalt cliff face. Sunbeams piercing through the narrow gorge, dust motes floating in air, muscular workers chiseling rock in historical Rashtrakuta attire, authentic historical realism, 8k"
    },
    {
        "id": "IMG-27",
        "filename": "ep02_27_shadow_in_the_abyss.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Looking down into a terrifyingly narrow, sheer vertical stone trench 100 feet deep. The rock walls are pitch black tholeiitic basalt with vertical fluting chisel marks. A narrow beam of midday sunlight cuts through the darkness striking the trench floor, atmospheric gloom, dramatic lighting, 8k"
    },
    {
        "id": "IMG-28",
        "filename": "ep02_28_vertical_chisel_fluting.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Macro detail shot of ancient vertical pick and chisel scrape marks (scarp fluting) preserved on a basalt rock face at Ellora. Raking side sunlight revealing the precise rhythmic tool patterns carved by 8th-century quarrymen. Extreme mineral texture, olive-green plagioclase crystals embedded in black basalt, 8k"
    },
    {
        "id": "IMG-29",
        "filename": "ep02_29_metallurgist_inspecting_ore.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Ancient Indian master metallurgist in a rustic forge shed holding a fractured high-carbon iron chisel head up to an oil lamp, examining the microscopic grain of the shattered metal with a magnifying crystal lens. Smoke, bronze measuring calipers, scattered iron ore, intense scholarly concentration, 8k"
    },
    {
        "id": "IMG-30",
        "filename": "ep02_30_blacksmith_quench_bath.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Close-up of a glowing orange-hot hand-forged steel chisel being plunged into a stone basin filled with dark herb-infused quenching water. Violent white steam hissing and boiling up around the tongs, fiery glowing reflections in the blacksmith's sweat-streaked face, 8k"
    },
    {
        "id": "IMG-31",
        "filename": "ep02_31_trench_bonfire_night.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Breathtaking nocturnal view inside the massive 33-meter deep trench at Ellora. A continuous roaring wall of bonfires fueled by Acacia wood burning against the bottom of the black cliff. Towering flames casting dancing demonic shadows, thick black smoke billowing toward the starry sky, ancient Indian quarrymen tending fires with long poles, epic cinematic spectacle, 8k"
    },
    {
        "id": "IMG-32",
        "filename": "ep02_32_glowing_charcoal_bed.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Macro close-up of a massive bed of white-hot glowing charcoal and acacia logs packed directly against dense volcanic bedrock. The basalt rock surface is glowing cherry-red at 600 degrees Celsius, intense heat haze distortion, embers floating, fiery radiant glow, photorealistic, 8k"
    },
    {
        "id": "IMG-33",
        "filename": "ep02_33_clay_amphora_brigade.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Action wide shot of a human bucket brigade: hundreds of ancient Indian laborers in loincloths passing heavy terracotta water pots along stone steps cut into the trench rim. Splashing droplets of cool well water glittering in the torchlight against dark rock, dynamic motion, epic logistics, 8k"
    },
    {
        "id": "IMG-34",
        "filename": "ep02_34_steam_billowing_canyon.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Magnificent cinematic wide shot of the Charanandri mountain summit as massive geysers of white steam erupt from the perimeter trenches into the cool morning sky. The steam cloud rises 100 feet in the air like a waking volcano, backlit by the rising sun, quarrymen cheering on the rims, 8k"
    },
    {
        "id": "IMG-35",
        "filename": "ep02_35_teak_lever_crews.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Ten powerful ancient Indian quarrymen putting their full body weight onto a colossal 25-foot teakwood lever pole. The iron-tipped end of the lever bites into a thermal shock fissure, prying a massive five-ton basalt slab upward off the bedrock. Dust, muscle strain, sweat, historical engineering realism, 8k"
    },
    {
        "id": "IMG-36",
        "filename": "ep02_36_shattered_basalt_gravel.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Ground-level macro shot of the fractured trench floor: the basalt is shattered into thousands of angular, razor-sharp cobblestones and micro-fractured rubble. Bare-chested quarrymen using wicker baskets and broad wooden shovels to clear the debris, raw mineral texture, 8k"
    },
    {
        "id": "IMG-37",
        "filename": "ep02_37_timber_slide_detail.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Close-up of heavy timber log slides greased with mustard oil. A massive, freshly cleaved three-ton black basalt boulder slides violently down the steep chute, kicking up splinters and stone chips, speed blur, dynamic angle, photorealistic, 8k"
    },
    {
        "id": "IMG-38",
        "filename": "ep02_38_rubble_embankment_valley.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Panoramic view of the valley below Ellora where a colossal artificial embankment of 400,000 tons of crushed basalt rubble is being leveled into agricultural terraces and village foundations. Hundreds of bullock carts unloading, ancient city rising from the excavated mountain rock, 8k"
    },
    {
        "id": "IMG-39",
        "filename": "ep02_39_oxen_hauling_rubble_sled.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Low-angle dynamic shot of a team of large humped Deccan zebu oxen with painted horns straining against heavy wooden yokes, pulling a massive wooden sledge loaded with dark basalt boulders across rocky terrain. Dust swirls, harsh golden Deccan sunlight, monumental labor, 8k"
    },
    {
        "id": "IMG-40",
        "filename": "ep02_40_monolith_spire_silhouette.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Epic dramatic sunset silhouette of the newly isolated central stone monolith at Ellora Cave 16. The monolithic island rises 33 meters out of the excavated trench abyss, perfectly squared and isolated from the mountain. Amber, crimson, and deep indigo twilight sky, solemn majestic scale, 8k"
    },
    {
        "id": "IMG-41",
        "filename": "ep02_41_temple_courtyard_reveal.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide cinematic perspective standing on the high rear cliff looking down into the newly excavated U-shaped canyon. At the bottom, the wide stone courtyard floor is cleared, completely isolating the massive 200-foot central rock temple block. Torchlight glinting along the base, astonishing human achievement, 8k"
    },
    {
        "id": "IMG-42",
        "filename": "ep02_42_kokasa_pointing_spire.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Master architect Kokasa standing on the cliff rim at twilight with a group of senior Rashtrakuta master sculptors. Kokasa unrolls a parchment scroll and points his bronze pointer directly at the untouched summit of the central monolith. The cliffhanger moment before temple carving begins, dramatic rim lighting, epic historical drama, 8k"
    }
]

def generate_image(item):
    fname = item["filename"]
    out_path = IMAGES_DIR / fname

    if out_path.exists():
        print(f"[{item['id']}] Already exists: {fname}")
        return True

    print(f"\n[{item['id']}] Generating {fname}...")
    try:
        resp = CLIENT.models.generate_content(
            model=MODEL,
            contents=item["prompt"]
        )
        if not resp.candidates or not resp.candidates[0].content.parts:
            print(f"  -> No candidates returned.")
            return False

        for part in resp.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"  -> SUCCESS: Saved {fname} ({len(part.inline_data.data)} bytes)")
                return True
        print("  -> No inline image bytes found.")
        return False
    except Exception as e:
        print(f"  -> Error: {e}")
        return False

def main():
    print(f"Generating {len(NEW_IMAGES)} New Unique Images for Episode 2 (Zero Repetition Pool)...")
    success = 0
    for item in NEW_IMAGES:
        if generate_image(item):
            success += 1
        time.sleep(3) # 3s spacing to protect quota
    print(f"\nCompleted: {success}/{len(NEW_IMAGES)} generated successfully!")

if __name__ == "__main__":
    main()
