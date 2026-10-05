"""
Generate the 8 bespoke base still images for Episode 04 Google Flow Video generation.
Uses gemini-2.5-flash-image for high visual fidelity at minimal cost.
Saves outputs to:
- ajanta-ellora/episode04/images/
- ajanta-ellora/episode04/google_flow_input_images/
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
EPISODE_DIR = BASE_DIR / "episode04"
IMAGES_DIR = EPISODE_DIR / "images"
GOOGLE_FLOW_DIR = EPISODE_DIR / "google_flow_input_images"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)

GF_STILLS = [
    {
        "filename": "ep04_gf_01_mist_clearing_bridge_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_01_mist_clearing_bridge.mp4",
        "beat": "Beat 06 (Act 1, Beat 6) | Spoken: 'From below, they look impossibly light.'",
        "image_prompt": "Cinematic 16:9 1080p documentary film still. Low-angle shot looking up through a deep basalt courtyard canyon at dawn. Dense white morning mist and thermal haze swirling around the monumental silhouette of the Kailasa suspended monolithic stone bridge hanging thirty feet in midair. Morning sunbeams piercing the haze, dark volcanic rock texture, 8k photorealistic.",
        "motion_prompt": "Slow camera drift pushing forward under the massive stone bridge as dense white morning fog and mist slowly swirl and dissipate, revealing the monumental dark carved basalt underbelly framing the soft dawn sky, cinematic historical lighting, 24fps."
    },
    {
        "filename": "ep04_gf_02_kokasa_precipice_survey_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_02_kokasa_precipice_survey.mp4",
        "beat": "Beat 18 (Act 2, Beat 9) | Spoken: 'The builders had to reveal a route and preserve its connection at the same time.'",
        "image_prompt": "Cinematic 16:9 1080p historical action still. Ancient Indian master architect Kokasa standing resolutely at the razor edge of a sheer 100-foot volcanic basalt cliff overlooking the excavated temple chasm at sunrise. Billowing white linen shawl, holding brass surveying calipers, determined gaze assessing the bridge axis, golden morning side light, 8k photorealistic.",
        "motion_prompt": "Ancient Indian master architect in white linen robes slowly steps forward to the razor edge of a sheer 100-foot volcanic basalt precipice, looking across the chasm at the surveyed bridge route. Wind blowing robes and hair, dramatic cinematic profile, morning golden hour light."
    },
    {
        "filename": "ep04_gf_03_snapping_chalk_axis_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_03_snapping_chalk_axis.mp4",
        "beat": "Beat 27 (Act 3, Beat 9) | Spoken: 'It is a carved line through space that makes the whole complex read as one deliberate design.'",
        "image_prompt": "Cinematic 16:9 1080p macro action still. Weathered artisan's hands pulling a taut cord saturated with bright red ochre mineral dye across the dark flat surface of freshly cut basalt bedrock. Red dust particles clinging to the string, ancient quarry background, dramatic morning side lighting, 8k ultra-sharp focus.",
        "motion_prompt": "Macro slow motion of a weathered bronze-skinned artisan pulling a taut red-ochre soaked cord upward from the basalt rock surface and snapping it down. A burst of vibrant red mineral dust puffs into the air, leaving a crisp straight dyed alignment line on the volcanic rock."
    },
    {
        "filename": "ep04_gf_04_chisel_undercutting_span_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_04_chisel_undercutting_span.mp4",
        "beat": "Beat 30 (Act 4, Beat 3) | Spoken: 'Stonecutters open the surrounding space in controlled stages, removing rock beside and beneath the intended passage.'",
        "image_prompt": "Cinematic 16:9 1080p macro action still. A pointed steel chisel held against the underside of a dark volcanic basalt rock bar. A heavy wooden mallet in mid-strike, sharp basalt fragments and fine grey rock powder bursting into the air, extreme macro close-up, dramatic lighting, 8k photorealistic.",
        "motion_prompt": "Macro high-speed close-up of a sharp tempered-iron point chisel tip being struck repeatedly by a wooden mallet. Sharp fragments and grey dust of dark volcanic basalt rock fly toward camera as the chisel carves into the horizontal rock underbelly."
    },
    {
        "filename": "ep04_gf_05_hammer_wedge_sparks_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_05_hammer_wedge_sparks.mp4",
        "beat": "Beat 36 (Act 4, Beat 9) | Spoken: 'The absence around the bridge was made deliberately, one removed surface at a time.'",
        "image_prompt": "Cinematic 16:9 1080p high-speed action still. A colossal 20-pound forged iron sledgehammer striking an iron splitting wedge deep inside a rock fissure. Brilliant shower of fiery golden friction sparks bursting outward against dark Deccan basalt, raw explosive physical force, 8k documentary.",
        "motion_prompt": "Slow motion impact of a colossal 20-pound iron sledgehammer slamming onto an iron splitting wedge driven into a rock fissure. Intense shower of bright golden friction sparks bursting outward as a massive block of basalt fractures away cleanly."
    },
    {
        "filename": "ep04_gf_06_chipping_cornice_sparks_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_06_chipping_cornice_sparks.mp4",
        "beat": "Beat 45 (Act 5, Beat 9) | Spoken: 'The void is part of the design, as carefully composed as the stone that remains.'",
        "image_prompt": "Cinematic 16:9 1080p action still. Skilled ancient Indian stone carver crouched under the curved stone cornice molding beneath the floating bridge, carefully holding a broad flat chisel and mallet. Delicate rock chips and fine dust showering down, soft warm bounce light from courtyard floor, 8k photorealistic.",
        "motion_prompt": "Close-up of a skilled sculptor crouched beneath the carved curved stone cornice of the suspended bridge, delicately tapping a broad flat chisel. Tiny white sparks and fine rock dust spray outward as intricate molding details emerge from the dark basalt."
    },
    {
        "filename": "ep04_gf_07_scarp_shadow_timelapse_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_07_scarp_shadow_timelapse.mp4",
        "beat": "Beat 54 (Act 6, Beat 9) | Spoken: 'The missing stone is evidence too, but it does not answer every question.'",
        "image_prompt": "Cinematic 16:9 1080p architectural still. The monumental sheer 30-meter vertical southern basalt scarp wall at Kailasa Temple, showing the rugged fractured rock scar where the southern bridge once connected. High contrast between blazing sunlight and pitch-black geometric rock shadows, 8k documentary.",
        "motion_prompt": "Cinematic timelapse of the massive vertical southern cliff scarp at Kailasa Temple. Sunlight and deep razor-sharp shadows sweep rapidly across the carved rock face and the empty gap where the lost bridge once stood, clouds racing overhead, shifting from bright morning to golden sunset."
    },
    {
        "filename": "ep04_gf_08_sculptors_on_ropes_GENERATE_VIDEO.jpg",
        "video_target": "ep04_gf_08_sculptors_on_ropes.mp4",
        "beat": "Beat 63 (Act 7, Beat 9) | Spoken: 'From below, sculpted passages cut across the sky above the court.'",
        "image_prompt": "Cinematic 16:9 1080p wide action still. Three ancient Indian sculptors suspended on thick braided hemp ropes along the sheer 100-foot vertical basalt cliff scarp of Kailasa courtyard. Working high in the open air, stone chips falling into the deep courtyard canyon below, dramatic historical scale, 8k photorealistic.",
        "motion_prompt": "Dramatic wide-to-medium camera tracking shot of three ancient Indian sculptors suspended on thick braided hemp ropes along the vertical 30-meter basalt canyon cliff, chipping rhythmically at the stone wall high in the air above the courtyard pit, wind swaying ropes gently."
    }
]

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash-image"
    
    total = len(GF_STILLS)
    print("=" * 65)
    print("  EPISODE 04 GOOGLE FLOW ACTION STILLS GENERATOR")
    print(f"  Generating {total} bespoke base stills at minimal cost")
    print("=" * 65)
    
    success = 0
    for idx, item in enumerate(GF_STILLS, 1):
        target_images = IMAGES_DIR / item["filename"]
        target_gf = GOOGLE_FLOW_DIR / item["filename"]
        
        print(f"\n[{idx:02d}/{total:02d}] Generating: {item['filename']}")
        
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=item["image_prompt"]
            )
            
            saved = False
            if resp.candidates and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        data = part.inline_data.data
                        with open(target_images, "wb") as f:
                            f.write(data)
                        with open(target_gf, "wb") as f:
                            f.write(data)
                        print(f"  [OK] Saved to images/ ({len(data)} bytes)")
                        print(f"  [OK] Isolated in google_flow_input_images/")
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
    print(f"  FINISHED: {success}/{total} Google Flow base stills ready.")
    print("=" * 65)

    # Generate Markdown Prompt Sheet
    sheet_path = GOOGLE_FLOW_DIR / "GOOGLE_FLOW_PROMPT_SHEET.md"
    md_content = "# Episode 04 Google Flow Video Generation Batch Sheet\n\n"
    md_content += "Use these 8 isolated base images in Google Flow / Runway Gen-3 / Veo to generate the 8 required action clips.\n\n"
    md_content += "| # | Input Still Image | Target Video Name | Spoken Narration Anchor | Google Flow Motion Prompt |\n"
    md_content += "|---|---|---|---|---|\n"
    for i, it in enumerate(GF_STILLS, 1):
        md_content += f"| {i} | `{it['filename']}` | `{it['video_target']}` | {it['beat']} | {it['motion_prompt']} |\n"
        
    md_content += "\n\n## Ingestion Instructions:\n"
    md_content += "1. Open Google Flow / Runway / Veo.\n"
    md_content += "2. Upload each input still from `ajanta-ellora/episode04/google_flow_input_images/`.\n"
    md_content += "3. Paste the corresponding Motion Prompt.\n"
    md_content += "4. Download the generated video clips, rename them to the exact **Target Video Name**, and place them in:\n"
    md_content += "   `ajanta-ellora/episode04/videos/`\n"
    md_content += "5. Once placed, inform the agent to execute the final assembly.\n"
    
    with open(sheet_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Generated Batch Prompt Sheet: {sheet_path}")

if __name__ == "__main__":
    main()
