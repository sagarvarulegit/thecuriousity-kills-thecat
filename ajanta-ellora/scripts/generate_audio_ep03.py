"""
Episode 3 Narration & Subtitle Synthesizer using Edge-TTS
Generates high-definition neural voiceovers and synchronized .srt subtitles.
Uses broadcast-grade FFmpeg concatenation for the master narration track.
All assets isolated strictly in ajanta-ellora/episode03/

Revisions:
- Clearly distinguishes historical 8th-century Rashtrakuta patron King Krishna I from the
  medieval Marathi Katha-Kalpataru legend of King Ela, Queen Manikavati, and master builder Kokasa.
- Qualifies archaeological estimates (excavation depth up to 33m at rear scarp, estimated
  hundreds of thousands of tons of basalt, workforce of thousands over generations).
- Frames the 7-day completion as traditional folklore, contrasting it with the engineering reality
  that top-down excavation was a physical necessity for monolithic rock-cut architecture.
- Fixes all subtitle overlaps ensuring 100% strictly monotonic, non-overlapping SRT cues.
"""

import asyncio
import os
import re
import subprocess
from datetime import timedelta
from pathlib import Path
import edge_tts

# Target voice: en-US-ChristopherNeural (authoritative, cinematic)
VOICE = "en-US-ChristopherNeural"

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EPISODE_DIR = BASE_DIR / "episode03"
AUDIO_DIR = EPISODE_DIR / "audio"
SUB_DIR = EPISODE_DIR / "subtitles"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUB_DIR.mkdir(parents=True, exist_ok=True)

