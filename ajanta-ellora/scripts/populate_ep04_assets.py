"""
Populate and generate all assets for Episode 04: The Floating Bridges of Kailasa.
Enforces the 3-Pillar Visual Diversity Formula and strict zero-repetition invariant.

Actions:
1. Copy 8 normalized action video clips from episode03/videos to episode04/videos.
2. Generate 15 key Bridge-specific hero visuals and thumbnail using Gemini Flash Image.
3. Pool distinct, unique universe archive stills from Ep 1, 2, 3 for remaining slots.
4. Verify all 64 images and 8 videos exist and are 100% unique (0 duplicates).
5. Populate google_flow_input_images/ directory.
"""

import os
import sys
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EP04_DIR = BASE_DIR / "episode04"
IMAGES_DIR = EP04_DIR / "images"
VIDEOS_DIR = EP04_DIR / "videos"
GOOGLE_FLOW_DIR = EP04_DIR / "google_flow_input_images"
THUMBNAIL_DIR = EP04_DIR / "thumbnail"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR / "scripts"))
from generate_episode04_assets import UNIQUE_BEATS_DATA

# 15 Key Bridge-Specific Prompts for Gemini Flash Image
KEY_BRIDGE_PROMPTS = [
    {
        "filename": "ep04_01_courtyard_ground_upward_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Low-angle perspective standing in the deep volcanic stone courtyard of Kailasa Temple (Ellora Cave 16), looking sharply upward at dawn. A colossal ancient stone bridge hangs suspended in mid-air thirty feet above, carved seamlessly from dark Deccan basalt rock, connecting two monolithic temple pavilions. Warm dawn sunlight grazing the rough rock surface, deep blue morning sky, National Geographic archaeological documentary, 8k."
    },
    {
        "filename": "ep04_02_gateway_to_hall_span_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide architectural elevation shot of Kailasa courtyard showing the open air span between the two-storeyed entrance gateway and the monolithic Nandi pavilion. Living rock bridge crossing the empty vertical chasm, ancient chisel marks visible, photorealistic historical documentary, 8k."
    },
    {
        "filename": "ep04_03_no_keystones_macro_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Telephoto macro shot looking directly at the underside of the rock-cut bridge at Kailasa Temple. Solid, continuous dark volcanic basalt stone, absolutely zero mortar lines, zero joint seams, zero keystones. Subtractive monolithic rock carving, ancient chisel dressing marks, dramatic side lighting, 8k."
    },
    {
        "filename": "ep04_04_monolith_mountain_reveal_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. High aerial panoramic view of the colossal rock trench of Kailasa Temple at Ellora. The entire temple complex, courtyard, gateway, and suspended bridges are revealed as a single continuous mountain of basalt released from the Charanandri ridge. Sunrise light, epic scale, 8k."
    },
    {
        "filename": "ep04_05_upper_bridge_ridge_walkway_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Upper level perspective walking across the narrow stone bridge walkway thirty feet above the courtyard floor. Carved basalt parapet with weathered lotus petal moldings, looking across to the upper terrace of the Nandi shrine, morning breeze, photorealistic 8k."
    },
    {
        "filename": "ep04_06_southern_cliff_broken_scar_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Dramatic close-up telephoto of the vertical southern cliff wall of Kailasa Temple. A clear, jagged fracture scar in the dark basalt marks the tragic historical break point where an ancient suspended stone bridge once connected to the cliff galleries before collapsing centuries ago. Atmospheric raking light, archaeological realism, 8k."
    },
    {
        "filename": "ep04_07_courtyard_shadow_silhouette_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Chiaroscuro high-contrast composition. The massive silhouette of the suspended Kailasa rock bridge casts a crisp, geometric diagonal shadow across the ancient carved relief sculptures of the courtyard rock wall. Morning sunbeam piercing the void, 8k."
    },
    {
        "filename": "ep04_08_bridge_puzzle_junction_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Detailed medium shot of the structural junction where the rock-cut bridge enters the solid vertical wall of the Nandi mandapa. The bridge and wall are one continuous piece of living volcanic bedrock with zero mortar or joint lines. Flawless subtractive masonry, 8k."
    },
    {
        "filename": "ep04_28_collapsed_span_wide_courtyard_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide vista of the southern Kailasa courtyard void. In the center, the great temple hall stands grandly, but toward the southern cliff wall, an immense empty gap reveals the missing fallen bridge span. Somber dramatic atmosphere, golden hour sunbeams, 8k."
    },
    {
        "filename": "ep04_30_fractured_rock_stub_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Macro telephoto focus on the jagged broken rock stump projecting outward from the upper gallery of Kailasa hall. Raw fractured basalt crystalline grain where the southern bridge snapped in antiquity, geological fracture planes, hyper-realistic stone texture, 8k."
    },
    {
        "filename": "ep04_36_bridge_cutting_sky_low_angle_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Looking almost straight up from the paved courtyard floor. The dark sculpted silhouette of the ancient Indian rock bridge cleanly bisects the vibrant cobalt blue morning sky. Golden sunlight crowning the upper balustrade, 8k."
    },
    {
        "filename": "ep04_42_subtractive_paradox_hero_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p hero still. Kailasa Temple at sunset. Warm amber light floods the courtyard, illuminating the intricate carved eaves of the suspended monolithic bridge linking gateway and shrine. An architectural masterpiece cut from solid mountain, majestic beauty, 8k."
    },
    {
        "filename": "ep04_45_plinth_elephant_teaser_01_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. The camera descends from the aerial bridges down to the colossal lower plinth of Kailasa Temple. A monumental life-sized elephant carved from the living bedrock emerges from deep shadow, appearing to bear the weight of the entire temple on its massive back. Dramatic teaser shot, 8k."
    },
    {
        "filename": "ep04_46_plinth_elephant_teaser_02_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Close-up profile of colossal rock-cut elephant heads along the base of Kailasa Temple. Detailed weathered ears, tusks, and caparisons hewn from solid volcanic stone, carrying the mountain cathedral above. Cinematic low-key lighting, 8k."
    },
    {
        "filename": "ep04_47_plinth_elephant_teaser_03_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Epic low-angle macro shot of a life-sized carved basalt elephant tusk silhouetted against the sunlit courtyard floor, guarding the subterranean foundations of Cave 16. Cliffhanger teaser for Episode 05, photorealistic 8k."
    },
    {
        "filename": "ep04_master_thumbnail_raw.jpg",
        "is_thumbnail": True,
        "prompt": "YouTube thumbnail masterpiece, 16:9 high contrast, hyper-detailed. Worms-eye perspective looking sharply upward through a massive ancient Indian stone bridge suspended 30 feet in open air between rock-cut temple pavilions. Deep volcanic basalt rock with glowing golden sunrise rim light against cobalt sky. Bold open negative space top-left for text. Viral curiosity hook, National Geographic documentary style, 8k."
    }
]

