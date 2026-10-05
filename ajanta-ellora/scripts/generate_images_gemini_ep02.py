"""
Automated Batch Image Generator for Episode 2 using Gemini Flash Image.
Generates 22 master hero images (explicitly tagged _GENERATE_VIDEO vs _PAN_ZOOM),
2 YouTube Shorts images, and 1 Master Thumbnail in standard 1080p Full HD.
"""

import os
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
EPISODE_DIR = BASE_DIR / "assets" / "episode-02"
IMAGES_DIR = EPISODE_DIR / "images"
GOOGLE_FLOW_INPUT = EPISODE_DIR / "google_flow_input_images"
THUMBNAIL_DIR = EPISODE_DIR / "thumbnail"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_INPUT.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-image"

IMAGES_TO_GENERATE = [
    {
        "id": "IMG-01",
        "filename": "ep02_01_trench_sunrise_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Epic wide-angle dawn vista of Charanandri ridge at Ellora, western India, 756 CE. Golden morning sunlight piercing misty Deccan valley. Red cinnabar chalk lines glowing on flat dark basalt summit. Thousands of stonecutters assembling along the escarpment in historical Rashtrakuta attire. Cinematic atmospheric depth, authentic ancient Indian geology, 8k"
    },
    {
        "id": "IMG-02",
        "filename": "ep02_02_surveyor_plummet_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Ancient Indian master architect Kokasa kneeling on dark volcanic basalt, inspecting a stone groove filled with water for leveling. A senior surveyor holds a lead plumb bob on a twisted cord over a sheer rock edge. Dawn light reflecting in water trough, extreme tactile texture of basalt stone and weathered hands, 8k"
    },
    {
        "id": "IMG-03",
        "filename": "ep02_03_quarrymen_army_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Panoramic wide shot of hundreds of muscular ancient Indian quarrymen standing in disciplined ranks along the mountain summit. They hold iron sledgehammers and steel punch chisels over shoulders. Morning mist rising from Deccan plain below, golden sun flare, epic historical scale, photorealistic, 8k"
    },
    {
        "id": "IMG-04",
        "filename": "ep02_04_chisel_fracture_test_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Macro action close-up of a pointed high-carbon steel punch chisel being struck by a thirty-pound basalt hammer against cold, unyielding black basalt bedrock. Bright golden sparks flying on impact, steel tip visibly resisting without penetrating the ultra-dense volcanic stone. Photorealistic high-speed capture, 8k"
    },
    {
        "id": "IMG-05",
        "filename": "ep02_05_dulled_iron_pile_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Grim close-up of a large heap of ruined, blunted, and mushroomed iron chisel heads piled next to an ancient charcoal forge. In the background, blacksmiths hammer glowing metal under bamboo thatch awnings. Smoke, embers, intense contrast, historical realism, 8k"
    },
    {
        "id": "IMG-06",
        "filename": "ep02_06_hardwood_convoys_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide shot of an endless convoy of heavy wooden bullock carts hauling thick logs of dark Acacia and Teak hardwood up the steep rocky slope of the Charanandri ridge. Dust clouds kicked up by wooden wheels, harsh Deccan sunlight, monumental supply line logistics, 8k"
    },
    {
        "id": "IMG-07",
        "filename": "ep02_07_stacking_pyres_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Dramatic perspective looking down into a freshly cut five-meter deep trench in volcanic rock. Dozens of laborers carefully stacking dry timber logs and cow dung cakes tightly against the sheer vertical basalt rock face. Dust, dramatic shadows, authentic ancient quarry work, 8k"
    },
    {
        "id": "IMG-08",
        "filename": "ep02_08_bonfire_ignited_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Terrifying and spectacular night scene inside an ancient rock-cut trench. Roaring 600-degree Celsius bonfires blazing furiously against a massive vertical black basalt cliff wall. Intense orange and yellow flames leaping twenty feet high, swirling sparks, glowing embers, photorealistic fire dynamics, 8k"
    },
    {
        "id": "IMG-09",
        "filename": "ep02_09_superheated_bedrock_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Macro view of basalt bedrock glowing dull cherry-red through dying charcoal embers at extreme 600°C temperature. Intense heat distortion shimmering in the air, deep thermal stress visible in the mineral surface of the volcanic stone. Chiaroscuro lighting, 8k"
    },
    {
        "id": "IMG-10",
        "filename": "ep02_10_water_carriers_rushing_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Dynamic medium tracking shot of a continuous human chain of Indian laborers rushing forward carrying unglazed terracotta water jars and leather water skins (mashak). Sweat glistening on skin, motion blur on splashing water droplets, night firelight illumination, 8k"
    },
    {
        "id": "IMG-11",
        "filename": "ep02_11_thermal_shock_explosion_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Violent explosive impact of cold mountain spring water splashing against a glowing cherry-red 600°C basalt rock face. Massive sudden eruption of thick white steam, exploding thermal vapor, tiny spitting shards of fractured stone flying through the air. Cinematic high-speed explosion capture, 8k"
    },
    {
        "id": "IMG-12",
        "filename": "ep02_12_microfracture_cracks_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Extreme macro photorealistic shot of freshly cooled black basalt rock showing a dense network of micro-fractures and spiderweb fissures snapping open across the surface. Steam whispering from cracks, crystalline mineral grain boundaries tearing apart under thermal contraction, 8k"
    },
    {
        "id": "IMG-13",
        "filename": "ep02_13_crowbar_levering_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Action shot of four muscular ancient Indian quarrymen ramming long forged-iron crowbars into deep thermal fissures in a sheer trench wall. With coordinated muscle strain, a massive two-ton slab of fractured basalt breaks free and crashes downward in a plume of stone dust, 8k"
    },
    {
        "id": "IMG-14",
        "filename": "ep02_14_sledgehammer_crush_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Impact moment: A heavy basalt sledgehammer crashing down with maximum force onto a thermally weakened rock slab. The brittle stone crust disintegrates instantly into gravel and rubble with an explosive burst of fine grey volcanic dust, 8k"
    },
    {
        "id": "IMG-15",
        "filename": "ep02_15_three_trenches_depth_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p conceptual still. Breathtaking aerial isometric view of Ellora Cave 16 excavation site showing the vast U-shaped trench reaching fifteen meters deep into the Charanandri ridge. The central uncarved block of mountain stands isolated on three sides. Scale figures working like ants in the trench bottoms. Architectural clarity, 8k"
    },
    {
        "id": "IMG-16",
        "filename": "ep02_16_timber_gravity_chute_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. High-energy action shot of a steep gravity chute constructed from heavy, oil-greased timber logs descending the cliff side. Enormous rough-hewn basalt boulders hurtling down the wooden ramp at high speed, kicking up rooster-tails of stone dust as they exit toward the valley, 8k"
    },
    {
        "id": "IMG-17",
        "filename": "ep02_17_elephant_haulage_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide shot of the staging plain below Charanandri cliff. Heavy timber sledges loaded with massive stone blocks being hauled by pairs of armored Indian war elephants and oxen with thick hemp rope harnesses. Ancient supply camp with tents and fires in background, 8k"
    },
    {
        "id": "IMG-18",
        "filename": "ep02_18_dust_and_sweat_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p portrait still. Intense, dignified close-up portrait of an elderly master stonecutter (Takshaka). Face caked in white and grey stone dust, sweat channels running down weathered dark skin, sharp piercing dark eyes, holding a heavy iron chisel. National Geographic documentary photography style, 8k"
    },
    {
        "id": "IMG-19",
        "filename": "ep02_19_depth_marker_checking_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Low-angle view looking straight up a smooth, twenty-five-meter sheer vertical trench wall. A surveyor at the summit leans over to inspect a weighted hemp plumb line hanging perfectly flush against the rock face. Golden afternoon light grazing tool marks, 8k"
    },
    {
        "id": "IMG-20",
        "filename": "ep02_20_the_back_scarp_wall_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Monumental wide shot of the monolithic back scarp of Kailasa: A staggering 33-meter (108-foot) vertical wall of solid basalt towering over the excavated trench floor. Dramatic scale with tiny human workers at the base, emphasizing megalithic volume of stone cleared, 8k"
    },
    {
        "id": "IMG-21",
        "filename": "ep02_21_isolated_monolith_dusk_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Magnificent wide panoramic sunset view of the Ellora ridge. The central uncarved mountain island stands completely isolated: a colossal monolithic block thirty-three meters high, fifty meters long, framed by the deep three perimeter trenches. Purple and orange twilight sky, 8k"
    },
    {
        "id": "IMG-22",
        "filename": "ep02_22_cliffhanger_spire_summit_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Hero cinematic shot of master architect Kokasa standing alone at the very apex of the isolated central monolithic rock island at dusk. Wind whipping his linen shawl, gazing upward toward the evening star. The sheer vertical drop surrounds him. Cinematic cliffhanger ending, 8k"
    },
    {
        "id": "SHORT-01",
        "filename": "ep02_short_01_thermal_shock_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 9:16 vertical 1080x1920 action still. Ancient Indian quarrymen dousing glowing cherry-red 600-degree basalt rock with cold mountain spring water inside a deep rock trench. Massive explosive eruption of white steam, flying stone fragments, chiaroscuro firelight, ultra-detailed, 8k"
    },
    {
        "id": "SHORT-02",
        "filename": "ep02_short_02_400k_tons_PAN_ZOOM.jpg",
        "prompt": "Cinematic 9:16 vertical 1080x1920 film still. Dramatic aerial view of the Kailasa Temple trench excavation site, showing enormous timber gravity chutes sliding tons of basalt boulders down the cliff into the valley, elephant haulage teams dragging them away, ancient Deccan landscape, documentary realism, 8k"
    },
    {
        "id": "THUMBNAIL",
        "filename": "thumbnail_episode_02_master.jpg",
        "prompt": "YouTube thumbnail masterpiece, 16:9 high contrast, hyper-detailed. Glowing 600°C cherry-red volcanic rock face exploding with white steam as cold water hits it inside a massive deep trench. In the foreground, an intense Indian architect holding an iron chisel gazing into the steam. Bold text space top left: 'THE FIRE SECRET?!'. Neon orange fire embers vs cool electric steam white vs dark obsidian basalt, viral documentary hook, 8k"
    }
]

