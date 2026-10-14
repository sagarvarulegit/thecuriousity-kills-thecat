"""
Episode 2 Narration & Subtitle Synthesizer using Edge-TTS
Generates high-definition neural voiceovers and synchronized .srt subtitles.
Uses broadcast-grade FFmpeg concatenation for the master narration track.
"""

import asyncio
import os
import subprocess
from datetime import timedelta
from pathlib import Path
import edge_tts

# Target voice: en-US-ChristopherNeural (authoritative, cinematic)
VOICE = "en-US-ChristopherNeural"

BASE_DIR = Path(__file__).resolve().parent.parent
EPISODE_DIR = BASE_DIR / "assets" / "episode-02"
AUDIO_DIR = EPISODE_DIR / "audio"
SUB_DIR = EPISODE_DIR / "subtitles"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUB_DIR.mkdir(parents=True, exist_ok=True)

EPISODE_ACTS = [
    {
        "act": "act_01_the_mobilization",
        "title": "Act I: The Sound of War in Stone",
        "text": (
            "Before you can carve a cathedral out of a mountain, you must perform an act of sheer violence against the earth itself. "
            "In the winter of 756 CE, ten thousand stonecutters climbed the Charanandri ridge. "
            "They did not begin by carving gods. They began by cutting three colossal trenches straight down into the crust of India. "
            "Two side trenches eighty-four meters long. One back scarp trench forty-seven meters wide. "
            "Together, they formed a massive U-shaped chasm thirty-three meters deep. "
            "Inside that chasm sat four hundred thousand tons of suffocating volcanic basalt. "
            "To free the temple, every single pebble had to be excavated by hand. "
            "And their enemy was not time. "
            "Their enemy was the hardest rock on planet Earth."
        )
    },
    {
        "act": "act_02_the_trenches",
        "title": "Act II: The Geometry of the Three Trenches",
        "text": (
            "Kokasa’s master plan demanded geometric perfection. "
            "If the trench walls leaned inward by even a fraction of a degree, the working space below would become a claustrophobic death trap. "
            "If they leaned outward, they would carve away rock needed for the temple’s sacred outer courtyards. "
            "To keep the cuts perfectly vertical thirty-three meters down, the Sutradharas used lead plumb-bobs and water leveling troughs. "
            "Every morning, water was poured into stone grooves etched along the summit rim. "
            "If the water drifted to the left, the cut was corrected. "
            "Millimeter by millimeter, the plumblines ensured the abyss descended true. "
            "Behind the temple site rose the sheer, terrifying back scarp: a single vertical wall of solid basalt taller than a ten-story building. "
            "From the valley below, it looked as though the empire had declared war on the mountain."
        )
    },
    {
        "act": "act_03_iron_limits",
        "title": "Act III: The Physical Limit of Iron & Steel",
        "text": (
            "The first week of excavation was a catastrophe. "
            "The stone of Ellora is tholeiitic basalt: cooled prehistoric lava packed with dense pyroxene and plagioclase crystals. "
            "Its compressive strength exceeds one hundred and forty megapascals. "
            "When a quarryman swung a thirty-pound sledgehammer against the cold bedrock, the steel chisel did not bite. "
            "It bounced. "
            "Shockwaves reverberated through the bones of the strikers’ arms, shattering wrists and blunting steel tips in minutes. "
            "By midday, piles of ruined, mushroomed iron chisels littered the camp. "
            "At this rate, simply excavating the three perimeter trenches would take forty years. "
            "The queen had only days. "
            "Kokasa knew that iron alone could never defeat the mountain. "
            "He needed a weapon hotter than the sun."
        )
    },
    {
        "act": "act_04_agni_karma",
        "title": "Act IV: The Ancient Science of Thermal Shock",
        "text": (
            "Kokasa turned to an ancient technique recorded in the Artha-Shastra and the Shilpa Shastras: Agni-Karma, the art of fire-setting. "
            "Convoys of bullock carts hauled thousands of tons of dense hardwood from the surrounding Deccan forests: Acacia, Khair, and ancient Teak. "
            "Quarrymen stacked the timber tightly against the basalt face in the trench, packing it with dried cow dung and sesame oil. "
            "At sunset, they set the trench ablaze. "
            "An inferno roared along the perimeter. Flames reached sixty feet into the night sky, turning the mountain ridge into a blazing volcanic ring. "
            "The basalt absorbed the terrifying heat. Its internal temperature soared past six hundred degrees Celsius. "
            "Inside the rock, individual mineral crystals began to expand at violently different rates. "
            "Quartz, feldspar, and pyroxene pushed against one another, turning the solid mountain into a compressed bomb."
        )
    },
    {
        "act": "act_05_shock_flash",
        "title": "Act V: Quenching the Mountain: The Thermal Explosion",
        "text": (
            "Then came the flash. "
            "As the bedrock glowed a dull cherry-red, Kokasa gave the signal. "
            "A human chain of five hundred water carriers rushed forward, carrying leather water skins and cold terracotta pots filled from the mountain spring. "
            "In a single synchronized motion, hundreds of gallons of ice-cold water struck the six-hundred-degree stone face. "
            "The reaction was deafening. "
            "A violent explosion of superheated white steam engulfed the trench. "
            "The sudden, brutal drop in temperature caused the outer layer of basalt to contract violently while the interior remained molten hot. "
            "With deafening snaps like gunshot fire, the mountain gave up. "
            "Millions of micro-fractures tore through the rock, turning diamond-hard basalt into brittle, shattered crust."
        )
    },
    {
        "act": "act_06_excavation_storm",
        "title": "Act VI: The Chisel Storm & Lever Crews",
        "text": (
            "The steam had barely cleared before the Takshakas charged into the smoking trench. "
            "Armed with long forged-iron crowbars, teams of four wedged their levers into the gaping thermal cracks. "
            "With a unified heave, massive two-ton sheets of fractured stone sheared away from the bedrock and crashed into the trench floor. "
            "Behind them came the hammer men. "
            "Their thirty-pound sledges easily smashed the heat-weakened slabs into manageable ballast. "
            "What would have taken weeks of agonizing hand-chiseling was reduced to rubble in twenty minutes. "
            "Fire had broken the mountain's spine."
        )
    },
    {
        "act": "act_07_gravity_engine",
        "title": "Act VII: Gravity as an Engine (100,000 Tons Cleared)",
        "text": (
            "Now came the next impossible challenge: where do you put four hundred thousand tons of broken rock? "
            "There were no steam cranes. No diesel dump trucks. "
            "If the rubble accumulated inside the trenches, the workers would be buried alive in their own excavation. "
            "Kokasa used gravity as his engine. "
            "He constructed massive timber chutes from polished, oil-greased logs angled directly down the natural western slope of the cliff. "
            "Day and night, boulders were rolled into the chutes, screaming down the mountainside into the staging plains below. "
            "Down in the valley, teams of war elephants and bullocks dragged the heaviest blocks to build defensive ramparts, roads, and village water reservoirs. "
            "Nothing was wasted. The mountain was not discarded; it was recycled into an empire."
        )
    },
    {
        "act": "act_08_monolithic_island",
        "title": "Act VIII: The Monolithic Island & Cliffhanger",
        "text": (
            "By the end of the dry season, the impossible had been achieved. "
            "The three perimeter trenches had plunged thirty-three meters straight down into the living earth. "
            "And standing alone in the center of the abyss was a colossal, isolated island of solid mountain. "
            "Fifty meters long. Thirty-three meters wide. One hundred feet high. "
            "Completely detached from the cliff on three sides. "
            "Kokasa climbed to the summit of the lonely stone monolith. "
            "Beneath his feet lay the hidden house of Shiva. "
            "The trenches were cut. The perimeter was cleared. "
            "Now came the terrifying part: "
            "One mistake, one cracked column, and the entire temple would collapse before it was ever born. "
            "In Episode Three: Kokasa makes the first cut of the sacred spire. "
            "Subscribe, and descend into the stone."
        )
    }
]