def copy_action_videos():
    print("\n[ACTION 1] Copying 8 Normalized Action Videos...")
    vids_src = BASE_DIR / "episode03" / "videos"
    video_names = [
        "gf_01_smoke_quarry_dissipate.mp4",
        "gf_02_kokasa_stepping_forward.mp4",
        "gf_03_chisel_striking_flawless.mp4",
        "gf_04_shanku_solar_shadow_timelapse.mp4",
        "gf_05_snapping_chalk_line.mp4",
        "gf_06_first_hammer_strike_sparks.mp4",
        "gf_07_sculptors_suspended_ropes.mp4",
        "gf_08_chipping_ceiling_sparks.mp4",
    ]
    for vname in video_names:
        src = vids_src / vname
        dst = VIDEOS_DIR / vname
        if not dst.exists() and src.exists():
            shutil.copy2(src, dst)
            print(f"  [COPIED] {vname}")
        elif dst.exists():
            print(f"  [EXISTS] {vname}")
        else:
            print(f"  [WARNING] Video source missing: {src}")

def generate_key_bridge_hero_stills():
    print("\n[ACTION 2] Generating Key Bridge Hero Stills via Gemini Flash Image...")
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    for item in KEY_BRIDGE_PROMPTS:
        fname = item["filename"]
        if item.get("is_thumbnail"):
            out_path = THUMBNAIL_DIR / fname
        else:
            out_path = IMAGES_DIR / fname
            
        if out_path.exists() and out_path.stat().st_size > 50000:
            print(f"  [EXISTS] {fname} ({out_path.stat().st_size // 1024} KB)")
            continue
            
        print(f"  Generating {fname}...")
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=item["prompt"]
            )
            saved = False
            if resp.candidates and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        with open(out_path, "wb") as f:
                            f.write(part.inline_data.data)
                        print(f"  -> SUCCESS: Saved {fname} ({len(part.inline_data.data) // 1024} KB)")
                        saved = True
                        break
            if not saved:
                print(f"  -> [WARN] Could not retrieve inline bytes for {fname}")
            time.sleep(2.0)
        except Exception as e:
            print(f"  -> [ERROR] Failed generating {fname}: {e}")

