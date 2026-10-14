"""
Automated Batch Image Generator for Episode 3 using Gemini Flash Image.
Generates 25 master hero images (explicitly tagged _GENERATE_VIDEO vs _PAN_ZOOM),
2 YouTube Shorts images, and 1 Master Thumbnail in standard 1080p Full HD.
All outputs isolated in ajanta-ellora/episode03/
"""

import os
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
EPISODE_DIR = BASE_DIR / "episode03"
IMAGES_DIR = EPISODE_DIR / "images"
GOOGLE_FLOW_INPUT = EPISODE_DIR / "google_flow_input_images"
THUMBNAIL_DIR = EPISODE_DIR / "thumbnail"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_INPUT.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-image"

IMAGES_TO_GENERATE = [
    # --- ACT 1: THE MONOLITH IN THE ABYSS ---
    {
        "id": "IMG-01",
        "filename": "ep03_01_monolith_abyss_wide_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. High aerial drone view looking down into the colossal 33-meter-deep U-shaped trench canyon cut into the volcanic basalt ridge of Ellora. In the center stands an isolated, colossal rectangular island of dark uncarved basalt stone (50m long, 33m wide, 33m high). Dawn sunlight raking across the cliff rim, mist in the trench abyss, photorealistic archaeological documentary, 8k"
    },
    {
        "id": "IMG-02",
        "filename": "ep03_02_vertical_trench_walls_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. 45-degree angle showing the sheer 100-foot vertical back scarp of the trench cut into Deccan basalt. Visible ancient wedge marks and pick pits run vertically down the stone. In the shadowed chasm below, tiny figures of quarrymen walk along the gravel floor. National Geographic realism, morning light, 8k"
    },
    {
        "id": "IMG-03",
        "filename": "ep03_03_cleared_valley_floor_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide vista overlooking the Deccan plain below the Charanandri ridge. The steep slopes feature enormous polished timber gravity slides, and in the distance, bullock carts and war elephants drag piles of basalt ballast toward village roadworks. Warm golden hour light, epic cinematic scale, 8k"
    },
    {
        "id": "IMG-04",
        "filename": "ep03_04_silent_quarry_ridge_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Panoramic wide landscape of the mountain ridge at sunrise. Total stillness after the excavation storm. Cold volcanic bedrock, thin morning mist drifting across the plateau, silhouetted acacia trees against golden sky, documentary atmosphere, 8k"
    },
    {
        "id": "IMG-05",
        "filename": "ep03_05_resting_quarrymen_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Medium close-up of veteran ancient Indian quarrymen sitting along a ledge of basalt stone. Muscular, dust-caked shoulders, resting heavy iron sledgehammers on the rock. Exhausted but triumphant expressions, early morning side lighting, ultra-realistic skin texture and mineral grit, 8k"
    },
    {
        "id": "IMG-06",
        "filename": "ep03_gf_01_smoke_quarry_dissipate_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Dense white thermal shock steam and woodsmoke clearing from a deep 33-meter rock trench canyon at sunrise. Morning sunbeams piercing the drifting haze, revealing towering dark volcanic basalt cliffs. Atmospheric historical capture, 8k"
    },
    {
        "id": "IMG-07",
        "filename": "ep03_06_kokasa_staring_abyss_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Intense cinematic close-up of master architect Kokasa. His weathered, bronze face is etched with profound concentration, dust clinging to his graying beard. His dark eyes reflect the massive monolithic stone island across the abyss. Soft morning sun flare, photorealistic character study, 8k"
    },
    {
        "id": "IMG-08",
        "filename": "ep03_07_kokasa_trench_brink_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Full-length hero shot of master architect Kokasa standing at the sheer edge of the 100-foot vertical rock canyon. His simple white linen shawl whips in the mountain wind. He holds a rolled palm-leaf blueprint in one hand, gazing across the empty void at the raw stone monolith. Epic historical drama, 8k"
    },
    {
        "id": "IMG-09",
        "filename": "ep03_08_raw_virgin_basalt_peak_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Macro extreme close-up of the rough summit peak of the monolithic basalt island. Untouched dark volcanic stone sparkling with crystalline feldspar phenocrysts and olivine veins. Low raking sunlight emphasizes the ancient tactile roughness of the rock before the first chisel cut, 8k"
    },

    # --- ACT 2: THE QUEEN'S VOW & THE SEVEN-DAY DEADLINE ---
    {
        "id": "IMG-10",
        "filename": "ep03_09_royal_rashtrakuta_camp_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Panoramic wide view of the Rashtrakuta imperial royal encampment on the plateau at dusk. Large ornate silk pavilions in scarlet and saffron, bronze fire cauldrons blazing, armored guards with spears, royal banners bearing the golden eagle Garuda crest, epic 8th-century Indian empire, 8k"
    },
    {
        "id": "IMG-11",
        "filename": "ep03_10_ailing_queen_chamber_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Interior of an ornate royal tent chamber illuminated by oil lamps. A frail, beautiful ancient Indian Queen rests upon an intricately carved wooden daybed draped in fine silk. Court physician attends her bedside, solemn atmosphere, warm chiaroscuro oil-lamp lighting, historical realism, 8k"
    },
    {
        "id": "IMG-12",
        "filename": "ep03_11_queen_shiva_vow_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Intimate macro close-up of the Queen’s pale, delicate hands tightly clutching a solid gold amulet of Shiva’s trident (Trishula) over her chest. Tear of devotional determination on her cheek, glowing oil lamp reflection on gold jewelry, emotional dramatic realism, 8k"
    },
    {
        "id": "IMG-13",
        "filename": "ep03_12_despairing_architects_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide interior shot of King Krishna I’s council pavilion. A group of senior royal architects in white robes kneel before the throne with heads bowed in despair, holding architectural scrolls. Solemn tension, ornate wooden carved pillars, dramatic side lighting, 8k"
    },
    {
        "id": "IMG-14",
        "filename": "ep03_13_king_krishna_anguish_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Hero medium shot of Emperor Krishna I seated on the Rashtrakuta lion throne. He wears a heavy jeweled gold crown, his regal, bearded face twisted in anguish and desperation for his dying queen. Clenched fists resting on carved lion armrests, dramatic chiaroscuro lighting, 8k"
    },
    {
        "id": "IMG-15",
        "filename": "ep03_gf_02_kokasa_stepping_forward_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Master builder Kokasa stepping confidently forward past kneeling courtiers in the royal council pavilion. Resolute expression, white linen shawl draped over shoulder, torchlight casting bold dramatic shadows, historical documentary realism, 8k"
    },
    {
        "id": "IMG-16",
        "filename": "ep03_14_kokasa_hero_promise_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Dynamic low-angle hero shot of master builder Kokasa standing tall before the imperial throne. Raising his right hand with quiet, unshakeable authority as he declares his seven-day promise. The King looks up in astonishment, golden torchlight reflecting off linen robes, 8k"
    },

    # --- ACT 3: THE PHYSICS OF ZERO MARGIN FOR ERROR ---
    {
        "id": "IMG-17",
        "filename": "ep03_17_subtractive_sculpting_concept_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Conceptual artistic shot: an ancient master architect on a mountain peak at dusk, looking down at a detailed stone model of a temple spire carved directly into an outcrop of rock. Tactile texture of raw stone meeting perfected architectural lines, 8k"
    },
    {
        "id": "IMG-18",
        "filename": "ep03_gf_03_chisel_striking_flawless_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Macro high-speed action shot of a razor-sharp steel chisel held by a weathered hand striking unyielding black basalt bedrock. Brilliant shower of golden friction sparks bursting outward, tiny razor-sharp stone chips flying, ultra-sharp focus, 8k"
    },
    {
        "id": "IMG-19",
        "filename": "ep03_19_scaffolding_abyss_void_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Dramatic downward vertigo perspective from the summit of the 100-foot stone monolith looking straight into the empty trench canyon below. Complete lack of ground support or scaffolding; sheer vertical drop of black rock, wind whistling past, 8k"
    },
    {
        "id": "IMG-20",
        "filename": "ep03_20_catastrophic_fracture_risk_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Dramatic high-contrast visualization of structural failure: a massive fault fissure propagating through dark subterranean basalt, hairline cracks spreading under thousands of tons of dead weight. Tense geotechnical documentary aesthetic, 8k"
    },

    # --- ACT 4: THE SOLAR GNOMON & THE SACRED GRID ---
    {
        "id": "IMG-21",
        "filename": "ep03_24_sutradharas_climbing_summit_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide shot of ancient Indian master surveyors (Sutradharas) in white dhoti robes climbing thick hemp rope ladders up the vertical 100-foot cliff face to the summit of the monolith at sunrise. Golden morning light, epic scale, 8k"
    },
    {
        "id": "IMG-22",
        "filename": "ep03_gf_04_shanku_solar_shadow_timelapse_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. A carved wooden Shanku (solar shadow pole) standing perfectly vertical in a stone socket on the basalt mountain summit. Crisp morning sunlight casting a long needle-sharp shadow across a scribed circle on the rock, astronomical precision, 8k"
    },
    {
        "id": "IMG-23",
        "filename": "ep03_gf_05_snapping_chalk_line_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Macro action shot of two surveyors on the basalt peak snapping a taut hemp chord dipped in vibrant red vermilion powder against the rock. A small puff of bright red mineral dust explodes upward, leaving a laser-straight crimson guideline, 8k"
    },
    {
        "id": "IMG-24",
        "filename": "ep03_27_vastu_purusha_grid_peak_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. High aerial perspective of the flat basalt summit covered in a glowing geometric grid of 64 red vermilion squares (Vastu-Purusha Mandala). Senior architects in white linen kneeling at grid intersections checking measurements with brass calipers, sunrise, 8k"
    },

    # --- ACT 5: THE FIRST STRIKE: HEWING THE STUPI ---
    {
        "id": "IMG-25",
        "filename": "ep03_gf_06_first_hammer_strike_sparks_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Extreme macro close-up of a pointed steel punch chisel resting on the red chalk crosshair of the mandala center. A heavy bronze mallet crashes down into the chisel head, bright yellow sparks bursting into the air, first historic cut, 8k"
    },
    {
        "id": "IMG-26",
        "filename": "ep03_34_isolating_stupi_finial_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. A circle of master sculptors (Rupakaras) kneeling on the basalt summit, chiseling a deep circular trench to isolate a 4-ton block of raw basalt at the very apex. Flying stone chips, intense craftsmanship, morning light, 8k"
    },
    {
        "id": "IMG-27",
        "filename": "ep03_37_finished_stupi_hero_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Hero low-angle shot of the completed monolithic Stupi finial—a magnificent three-tiered ribbed stone Kalasha vase—standing pristine atop the volcanic peak against a vivid blue sky. Crisp carved edges, monolithic perfection, 8k"
    },

    # --- ACT 6: THE FOUR TIERS OF THE DRAVIDIAN VIMANA ---
    {
        "id": "IMG-28",
        "filename": "ep03_42_carving_griva_nandi_bulls_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Master sculptors working on the octagonal neck (Griva) of the temple spire. At the four cardinal corners, artisans meticulously carve life-sized monolithic Nandi bulls resting gracefully on the cornice mouldings. Tactile stone carving realism, 8k"
    },
    {
        "id": "IMG-29",
        "filename": "ep03_gf_07_sculptors_suspended_ropes_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Dramatic wide action shot of three muscular ancient Indian stonecutters suspended by thick hemp rope harnesses along the sheer 100-foot vertical face of the temple spire. Chiseling stepped horizontal tiers under blazing sun, billowing white stone dust, 8k"
    },
    {
        "id": "IMG-30",
        "filename": "ep03_45_stepped_pyramid_emerging_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. 45-degree aerial view of the partially carved Dravidian Vimana tower emerging from the mountain peak. Four stepped storeys crowned with miniature pavilion shrines (Kutas and Salas) carved directly into living rock, breathtaking archaeological reconstruction, 8k"
    },

    # --- ACT 7: THE TERRIFYING HOLLOW CORE ---
    {
        "id": "IMG-31",
        "filename": "ep03_gf_08_chipping_ceiling_sparks_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Dark, atmospheric cave interior beneath the carved spire roof. An ancient stonemason lying on high wooden scaffolding boards driving a chisel upward into the flat rock ceiling. Showers of sparks and grit raining down in warm flickering oil-lamp light, 8k"
    },
    {
        "id": "IMG-32",
        "filename": "ep03_53_wooden_mallet_acoustic_test_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Close-up of an ancient master mason inside the darkened sanctum, pressing his ear directly against the smooth basalt ceiling while tapping it gently with a solid wooden mallet to listen to acoustic resonance. Chiaroscuro torchlight, profound concentration, 8k"
    },
    {
        "id": "IMG-33",
        "filename": "ep03_55_perfected_sanctum_ceiling_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide shot inside the finished monolithic Garbhagriha inner sanctum. The flat, polished basalt ceiling hangs suspended across the chamber without a single support column. Flickering bronze oil lamps illuminating razor-sharp interior corners, sacred stillness, 8k"
    },

    # --- ACT 8: THE CROWN EMERGES & CLIFFHANGER ---
    {
        "id": "IMG-34",
        "filename": "ep03_57_gleaming_white_spire_hero_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Masterpiece hero wide shot: the finished four-tiered Dravidian temple spire gleams brilliant white, burnished with seashell lime plaster like fresh Himalayan snow. Rising proudly above the dark volcanic cliff rim against the dawn sky, breathtaking architectural triumph, 8k"
    },
    {
        "id": "IMG-35",
        "filename": "ep03_60_queen_breaking_fast_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Close-up of the joyful Rashtrakuta Queen on her royal pavilion veranda. Smiling through tears of devotion, taking a sip of holy water from a chased silver goblet as she gazes across the valley at the gleaming white temple spire on the horizon, morning sun, 8k"
    },
    {
        "id": "IMG-36",
        "filename": "ep03_62_kokasa_looking_down_abyss_hero_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Epic low-angle silhouette: master architect Kokasa stands at the edge of the newly carved spire terrace at dusk. He gazes straight down into the 80 feet of dark, solid, uncarved mountain below. Wind whipping his linen shawl, cliffhanger ending, 8k"
    },

    # --- YOUTUBE SHORTS FUNNELS ---
    {
        "id": "SHORT-01",
        "filename": "ep03_short_01_queens_vow_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 9:16 vertical 1080x1920 action still. An ancient Indian Queen in royal silk robes gazing out from a palace balcony toward a mountain peak where a brilliant white monolithic temple spire gleams in the morning sun. High contrast, viral documentary hook, 8k"
    },
    {
        "id": "SHORT-02",
        "filename": "ep03_short_02_carved_backwards_PAN_ZOOM.jpg",
        "prompt": "Cinematic 9:16 vertical 1080x1920 film still. Vertigo perspective from the top of the Kailasa temple spire looking down through carved levels to the 100-foot chasm below. Visualizing top-down subtractive carving without scaffolding, bold documentary realism, 8k"
    },

    # --- MASTER THUMBNAIL ---
    {
        "id": "THUMBNAIL",
        "filename": "thumbnail_episode_03_master.jpg",
        "prompt": "YouTube thumbnail masterpiece, 16:9 high contrast, hyper-detailed. A master Indian architect standing at the razor-edge summit of a 100-foot stone monolith holding an iron chisel against the peak, as a brilliant glowing white temple spire emerges from the dark volcanic mountain. Bold text space top left: 'CARVED BACKWARDS?!'. Neon gold sun flare vs dark basalt rock vs brilliant white lime spire, viral curiosity hook, 8k"
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
            print("  -> No candidates returned.")
            return False

        saved = False
        for part in resp.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"  -> SUCCESS: Saved {out_path.name} ({len(part.inline_data.data)} bytes)")
                
                if "GENERATE_VIDEO" in fname:
                    gf_target = GOOGLE_FLOW_INPUT / fname
                    shutil.copy2(out_path, gf_target)
                    print(f"  -> ISOLATED for Google Flow: {gf_target.name}")

                saved = True
                break
        if not saved:
            print("  -> No inline image bytes found in response parts.")
            return False

        time.sleep(2.5)  # Rate limiting protection
        return True
    except Exception as e:
        print(f"  -> ERROR generating {fname}: {e}")
        return False

def main():
    print("=" * 65)
    print("  EPISODE 3 GEMINI FLASH IMAGE MASTER BATCH GENERATOR")
    print("=" * 65)
    print(f"Total Visuals to Process: {len(IMAGES_TO_GENERATE)}")
    
    success_count = 0
    for item in IMAGES_TO_GENERATE:
        ok = generate_image_item(item)
        if ok:
            success_count += 1
            
    print("\n" + "=" * 65)
    print(f"  BATCH GENERATION COMPLETE: {success_count}/{len(IMAGES_TO_GENERATE)} VISUALS READY")
    print(f"  Isolated Google Flow Action Targets in: {GOOGLE_FLOW_INPUT}")
    print("=" * 65)

if __name__ == "__main__":
    main()