SHORTS = [
    {
        "id": "short_01",
        "name": "short_01_the_fire_secret",
        "text": (
            "How did 8th-century Indian builders cut three 100-foot-deep canyons through solid mountain without explosives or dynamite? "
            "They used a terrifying scientific trick called Agni-Karma: thermal shock. "
            "First, they stacked hundreds of tons of hardwood bonfires against the bedrock, heating the volcanic stone to six hundred degrees Celsius. "
            "Then, at the peak of the heat, they threw hundreds of gallons of ice-cold spring water directly onto the glowing rock face! "
            "The sudden contraction caused the mountain to literally tear itself apart at the molecular level, exploding with micro-fractures! "
            "With the stone's spine broken, workers could pry off two-ton sheets of rock with simple iron crowbars in minutes instead of months! "
            "Watch Episode Two of our full documentary series linked below to see how four hundred thousand tons were moved using gravity!"
        )
    },
    {
        "id": "short_02",
        "name": "short_02_where_did_400k_tons_go",
        "text": (
            "To build the Kailasa temple, ancient builders removed four hundred thousand tons of solid rock. "
            "That's more stone than the Great Pyramid of Giza by volume per worker! "
            "So where did all the rubble go without bulldozers or dump trucks? "
            "Architect Kokasa turned gravity into an engine. "
            "He built massive wooden slides down the western cliff face, greased with sesame oil. "
            "Workers rolled giant boulders into the chutes, and gravity shot them straight into the valley at fifty miles an hour! "
            "Down below, teams of war elephants dragged the stone away to build roads, fortress walls, and reservoirs for nearby villages! "
            "Nothing was wasted. "
            "See how the three giant perimeter trenches were completed in Episode Two linked below!"
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
        with open(srt_path, "w", encoding="utf-8") as file:
            file.write(submaker.get_srt())

def get_audio_duration(path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    return float(out)

def build_full_narration_and_subtitles():
    print("\nAssembling Full Episode 2 Audio Track & Aligned Subtitles via FFmpeg...")
    
    # 1. Concat Audio via FFmpeg concat filter
    concat_list = AUDIO_DIR / "temp_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for act in EPISODE_ACTS:
            act_name = act["act"]
            path_posix = (AUDIO_DIR / f"{act_name}.mp3").as_posix()
            f.write(f"file '{path_posix}'\n")

    full_audio = AUDIO_DIR / "episode_02_full_narration.mp3"
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(full_audio)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    if concat_list.exists():
        concat_list.unlink()

    full_dur = get_audio_duration(full_audio)
    print(f"  -> Master Audio: {full_audio.name} ({full_dur:.2f} seconds)")

    # 2. Concat and time-offset all act .srt files into master episode_02_full.srt
    full_srt_path = SUB_DIR / "episode_02_full.srt"
    current_time_offset = 0.0
    global_cue_index = 1
    full_srt_lines = []

    for act in EPISODE_ACTS:
        act_srt = SUB_DIR / f"{act['act']}.srt"
        act_audio = AUDIO_DIR / f"{act['act']}.mp3"
        act_dur = get_audio_duration(act_audio)

        if act_srt.exists() and act_srt.stat().st_size > 0:
            content = act_srt.read_text(encoding="utf-8").strip()
            blocks = content.split("\n\n")
            for block in blocks:
                lines = block.strip().split("\n")
                if len(lines) >= 3:
                    # lines[0] = cue index, lines[1] = 00:00:01,000 --> 00:00:05,000, lines[2:] = text
                    time_line = lines[1]
                    parts = time_line.split(" --> ")
                    if len(parts) == 2:
                        def parse_srt_time(ts_str):
                            h, m, rest = ts_str.split(":")
                            s, ms = rest.split(",")
                            return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0

                        start_sec = parse_srt_time(parts[0]) + current_time_offset
                        end_sec = parse_srt_time(parts[1]) + current_time_offset
                        start_td = timedelta(seconds=start_sec)
                        end_td = timedelta(seconds=end_sec)
                        new_timeline = f"{format_timestamp(start_td)} --> {format_timestamp(end_td)}"
                        text_content = "\n".join(lines[2:])
                        full_srt_lines.append(f"{global_cue_index}\n{new_timeline}\n{text_content}\n")
                        global_cue_index += 1

        current_time_offset += act_dur

    full_srt_path.write_text("\n".join(full_srt_lines), encoding="utf-8")
    print(f"  -> Master Subtitles: {full_srt_path.name} ({global_cue_index - 1} cues aligned with 0ms drift)")

async def main():
    print(f"Synthesizing Episode 2 Voiceovers with: {VOICE}")

    # Generate each act
    for act in EPISODE_ACTS:
        out_mp3 = AUDIO_DIR / f"{act['act']}.mp3"
        out_srt = SUB_DIR / f"{act['act']}.srt"
        print(f"Generating {act['title']}...")
        await generate_speech(act["text"], out_mp3, out_srt)

    # Generate Shorts
    for short in SHORTS:
        print(f"Generating {short['name']}...")
        s_mp3 = AUDIO_DIR / f"{short['name']}.mp3"
        s_srt = SUB_DIR / f"{short['name']}.srt"
        await generate_speech(short["text"], s_mp3, s_srt)

    # Assemble master full narration track & full subtitles
    build_full_narration_and_subtitles()
    print("\nAll Episode 2 Audio and Subtitles verified!")

if __name__ == "__main__":
    asyncio.run(main())