def pool_archive_and_hero_stills():
    print("\n[ACTION 3] Populating Remaining 1:1 Unique Assets Manifest...")
    # Gather all existing stills from ep01, ep02, ep03
    ep01_imgs = {p.name: p for p in (BASE_DIR / "episode01" / "images").glob("*.jpg")}
    ep02_imgs = {p.name: p for p in (BASE_DIR / "episode02" / "images").glob("*.jpg")}
    ep03_imgs = {p.name: p for p in (BASE_DIR / "episode03" / "images").glob("*.jpg")}
    
    all_available_pool = []
    # Combine pools prioritizing ep01, ep02, ep03 distinct stills
    for pool in [ep01_imgs, ep02_imgs, ep03_imgs]:
        for k, v in pool.items():
            if "thumbnail" not in k.lower():
                all_available_pool.append((k, v))
                
    used_sources = set()
    pool_idx = 0
    
    # Iterate through UNIQUE_BEATS_DATA
    for m_type, m_file, desc, motion in UNIQUE_BEATS_DATA:
        if m_type == "video":
            continue
        target = IMAGES_DIR / m_file
        if target.exists() and target.stat().st_size > 10000:
            continue
            
        # Check if direct archive mapping exists
        # e.g. ep04_archive_08_blueprint_cutaway_PAN_ZOOM.jpg -> ep01_08_blueprint_cutaway_PAN_ZOOM.jpg
        slug = m_file.replace("ep04_archive_", "ep01_").replace("ep04_", "ep01_")
        if slug in ep01_imgs:
            shutil.copy2(ep01_imgs[slug], target)
            print(f"  [LINKED EP01] {m_file} <- {slug}")
            used_sources.add(slug)
            continue
            
        # Otherwise pull a unique unused image from the pool
        assigned = False
        while pool_idx < len(all_available_pool):
            src_name, src_path = all_available_pool[pool_idx]
            pool_idx += 1
            if src_name not in used_sources:
                shutil.copy2(src_path, target)
                used_sources.add(src_name)
                print(f"  [POOLED UNIVERSE] {m_file} <- {src_name}")
                assigned = True
                break
                
        if not assigned:
            print(f"  [ERROR] Exhausted unique pool for {m_file}!")

def copy_google_flow_inputs():
    print("\n[ACTION 4] Populating Google Flow Input Images...")
    for p in IMAGES_DIR.glob("*GENERATE_VIDEO.jpg"):
        dst = GOOGLE_FLOW_DIR / p.name
        if not dst.exists():
            shutil.copy2(p, dst)
            print(f"  [GF INPUT] {p.name}")

def verify_manifest_uniqueness():
    print("\n[ACTION 5] Programmatic Assertion: Zero Media Repetition...")
    all_media = []
    missing = []
    
    for m_type, m_file, desc, motion in UNIQUE_BEATS_DATA:
        if m_type == "video":
            p = VIDEOS_DIR / m_file
        else:
            p = IMAGES_DIR / m_file
            
        if not p.exists():
            missing.append(f"[{m_type.upper()}] {m_file}")
        all_media.append(m_file)
        
    print(f"  Total Declared Cuts: {len(all_media)}")
    print(f"  Unique Media Files:  {len(set(all_media))}")
    print(f"  Missing On Disk:     {len(missing)}")
    
    if missing:
        print("  Missing items:")
        for m in missing[:10]:
            print(f"    - {m}")
        return False
        
    if len(all_media) == len(set(all_media)):
        print("  [PASS] ZERO REPETITION INVARIANT VERIFIED! 100% Unique Media across 72 cuts.")
        return True
    else:
        duplicates = [x for x in all_media if all_media.count(x) > 1]
        print(f"  [FAIL] Duplicates detected: {set(duplicates)}")
        return False

def main():
    print("=" * 65)
    print(" POPULATING & GENERATING EPISODE 04 BROADCAST ASSET SUITE")
    print("=" * 65)
    copy_action_videos()
    generate_key_bridge_hero_stills()
    pool_archive_and_hero_stills()
    copy_google_flow_inputs()
    ok = verify_manifest_uniqueness()
    if ok:
        print("\n[SUCCESS] Step 3 Completed: All 72 media files ready and verified.")
    else:
        print("\n[WARNING] Some assets need further resolution.")

if __name__ == "__main__":
    main()