EPISODE_ACTS = [
    {
        "act": "act_01_the_monolith_abyss",
        "title": "Act I: The Monolith in the Abyss",
        "text": (
            "Look down into the abyss. "
            "At the sheerest face of the Charanandri ridge, three colossal trenches have severed the living rock, plunging over thirty meters into the mountain. "
            "Standing in the center of the chasm is an isolated island of volcanic basalt: roughly fifty meters long, thirty-three meters wide, and one hundred feet tall. "
            "Archaeologists estimate hundreds of thousands of tons of rock were cleared into the valley. "
            "Now, silence falls over the ridge. "
            "Thousands of quarrymen rest their sledgehammers. "
            "For months, they have cut away the perimeter. "
            "Now begins the true test of architectural history. "
            "Master architect Kokasa stands at the sheer edge of the trench, staring across the void at the naked stone island. "
            "The rock is raw, jagged, and unformed. "
            "Inside that monolithic block sleeps the greatest rock-cut temple ever conceived."
        )
    },
    {
        "act": "act_02_the_queens_vow",
        "title": "Act II: The Queen's Vow & The Legend of Kokasa",
        "text": (
            "Archaeological records and royal copper plates credit the eighth-century Rashtrakuta king, Krishna the First, with patronizing this monolithic wonder. "
            "Yet local tradition preserved an unforgettable human story. "
            "The medieval Marathi chronicle, Katha-Kalpataru, recounts the tale of King Ela and his queen, Manikavati. "
            "According to the legend, the queen made a desperate vow: she would touch neither food nor water until she beheld the crowning pinnacle of a temple dedicated to Shiva. "
            "The court architects bowed their heads in despair. "
            "To quarry foundations, raise walls, and mount the spire of a traditional temple would take twenty years. "
            "Before the first pillar stood, the queen would perish. "
            "Then, master builder Kokasa stepped forward with an audacity that stunned the court. "
            "He made an impossible promise: "
            "Within seven days, the queen shall gaze upon the crowning finial of Shiva's abode. "
            "The court was astonished: how could any builder conjure a temple spire in a single week?"
        )
    },
    {
        "act": "act_03_zero_margin_error",
        "title": "Act III: The Physics of Zero Margin for Error",
        "text": (
            "Kokasa understood a structural truth that modern engineers still revere: "
            "You do not carve a rock-cut monument from the bottom up. "
            "You carve it from the top down. "
            "Traditional construction is additive: you assemble stone on stone, correcting errors as you rise. "
            "Monolithic rock-cut architecture is ruthlessly subtractive. "
            "Every blow of the hammer is permanent. "
            "There was no scaffolding resting on the courtyard floor, because the courtyard was still trapped beneath one hundred feet of solid mountain. "
            "If an artisan cuts two inches too deep into a lintel, the roof shears. "
            "If a rock fissure is miscalculated, hundreds of tons of overhead basalt can fracture and collapse. "
            "You cannot glue a mountain back together. "
            "To carve the spire, Kokasa would not dig into the earth. "
            "He would climb to the sky."
        )
    },
    {
        "act": "act_04_shanku_sacred_grid",
        "title": "Act IV: The Solar Gnomon & The Sacred Grid",
        "text": (
            "At dawn, the master surveyors—the Sutradharas—climbed rope ladders to the summit of the isolated stone block. "
            "They carried no iron chisels. They brought the Shanku: a calibrated wooden solar gnomon. "
            "As the morning sun crested the Sahyadri ranges, the shadow of the gnomon tracked across the virgin basalt. "
            "By bisecting the shadow's morning and evening arcs, they established the true cardinal east-west axis. "
            "Next came the sacred cord, the Sutra. "
            "Dipped in wet vermilion red chalk, the cords were stretched taut and snapped against the basalt with sharp twangs. "
            "Grid lines bloomed across the summit: the Vastu-Purusha Mandala, a geometric matrix of sixty-four sacred squares. "
            "Every sanctuary wall, doorway, and column was calculated down to the millimeter before a single chip of stone was struck."
        )
    },
    {
        "act": "act_05_first_strike_stupi",
        "title": "Act V: The First Strike: Hewing the Stupi",
        "text": (
            "On the second morning, the Rupakaras—the master sculptors—ascended to the summit. "
            "At the exact center of the mandala, Kokasa placed the point of a tempered iron chisel. "
            "A hammer struck. "
            "The crack echoed through the empty trenches like a rifle shot. "
            "The sacred carving had begun. "
            "They did not excavate downward into the massif; they isolated the crowning finial: the Stupi. "
            "Working on their knees in a tight circle, artisans chipped away the surrounding basalt, sculpting a ribbed stone vase—the Kalasha—out of the living mountain. "
            "Unlike built masonry where finials are hoisted with timber winches, this multi-ton sacred crown was never lifted an inch. "
            "It was born directly from the volcanic ridge, permanently anchored to the bedrock of Earth."
        )
    },
    {
        "act": "act_06_four_tiers_vimana",
        "title": "Act VI: The Four Tiers of the Dravidian Vimana",
        "text": (
            "With the finial freed, the sculptors stepped downward onto narrow rock ledges, cutting the spire beneath their feet. "
            "This was the Vimana: a Dravidian stepped pyramidal tower. "
            "Tier by tier, the stone was peeled away like the rings of an onion. "
            "On the upper level, they sculpted the octagonal neck—the Griva—flanked by monolithic resting bulls. "
            "Below it, they hewed stepped storeys, carving miniature pavilion shrines—the Kutas and Salas—directly into the descending slopes. "
            "Under the Deccan sun, carvers worked shoulder to shoulder, suspended by hemp ropes over thirty-meter drops. "
            "Basalt dust rose like incense into the sky. "
            "By the fifth day, the stepped pyramid of the spire emerged from the rock, perfectly proportioned, tapering toward the heavens."
        )
    },
    {
        "act": "act_07_hollow_core_sanctum",
        "title": "Act VII: The Terrifying Hollow Core",
        "text": (
            "Now came the most perilous phase of the summit carving: "
            "Hollowing the mountain from the inside out. "
            "Directly beneath the finished spire lay the Garbhagriha—the sacred inner sanctum. "
            "To create this chamber, stonemasons had to bore horizontally into the stone beneath their own finished roof. "
            "They worked in suffocating darkness, lit only by bronze lamps burning sesame oil. "
            "Standing on suspended timber scaffolding, masons chipped away the basalt ceiling directly above their heads. "
            "One errant fracture could compromise the structural integrity of the roof slab. "
            "They tested the thickness of the stone by tapping the ceiling with hardwood mallets, listening to the resonance. "
            "A deep, hollow ring meant halt; a solid thud meant cut further. "
            "Working in continuous shifts, the sanctum ceiling was brought to structural perfection."
        )
    },
    {
        "act": "act_08_crown_emerges",
        "title": "Act VIII: The Crown Emerges & Cliffhanger",
        "text": (
            "In local folklore, the legend concludes with Queen Manikavati seeing the white spire and breaking her fast—a tale that arose to celebrate why Kailasa was carved from above. "
            "The artisans coated the newly hewn shikhara with a fine plaster of calcined seashell lime, burnishing it with smooth agates until it gleamed white against the dark basalt cliff. "
            "Yet beneath that gleaming spire, over eighty feet of solid mountain still waited in the abyss. "
            "In archaeological reality, top-down excavation was not a frantic seven-day miracle; it was a cold, calculated engineering necessity. "
            "It would take decades across generations of Rashtrakuta artisans to carve the vast courtyard, monumental elephants, and assembly halls down to the bedrock floor. "
            "Kokasa looked down from the summit into the shadowed abyss below. "
            "The crown was carved. "
            "Now, they had to excavate the body: slicing through thirty meters of stone to carve suspended bridges, monolithic pillars, and the great hypostyle hall. "
            "Next week, on Episode Four: The Floating Bridges of Kailasa. "
            "Subscribe, and carve the impossible."
        )
    }
]

