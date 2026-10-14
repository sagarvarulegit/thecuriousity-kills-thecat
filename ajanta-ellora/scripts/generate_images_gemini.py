"""
Automated Batch Image Generator for Episode 1 using Gemini Flash Image.
Generates all remaining 18 master images + 2 Shorts images.
"""

import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
IMAGES_DIR = "ajanta-ellora/assets/episode-01/images"
os.makedirs(IMAGES_DIR, exist_ok=True)

MODEL = "gemini-2.5-flash-image"

IMAGES_TO_GENERATE = [
    {
        "id": "IMG-02",
        "filename": "ep01_02_king_sickbed.jpg",
        "prompt": "Cinematic 16:9 wide film still. King Krishna I of the 8th-century Rashtrakuta Dynasty lying ill on an ornate carved teak daybed draped in Indian silks, fever on brow, ancient bronze medicine bowls on low stone table, flickering oil lamp, historical authenticity, photorealistic, 8k"
    },
    {
        "id": "IMG-04",
        "filename": "ep01_04_architects_council.jpg",
        "prompt": "Cinematic 16:9 wide film still. Senior ancient Indian royal architects with gray beards in a grand stone palace council chamber shaking their heads in defeat, holding wooden measuring rulers and palm-leaf scrolls, King Krishna I visible on throne in background, dramatic lighting, 8k"
    },
    {
        "id": "IMG-05",
        "filename": "ep01_05_water_clock.jpg",
        "prompt": "Cinematic 16:9 macro close-up. Ancient Indian water clock (ghatika yantra), water droplets falling through a perforated copper bowl floating in a stone basin, measuring fleeting time, dark moody shadows, atmospheric oil lamp glow, 8k"
    },
    {
        "id": "IMG-06",
        "filename": "ep01_06_kokasa_entrance.jpg",
        "prompt": "Cinematic 16:9 wide film still. Master architect Kokasa in simple dark cotton dhoti walking confidently down the center stone aisle of a royal Indian palace toward the carved throne, courtiers watching in surprise, golden sunlight through carved stone lattices, 8k"
    },
    {
        "id": "IMG-08",
        "filename": "ep01_08_blueprint_cutaway.jpg",
        "prompt": "Cinematic 16:9 conceptual 3D architectural cross-section. A giant solid black basalt mountain cliff with glowing holographic blue blueprint lines showing a multi-tiered Dravidian temple carved inside it from the summit downward, subtractive engineering concept, 8k"
    },
    {
        "id": "IMG-09",
        "filename": "ep01_09_king_command.jpg",
        "prompt": "Cinematic 16:9 medium close-up. King Krishna I delivering a royal decree, wearing golden crown and royal jewelry, hand outstretched in command, regal authority and intense determination in his eyes, ancient Indian palace, 8k"
    },
    {
        "id": "IMG-10",
        "filename": "ep01_10_deccan_riders.jpg",
        "prompt": "Cinematic 16:9 wide panoramic landscape. 8th-century Deccan plateau Maharashtra, ancient scouts and riders on horseback crossing dry savannah beneath towering black basalt volcanic cliffs, golden morning light, epic historical adventure, 8k"
    },
    {
        "id": "IMG-11",
        "filename": "ep01_11_prehistoric_lava.jpg",
        "prompt": "Cinematic 16:9 epic visual. Prehistoric Deccan Traps continental flood basalt eruption, colossal volcanic fissure vents spewing rivers of glowing orange molten lava across black smoking plains, 66 million years ago, hyperrealistic, 8k"
    },
    {
        "id": "IMG-12",
        "filename": "ep01_12_charanandri_ridge.jpg",
        "prompt": "Cinematic 16:9 aerial drone shot. The rugged Charanandri basalt ridge at Ellora, 8th century, towering volcanic stone escarpment bathed in golden morning sun, ancient dirt path, untamed Deccan landscape, 8k"
    },
    {
        "id": "IMG-14",
        "filename": "ep01_14_treasury_chests.jpg",
        "prompt": "Cinematic 16:9 wide shot. Vast subterranean royal Rashtrakuta treasury, massive iron-banded teak chests overflowing with ancient gold dinar coins, silver ingots, pearls, and gemstone jewelry, guards holding torches in shadows, 8k"
    },
    {
        "id": "IMG-15",
        "filename": "ep01_15_copper_charter.jpg",
        "prompt": "Cinematic 16:9 macro shot. Ancient Indian royal scribe using a sharp iron burin to engrave Sanskrit inscriptions into polished copper sheet charter, copper shavings curling away, soft warm candlelight, 8k"
    },
    {
        "id": "IMG-16",
        "filename": "ep01_16_agrarian_supply.jpg",
        "prompt": "Cinematic 16:9 wide landscape. Ancient Deccan agrarian valley, farmers harvesting golden grain in irrigated fields, and a long convoy of wooden bullock carts laden with grain sacks moving along a dirt road toward the distant mountain, sunny day, 8k"
    },
    {
        "id": "IMG-17",
        "filename": "ep01_17_merchant_guild.jpg",
        "prompt": "Cinematic 16:9 medium shot. Wealthy ancient Indian merchants in fine embroidered muslin robes meeting with royal ministers, exchanging bags of gold and silver coins with ledger scrolls, open stone marketplace verandah, 8k"
    },
    {
        "id": "IMG-18",
        "filename": "ep01_18_artisan_camp.jpg",
        "prompt": "Cinematic 16:9 wide sprawling establishing shot. Ancient Indian construction encampment of hundreds of thatch and canvas tents at the base of the black volcanic cliffs of Ellora, cooking fires sending smoke into dawn air, bustling worker village, 8k"
    },
    {
        "id": "IMG-19",
        "filename": "ep01_19_blacksmith_forge.jpg",
        "prompt": "Cinematic 16:9 film still. Ancient Indian blacksmith forge, muscular artisan striking a glowing white-hot pointed steel chisel on an anvil with hammer, brilliant shower of sparks exploding, roaring charcoal furnace in background, night scene, 8k"
    },
    {
        "id": "IMG-20",
        "filename": "ep01_20_survey_summit.jpg",
        "prompt": "Cinematic 16:9 wide shot. Two ancient Indian master surveyors in traditional dhotis snapping a long red chalk rope across flat black volcanic bedrock on a mountain summit, an explosive cloud of red cinnabar dust rising in a razor-straight line, sunrise, 8k"
    },
    {
        "id": "IMG-21",
        "filename": "ep01_21_clay_model_seal.jpg",
        "prompt": "Cinematic 16:9 extreme close-up. King Krishna I pressing a heavy bronze royal signet ring with engraved Garuda eagle crest into molten red sealing wax on a copper charter, beside a carved miniature clay temple model, candlelight, 8k"
    },
    {
        "id": "IMG-22",
        "filename": "ep01_22_first_chisel_strike.jpg",
        "prompt": "Cinematic 16:9 silhouette. Ancient Indian quarryman holding a pointed steel punch against the volcanic rock on a mountain summit at dawn, another muscular worker swinging a heavy stone sledgehammer mid-air at the apex of his strike, dramatic morning sky, 8k"
    },
    {
        "id": "SHORT-01",
        "filename": "ep01_short_01_queen_vow.jpg",
        "prompt": "Cinematic vertical 9:16 portrait. Ancient Indian queen in royal silk saree kneeling in prayer before a glowing black stone Shiva lingam in a dark stone sanctum, flickering oil lamps, tear on cheek, dramatic lighting, vertical composition, 8k"
    },
    {
        "id": "SHORT-02",
        "filename": "ep01_short_02_treasury.jpg",
        "prompt": "Cinematic vertical 9:16 composition. Ancient Indian royal treasury vault, massive wooden chests overflowing with gold coins and jewels, royal scribes in background with palm leaves, torchlight, vertical frame, 8k"
    }
]

def generate_image_item(item):
    out_path = os.path.join(IMAGES_DIR, item["filename"])
    if os.path.exists(out_path):
        print(f"[{item['id']}] Already exists: {item['filename']}")
        return True

    print(f"\n[{item['id']}] Generating {item['filename']}...")
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
    print(f"==================================================")
    print(f"Starting Gemini Batch Image Generation ({len(IMAGES_TO_GENERATE)} images)")
    print(f"Model: {MODEL}")
    print(f"Target Directory: {IMAGES_DIR}")
    print(f"==================================================")

    success_count = 0
    for item in IMAGES_TO_GENERATE:
        ok = generate_image_item(item)
        if ok:
            success_count += 1
        time.sleep(3)  # Gentle pacing to avoid rate limits

    print(f"\nBatch Complete! Successfully generated/verified {success_count}/{len(IMAGES_TO_GENERATE)} images.")

if __name__ == "__main__":
    main()
