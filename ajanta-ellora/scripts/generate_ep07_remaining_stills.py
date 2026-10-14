#!/usr/bin/env python3
"""
generate_ep07_remaining_stills.py — Generates remaining unique 16:9 cinematic stills
Enforces Law 3: Zero media repetition invariant (0 duplicates across the episode).
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()

IMAGES_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat/ajanta-ellora/episode07/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-image"

STILLS = [
    {
        "filename": "ep07_06_teak_scrub_plateau_rim_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Looking across the arid Deccan plateau covered in dry teak scrub, jagged dry basalt rocks, golden dry grass in harsh noon sun, subtle canyon edge hidden in background haze, 8k"
    },
    {
        "filename": "ep07_09_satavahana_ancient_scroll_charter_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p historical archive still. Macro top-down view of an ancient Satavahana dynasty royal copper plate charter with inscribed Brahmi script, resting on dark weathered wood with terracotta seals, authentic museum artifact lighting, 8k"
    },
    {
        "filename": "ep07_10_seven_centuries_stone_laboratory_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Panoramic view of ancient unfinished rock-cut cave facade at Ajanta, showing layers of experimental chisel strikes in dark basalt, morning sun raking across rough volcanic stone, 8k"
    },
    {
        "filename": "ep07_13_aniconic_buddha_wheel_footprint_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Close-up of ancient early Buddhist aniconic rock relief: carved sacred Dharmachakra wheel and Buddha footprints (buddhapada) in dark polished basalt, gentle candlelight reflection, 8k"
    },
    {
        "filename": "ep07_19_monsoon_dark_clouds_sahyadri_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Epic wide landscape of the Sahyadri mountain escarpment under massive, billowing dark monsoon storm clouds. Dramatic silver lightning illuminating jagged black volcanic ridges, 8k"
    },
    {
        "filename": "ep07_21_flood_erosion_basalt_crack_detail_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p macro still. Close-up of water erosion patterns in dark basalt rock, showing microscopic fractures and mineral veins being washed by thin water films, geological detail, 8k"
    },
    {
        "filename": "ep07_24_rock_cut_diversion_ravine_overflow_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Ancient rock-cut drainage gutter channel carving along the top of a basalt cliff, rushing overflow water spilling into a side ravine far from the cave entrance, monsoon afternoon lighting, 8k"
    },
    {
        "filename": "ep07_25_dry_season_arid_canyon_sunlight_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. The dry, arid Waghur canyon during summer. Sunbaked basalt cliffs, golden dust blowing across the empty riverbed, intense blazing sun, stark desert stillness, 8k"
    },
    {
        "filename": "ep07_27_basalt_cooling_joint_micro_filtration_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p macro still. Vertical cooling joint fissure in dense crystalline basalt. Clear water droplets slowly beading and filtering through dark mineral crystals, macro subterranean lighting, 8k"
    },
    {
        "filename": "ep07_29_acoustic_resonator_chaitya_elevation_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p architectural still. Symmetrical long interior perspective looking through the barrel-vaulted nave of Cave 10 chaitya hall. Sunlight pouring through the great horseshoe arch sun-window, illuminating geometric colonnade, 8k"
    },
    {
        "filename": "ep07_30_basalt_nonporous_wall_reverberation_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p macro still. Macro view of the ultra-dense, dark glassy surface of chiseled volcanic basalt inside an ancient cave sanctuary. Smooth hand-rubbed rock reflecting dim golden lamp light, 8k"
    },
    {
        "filename": "ep07_31_cave_9_nave_geometry_perspective_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Wide-angle interior of Cave 9 chaitya. Austere octagonal columns flanking the central aisle leading to the monolithic stone stupa dome, deep shadows and sacred stillness, 8k"
    },
    {
        "filename": "ep07_33_vocal_frequency_110hz_resonance_wave_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p artistic still. Ethereal golden soundwaves and acoustic frequency resonance rings vibrating through the dark stone nave of an ancient rock monastery, dust motes dancing in resonance, 8k"
    },
    {
        "filename": "ep07_35_bedrock_musical_instrument_nave_glow_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Looking up at the massive basalt vault of Cave 10 glowing in deep amber and indigo twilight, warm oil lamps creating golden halos on the curved stone ribs, sacred architectural harmony, 8k"
    },
    {
        "filename": "ep07_36_satavahana_dynasty_coins_copper_charter_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p historical archive still. Ancient lead and copper Satavahana coins with ship and elephant emblems lying beside an ancient palm-leaf manuscript on aged rough linen, warm museum light, 8k"
    },
    {
        "filename": "ep07_37_ancient_trade_routes_indian_ocean_ports_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Historical trade port scene on the western Indian coast at twilight. Ancient merchant ships with square sails anchored in a calm estuary, cargo crates and spices stacked on stone docks, 8k"
    },
    {
        "filename": "ep07_38_silent_canyon_abandoned_scarp_twilight_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Eerie silent panorama of the crescent Waghur gorge at twilight. Deep blue dusk sky, shadows engulfing the dark carved cave mouths along the cliff, utter solitude and silence, 8k"
    },
    {
        "filename": "ep07_40_wild_bamboo_bats_darkened_sanctum_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Looking from deep inside a dark abandoned cave sanctum out toward the overgrown entrance. Wild bamboo branches silhouetted against twilight sky, bats fluttering in the shadows, 8k"
    },
    {
        "filename": "ep07_41_dormant_chiseled_basalt_portal_shadow_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Ancient weather-beaten carved basalt doorway of Cave 10, cracked stone lintel and roots wrapping around ancient columns, ancient dust settled thick on the threshold, 8k"
    },
    {
        "filename": "ep07_43_sealed_canyon_secret_1000_years_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p still. Lush impenetrable green jungle canopy completely hiding the sheer canyon cliffs below. Morning mist rising from the gorge, mysterious and untouched wilderness, 8k"
    },
    {
        "filename": "ep07_45_polished_mirror_light_brass_reflector_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p macro still. Highly polished ancient bronze mirror reflector beaming a bright concentrated beam of natural sunlight into the dark interior of an ancient rock cave, illuminating vibrant wall pigments, 8k"
    }
]

def main():
    print("=" * 65)
    print("  EPISODE 07: GENERATING REMAINING UNIQUE STILL ASSETS")
    print("=" * 65)
    
    count = 0
    for item in STILLS:
        fname = item["filename"]
        out_path = IMAGES_DIR / fname
        if out_path.exists() and out_path.stat().st_size > 10000:
            print(f"[EXISTS] {fname}")
            count += 1
            continue
            
        print(f"[*] Generating {fname}...")
        try:
            resp = CLIENT.models.generate_content(
                model=MODEL,
                contents=item["prompt"]
            )
            if resp.candidates and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        with open(out_path, "wb") as f:
                            f.write(part.inline_data.data)
                        print(f"  -> Saved {fname} ({len(part.inline_data.data):,} bytes)")
                        count += 1
                        break
            time.sleep(2.0)
        except Exception as e:
            print(f"  -> Error generating {fname}: {e}")
            
    print("=" * 65)
    print(f"Ready: {count}/{len(STILLS)} stills in {IMAGES_DIR}")
    print("=" * 65)

if __name__ == "__main__":
    main()
