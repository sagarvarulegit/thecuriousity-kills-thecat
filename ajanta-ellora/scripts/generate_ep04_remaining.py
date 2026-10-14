"""
Bespoke Image Generator for Episode 04 Remaining Assets.
Uses Google Gemini API via official google-genai client with gemini-2.5-flash-image
to maximize visual fidelity while strictly minimizing token and API costs.
Generates all 31 remaining duplicates to achieve 100% zero cross-episode duplication.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EPISODE_DIR = BASE_DIR / "episode04"
IMAGES_DIR = EPISODE_DIR / "images"

ALL_TARGETS = [
    # --- ACTIVE SCENE BEATS (19 images) ---
    {
        "filename": "ep04_22_rockcut_span_vs_arch_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary architectural comparison illustration. On one side, an ancient Roman assembled stone arch showing keystones, voussoirs, and mortar joints under compression. On the other side, the Kailasa monolithic rock-cut horizontal stone bridge, carved directly out of solid Deccan basalt bedrock with zero joints or mortar. Glowing structural tension lines, deep volcanic basalt tones, museum grade archaeological diagram, 8k."
    },
    {
        "filename": "ep04_23_empty_courtyard_floor_beneath_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary film still. Vertigo-inducing high camera angle looking straight down from the edge of the suspended Kailasa rock bridge into the deep excavated courtyard floor 30 meters below. Dramatic shadow of the overhead bridge cast across the carved flagstones, dwarfed human scale, ancient basalt walls, morning sunlight, 8k photorealistic."
    },
    {
        "filename": "ep04_24_cantilever_anchor_geometry_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary macro photograph of the precise structural junction where the monolithic Kailasa stone bridge roots into the vertical living basalt cliff face. Seamless stone continuity with zero seams, zero mortar, visible ancient chisel fluting grooves, raw dark basalt texture, raking side sunlight, 8k National Geographic style."
    },
    {
        "filename": "ep04_25_chisel_fluting_underside_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 archaeological close-up looking up at the underside ceiling of the Kailasa rock-cut bridge. Parallel horizontal chisel fluting striations and ancient pick marks left by Rashtrakuta stonecutters in the dark Deccan volcanic rock. Warm golden bounce light from the courtyard floor illuminating ancient chisel marks, 8k documentary."
    },
    {
        "filename": "ep04_26_subtractive_structure_concept_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 archaeological conceptual illustration of subtractive carving at Ellora. A solid dark volcanic mountain mass shown with glowing translucent voids being removed step-by-step from the top down, leaving the suspended stone bridge hanging in midair without ever having been assembled. Deep charcoal and volcanic amber tones, 8k."
    },
    {
        "filename": "ep04_27_few_steps_walkway_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 eye-level film still standing directly on the upper walkway of the Kailasa monolithic stone bridge. Smooth ancient carved basalt walkway with shallow stone steps leading forward toward the upper portal of the Nandi pavilion. Low parapet walls, open air drop on either side, dawn sunlight, photorealistic 8k documentary."
    },
    {
        "filename": "ep04_29_southern_scarp_void_perspective_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary view across the southern canyon wall of Kailasa Temple. A wide empty sunlit void in the open air where the second monolithic bridge once spanned before ancient collapse. Towering dark basalt scarp wall, archaeological depth, morning dust motes, dramatic historical atmosphere, 8k."
    },
    {
        "filename": "ep04_31_surviving_vs_lost_span_comparison_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 architectural split comparison of Kailasa's two bridges. On the northern side, the intact surviving monolithic stone bridge standing triumphant across the courtyard gap. On the southern side, the jagged fractured rock stump where the companion bridge fell away into the courtyard centuries ago. Documentary archaeological lighting, 8k."
    },
    {
        "filename": "ep04_32_interpretive_reconstruction_ghost_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary photograph of the Kailasa southern cliff face with an elegant ghostly semi-transparent golden holographic architectural reconstruction line overlay showing how the lost southern bridge once connected the gateway to the southern shrines before its collapse. High production archaeological documentary, 8k."
    },
    {
        "filename": "ep04_33_sacred_procession_gateway_entry_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 historical recreation film still. Rashtrakuta era royal priests and attendants in fine Indian silk entering the upper level of the Kailasa gateway. Carrying bronze oil lamps and ceremonial offerings, stepping onto the elevated stone bridge threshold above the courtyard chasm. Warm candlelight and morning glow, 8k photorealistic."
    },
    {
        "filename": "ep04_34_shiva_hall_nandi_relationship_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary view framed through the carved pillars of the Nandi pavilion looking directly across the elevated axis toward the grand multi-tiered Vimana of the Great Shiva temple. Intricate rock-cut dvarapala guardians, deep relief carvings, monumental monolithic scale, dramatic morning sunlight, 8k."
    },
    {
        "filename": "ep04_35_four_part_spatial_sequence_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 wide architectural isometric illustration illustrating the sacred four-part linear spatial sequence of Kailasa Temple: Entrance Gopuram Gateway connected by overhead Bridge to Nandi Mandapa connected to Great Sabha Mandapa and Vimana Sanctuary, all carved from a single unbroken basalt mountain. Crisp archaeological lines, 8k."
    },
    {
        "filename": "ep04_37_upper_level_continuous_walkway_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 film still of the upper continuous walkway connecting the monolithic shrines of Kailasa at twilight. Warm oil torches burning in carved basalt wall niches casting amber reflections on the ancient stone floor, starry sky above the sunken courtyard canyon, atmospheric cinematic historical realism, 8k."
    },
    {
        "filename": "ep04_38_infrastructure_and_image_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 low-angle documentary photograph looking up from the courtyard at the majestic profile of the Kailasa floating bridge cutting against the brilliant blue sky. Showing how functional upper-level circulation becomes a sublime triumphal sky-arch framing the heavens. National Geographic documentary quality, 8k."
    },
    {
        "filename": "ep04_39_light_and_void_legibility_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary film still showing sharp geometric midday sunlight slicing through the open air void beneath the Kailasa rock-cut bridge. Extreme contrast between deep pitch-black shadows under the bridge and blinding golden light on the carved elephant plinth below, 8k photorealistic."
    },
    {
        "filename": "ep04_40_courtyard_return_full_bridge_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 wide panoramic documentary still from the north courtyard floor of Kailasa Temple. The complete horizontal span of the monolithic stone bridge stretching overhead between the two-storey gateway and Nandi pavilion, showcasing the sheer audacity of carving an aerial bridge from solid rock. 8k."
    },
    {
        "filename": "ep04_41_bedrock_continuity_overview_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 high-angle geological survey photograph of Kailasa Cave 16 at Ellora. The entire temple complex, bridge, gateway, pavilions, and courtyard walls clearly shown as a single unbroken geological sheet of dark Deccan volcanic basalt. Golden hour raking light highlighting continuous horizontal lava flows, 8k."
    },
    {
        "filename": "ep04_43_surviving_connections_tribute_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 golden hour documentary tribute still focusing on the surviving north bridge of Kailasa Temple. Warm sunset light washing over the weathered basalt carvings, fine stone balustrade, and ancient relief panels that have defied gravity for over 1,200 years. Poetic archaeological documentary, 8k."
    },
    {
        "filename": "ep04_44_question_mark_archaeology_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 atmospheric dusk documentary shot. A lone modern archaeologist with notebook standing in the silent courtyard of Kailasa Temple, looking up in wonder at the broken rock stump where the southern bridge once stood. Dramatic blue hour lighting, mysterious and contemplative, 8k photorealistic."
    },

    # --- HISTORICAL UNIVERSE ARCHIVE CARDS (12 images) ---
    {
        "filename": "ep04_archive_01_palace_dusk_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 historical still. Royal Rashtrakuta stone palace balcony overlooking ancient Manyakheta at dusk. Emperor Krishna I standing with bronze calipers reviewing temple architectural scrolls. Oil torches flickering in breeze, deep indigo twilight, 8k photorealistic."
    },
    {
        "filename": "ep04_archive_04_architects_council_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 documentary historical still. Master architect Kokasa and his guild of elder Sthapatis gathered over a large wooden drafting table studying charcoal blueprints of the Kailasa temple bridge connections. Warm oil lamp glow, detailed parchment, intense discussion, 8k."
    },
    {
        "filename": "ep04_archive_06_kokasa_entrance_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 film still. Master builder Kokasa standing at the edge of the Charanandri basalt ridge holding a plumb-bob and measuring cord, looking down into the newly excavated chasm where the bridges will hang. Morning wind billowing white cotton robes, heroic silhouette, 8k."
    },
    {
        "filename": "ep04_archive_07_kokasa_scroll_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 macro close-up of an ancient Sanskrit architectural manuscript scroll made of birch bark and palm leaves, showing precise geometric Sanskrit inscriptions and grid coordinates for monolithic rock-cut bridge cantilevers. Warm historical lighting, 8k."
    },
    {
        "filename": "ep04_archive_08_blueprint_cutaway_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 architectural cutaway diagram on aged vellum paper showing the 3D interior spatial voids, connecting bridges, and drainage channels of the Kailasa monolithic complex. Fine sepia and vermilion ink lines, museum conservation grade, 8k."
    },
    {
        "filename": "ep04_archive_11_prehistoric_lava_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 historical geological capture. Molten glowing red basalt lava cooling 65 million years ago into dense columnar Deccan trap basalt layers. Volcanic steam, cooling cracks forming horizontal basalt strata, primordial geological origin, 8k."
    },
    {
        "filename": "ep04_archive_12_charanandri_ridge_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 wide drone landscape of the Charanandri hills at Ellora before excavation began. Pristine untouched volcanic plateau crowned by wild grasses and acacia trees at sunrise, ancient India wilderness, 8k photorealistic."
    },
    {
        "filename": "ep04_archive_13_testing_basalt_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 historical still. Master quarryman striking a heavy bronze tuning fork and iron hammer against a raw basalt boulder to test the resonance and internal flawlessness of the volcanic rock. Dust rising, focused expression, golden morning light, 8k."
    },
    {
        "filename": "ep04_archive_15_copper_charter_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 museum macro photograph of an authentic 8th-century Rashtrakuta copper plate charter held together by a heavy royal Garuda seal ring. Ancient Old Kannada and Sanskrit inscriptions commemorating the construction of Kailasa temple, raking museum lighting, 8k."
    },
    {
        "filename": "ep04_archive_18_artisan_camp_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 historical wide film still. Bustling encampment of 7,000 Rashtrakuta stonecutters, blacksmiths, and rope-weavers at the foot of Ellora cliffs at dawn. Hundreds of smoke plumes rising from blacksmith hearths re-forging dull chisels, vibrant ancient industry, 8k."
    },
    {
        "filename": "ep04_archive_21_clay_model_seal_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 macro close-up. Ancient terracotta miniature architectural study model of the Kailasa temple bridge system resting on an architect's workbench. Sun-dried clay, intricate hand-molded miniature shrines and elevated walkways, warm oil lamp light, 8k."
    },
    {
        "filename": "ep04_archive_22_first_chisel_strike_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 macro action still. Pointed tempered-steel chisel tip resting against the pristine mountain surface, being struck by a heavy wooden mallet. First stone chips flying off the untouched rock summit, historic moment of inception, golden dawn light, 8k."
    }
]

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash-image"
    
    total = len(ALL_TARGETS)
    print("=" * 65)
    print(f"  EPISODE 04 BESPOKE GENERATOR (gemini-2.5-flash-image)")
    print(f"  Processing {total} assets with rate-limiting & minimal cost")
    print("=" * 65)
    
    success = 0
    for idx, item in enumerate(ALL_TARGETS, 1):
        target = IMAGES_DIR / item["filename"]
        print(f"\n[{idx:02d}/{total:02d}] Generating: {item['filename']}")
        
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=item["prompt"]
            )
            
            saved = False
            if resp.candidates and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        with open(target, "wb") as f:
                            f.write(part.inline_data.data)
                        print(f"  [OK] Saved {target.name} ({len(part.inline_data.data)} bytes)")
                        saved = True
                        success += 1
                        break
            if not saved:
                print(f"  [FAIL] No image bytes returned.")
        except Exception as e:
            print(f"  [ERROR] {e}")
            
        if idx < total:
            time.sleep(2.0)
            
    print("\n" + "=" * 65)
    print(f"  FINISHED: {success}/{total} assets generated and saved.")
    print("=" * 65)

if __name__ == "__main__":
    main()