SHORTS = [
    {
        "id": "short_01",
        "name": "short_01_the_queens_vow",
        "text": (
            "How was the world's largest monolithic temple hewn out of solid cliffside? "
            "While eighth-century Rashtrakuta inscriptions commemorate King Krishna the First as its patron, a medieval Marathi chronicle, the Katha-Kalpataru, preserves a dramatic legend of King Ela and Queen Manikavati. "
            "When the queen vowed to fast until she saw the temple's pinnacle, master artisan Kokasa promised to carve from the ridge downward so she could see the spire first! "
            "Modern archaeology reveals that while the seven-day completion is traditional folklore, top-down excavation into the basalt scarp was an ingenious engineering necessity. "
            "By carving from above, artisans never needed ground scaffolding, standing directly upon the bedrock they were sculpting! "
            "Over decades, thousands of carvers hewed a free-standing temple out of the mountain pit. "
            "Watch our full documentary linked below to explore the engineering secrets of Kailasa!"
        )
    },
    {
        "id": "short_02",
        "name": "short_02_why_carved_backwards",
        "text": (
            "Why is the world's largest monolithic temple carved from the roof down instead of the ground up? "
            "At Ellora Cave 16, ancient Indian sculptors didn't assemble foundation stones upward. They started at the cliff summit, carving the temple spire first, then the ceiling, the pillars, and finally the courtyard floor! "
            "Why? Because in subtractive rock-cut architecture, the mountain was their scaffolding. "
            "As artisans chiseled downward into the basalt massif, they stood directly upon the bedrock they were sculpting. "
            "One wrong strike could shear a load-bearing lintel and collapse the overhead rock! "
            "Watch our full documentary linked below to see how ancient engineers carved Kailasa from above!"
        )
    }
]

def format_timestamp(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def time_to_td(t_str: str) -> timedelta:
    h, m, s_ms = t_str.split(":")
    s, ms = s_ms.split(",")
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))

def clean_srt_cues(raw_srt: str) -> list:
    """Parses raw SRT text, enforces strict monotonicity and zero overlapping cues."""
    blocks = raw_srt.strip().split("\n\n")
    cues = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            time_match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})", lines[1].strip())
            if time_match:
                start_td = time_to_td(time_match.group(1))
                end_td = time_to_td(time_match.group(2))
                text = "\n".join(lines[2:])
                cues.append({"start": start_td, "end": end_td, "text": text})
                
    # Fix overlaps: ensure start[i] >= end[i-1] + 10ms
    cleaned = []
    for i, cue in enumerate(cues):
        start = cue["start"]
        end = cue["end"]
        if cleaned:
            prev_end = cleaned[-1]["end"]
            if start < prev_end:
                # Adjust previous end to precede current start
                if prev_end > start:
                    cleaned[-1]["end"] = max(cleaned[-1]["start"] + timedelta(milliseconds=100), start)
                    start = max(start, cleaned[-1]["end"] + timedelta(milliseconds=10))
        if end <= start:
            end = start + timedelta(milliseconds=500)
        cleaned.append({"start": start, "end": end, "text": cue["text"]})
    return cleaned

def write_cues_to_srt(cues: list, srt_path: Path, offset: timedelta = timedelta(seconds=0)):
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            s = format_timestamp(c["start"] + offset)
            e = format_timestamp(c["end"] + offset)
            f.write(f"{i}\n{s} --> {e}\n{c['text']}\n\n")

async def generate_speech(text: str, output_path: Path, srt_path: Path = None):
    communicate = edge_tts.Communicate(text, VOICE, rate="-4%", pitch="-2Hz")
    submaker = edge_tts.SubMaker() if srt_path else None
    
    with open(output_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary") and submaker:
                submaker.feed(chunk)
                
    if srt_path and submaker:
        raw_srt = submaker.get_srt()
        cleaned_cues = clean_srt_cues(raw_srt)
        write_cues_to_srt(cleaned_cues, srt_path)

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())