def generate_image_item(item):
    fname = item["filename"]
    if fname.startswith("thumbnail"):
        out_path = THUMBNAIL_DIR / fname
    else:
        out_path = IMAGES_DIR / fname

    if out_path.exists():
        print(f"[{item['id']}] Already exists: {fname}")
        # Ensure it's in google_flow_input_images if tagged GENERATE_VIDEO
        if "GENERATE_VIDEO" in fname:
            gf_target = GOOGLE_FLOW_INPUT / fname
            if not gf_target.exists():
                shutil.copy2(out_path, gf_target)
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

        saved = False
        for part in resp.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"  -> SUCCESS: Saved {out_path} ({len(part.inline_data.data)} bytes)")
                
                # If tagged GENERATE_VIDEO, also copy to google_flow_input_images
                if "GENERATE_VIDEO" in fname:
                    gf_target = GOOGLE_FLOW_INPUT / fname
                    shutil.copy2(out_path, gf_target)
                    print(f"  -> ISOLATED for Google Flow: {gf_target.name}")

                saved = True
                break
        if not saved:
            print("  -> No inline image bytes found in response parts.")
            return False
        return True
    except Exception as e:
        print(f"  -> Error: {e}")
        return False

def main():
    print("==================================================")
    print(f"Gemini Batch Image Generator (Episode 2: {len(IMAGES_TO_GENERATE)} targets)")
    print(f"Model: {MODEL}")
    print(f"Images Output: {IMAGES_DIR}")
    print(f"Google Flow Input Folder: {GOOGLE_FLOW_INPUT}")
    print(f"Thumbnail Output: {THUMBNAIL_DIR}")
    print("==================================================")

    success_count = 0
    for item in IMAGES_TO_GENERATE:
        ok = generate_image_item(item)
        if ok:
            success_count += 1
        time.sleep(3)  # Gentle 3s spacing to protect API quota

    print("\n==================================================")
    print(f"Batch Complete! Verified {success_count}/{len(IMAGES_TO_GENERATE)} images.")
    print("==================================================")

if __name__ == "__main__":
    main()