async def main():
    print("=" * 60)
    print("  EPISODE 3 NARRATION & SUBTITLES SYNTHESIS ENGINE (REVISED)")
    print("=" * 60)
    
    act_audio_files = []
    act_cues_list = []
    
    # 1. Synthesize 8 Acts
    for i, act_data in enumerate(EPISODE_ACTS, 1):
        act_key = act_data["act"]
        audio_out = AUDIO_DIR / f"{act_key}.mp3"
        srt_out = SUB_DIR / f"{act_key}.srt"
        
        print(f"\n[{i}/8] Synthesizing {act_data['title']}...")
        await generate_speech(act_data["text"], audio_out, srt_out)
        
        dur = get_audio_duration(audio_out)
        print(f"      -> Audio: {audio_out.name} ({dur:.2f}s)")
        print(f"      -> Subtitles: {srt_out.name}")
        act_audio_files.append(audio_out)
        
        # Load cleaned cues
        raw_content = srt_out.read_text(encoding="utf-8")
        cues = clean_srt_cues(raw_content)
        act_cues_list.append(cues)

    # 2. Synthesize 2 Shorts
    print("\n" + "=" * 60)
    print("  SYNTHESIZING 2 COMPANION VIRAL SHORTS")
    print("=" * 60)
    for short_data in SHORTS:
        s_name = short_data["name"]
        audio_out = AUDIO_DIR / f"{s_name}.mp3"
        srt_out = SUB_DIR / f"{s_name}.srt"
        
        print(f"\n[*] Synthesizing Short: {s_name}...")
        await generate_speech(short_data["text"], audio_out, srt_out)
        dur = get_audio_duration(audio_out)
        print(f"    -> Audio: {audio_out.name} ({dur:.2f}s)")
        print(f"    -> Subtitles: {srt_out.name}")

    # 3. Concatenate Master Audio File via FFmpeg
    print("\n" + "=" * 60)
    print("  BUILDING MASTER CONCATENATED AUDIO TRACK")
    print("=" * 60)
    
    master_audio_path = AUDIO_DIR / "episode_03_full_narration.mp3"
    concat_list_path = AUDIO_DIR / "concat_list.txt"
    
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for audio_file in act_audio_files:
            f.write(f"file '{audio_file.name}'\n")
            
    concat_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(master_audio_path)
    ]
    subprocess.run(concat_cmd, check=True, capture_output=True)
    concat_list_path.unlink() # Cleanup temp file
    
    total_master_dur = get_audio_duration(master_audio_path)
    print(f"\n[SUCCESS] Master audio assembled: {master_audio_path.name}")
    print(f"          Total Master Duration: {total_master_dur:.2f}s (~{total_master_dur/60:.2f} min)")

    # 4. Assemble Master Synchronized Subtitle Track (Zero Overlaps)
    print("\n" + "=" * 60)
    print("  ASSEMBLING MASTER SYNCHRONIZED SRT TRACK (ZERO OVERLAPS)")
    print("=" * 60)
    
    master_srt_path = SUB_DIR / "episode_03_full.srt"
    master_cues = []
    current_time_offset = timedelta(seconds=0)
    
    for i, act_data in enumerate(EPISODE_ACTS):
        act_key = act_data["act"]
        act_audio_file = AUDIO_DIR / f"{act_key}.mp3"
        act_dur = get_audio_duration(act_audio_file)
        cues = act_cues_list[i]
        
        for c in cues:
            master_cues.append({
                "start": c["start"] + current_time_offset,
                "end": c["end"] + current_time_offset,
                "text": c["text"]
            })
            
        current_time_offset += timedelta(seconds=act_dur)
        
    # Final pass to guarantee strict monotonicity
    for j in range(1, len(master_cues)):
        prev_end = master_cues[j-1]["end"]
        cur_start = master_cues[j]["start"]
        if cur_start < prev_end:
            master_cues[j-1]["end"] = cur_start - timedelta(milliseconds=10)
            
    with open(master_srt_path, "w", encoding="utf-8") as master_srt:
        for idx, mc in enumerate(master_cues, 1):
            s = format_timestamp(mc["start"])
            e = format_timestamp(mc["end"])
            master_srt.write(f"{idx}\n{s} --> {e}\n{mc['text']}\n\n")
            
    print(f"[SUCCESS] Master subtitles created: {master_srt_path.name}")
    print(f"          Total Cues: {len(master_cues)}")
    print("\nAll revised audio and subtitle assets successfully generated for Episode 3!")

if __name__ == "__main__":
    asyncio.run(main())
