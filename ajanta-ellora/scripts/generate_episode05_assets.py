"""Build Episode 05's non-image/non-video production assets.

Run from any directory with edge-tts and FFmpeg/ffprobe installed:
    python ajanta-ellora/scripts/generate_episode05_assets.py

Narration and sentence-level subtitle timing are synthesized from the same
authoritative script. No images or videos are created by this script.
"""
from __future__ import annotations

import asyncio
import re
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episode05"
AUDIO, SUBS = EP / "audio", EP / "subtitles"
SCRIPT, KIT = EP / "script_and_storyboard", EP / "publish_kit"
VOICE = "en-US-ChristopherNeural"

# Sentence-level narration. Each act is timed from its synthesized speech.
ACTS = [
    ("act_01_the_animals_beneath", "Act I — The Animals Beneath", [
        "Look beneath the temple.",
        "Along Kailasa’s raised base, elephants emerge from the dark stone, shoulder to shoulder beneath a monumental ledge.",
        "At first glance, they seem to hold the entire temple above the ground.",
        "But the image asks a question that the architecture answers in a more surprising way.",
        "Are these animals carrying the building, or showing us how to see it?",
        "At Ellora, the answer begins with a distinction between what stone does and what sculpture makes us feel.",
        "The elephants are carved into the temple’s lower storey; the temple itself remains part of a vast rock-cut composition.",
        "Today, we follow the plinth from its carved animals to the meaning of a mountain made to appear lifted.",
        "The mystery is not whether the elephants are beautiful, but why the temple seems to need them.",
    ]),
    ("act_02_a_mountain_as_temple", "Act II — A Mountain as Temple", [
        "Kailasa is Cave Sixteen at Ellora, a Hindu monument cut from the basalt hillside.",
        "Rather than assemble a temple from blocks, its builders released a freestanding complex from the surrounding rock.",
        "The main shrine rises at the center of a court, with a gateway, Nandi pavilion, halls, and subsidiary shrines arranged around it.",
        "The plinth is the elevated base beneath the principal temple, setting the shrine above the court floor.",
        "Its surfaces are not blank foundations: they carry a dense sculptural program that continues around the building.",
        "The base therefore has two jobs for the visitor’s eye: it establishes height and gives that height a living edge.",
        "Rows of figures, animals, and patterned bands turn the transition from earth to temple into an experience.",
        "The monument does not simply stand in the landscape; it stages how we encounter its mass.",
        "To understand the elephants, we first need to see the plinth as architecture and image at once.",
    ]),
    ("act_03_reading_the_plinth", "Act III — Reading the Plinth", [
        "Walk your attention along the lower storey.",
        "Sahapedia describes elephants gathering lotus flowers in their trunks, deeply carved beneath the high basement.",
        "The animals are not isolated ornaments placed on a modern-looking facade.",
        "They belong to a continuous sculpted zone that wraps the base with elephants, lions, and other figures.",
        "The scale and relief make the band legible from the court, even as its details reward a closer look.",
        "Some trunks are damaged, and weathering changes what survives; the sculpture we see is not an untouched original surface.",
        "A historic account also described a herd bearing the temple, an image captured by the composition itself.",
        "That description tells us what the carving makes visible, not a hidden engineering report from the builders.",
        "The first clue is visual: the animals create a living threshold between the ground and the sacred structure above.",
    ]),
    ("act_04_the_illusion_of_support", "Act IV — The Illusion of Support", [
        "Now look at the line where the plinth meets the temple mass.",
        "The elephants appear to push upward, their backs aligned beneath the projecting base.",
        "This is a powerful sculptural convention: the building seems to rest on a procession of living bodies.",
        "Yet at Kailasa, these elephants are carved in relief on the lower storey, within the same rock-cut monument.",
        "They are not a row of freestanding columns secretly holding a separate building aloft.",
        "The rock-cut core and plinth carry the architectural mass; the figures shape how that mass is imagined.",
        "That does not make the sculpture less important. It makes its work more precise.",
        "The animal band transforms a heavy base into a scene of effort, movement, and upward force.",
        "A stone temple can feel weightless for a moment because its base shows weight being carried.",
    ]),
    ("act_05_animals_and_the_sacred_mountain", "Act V — Animals and the Sacred Mountain", [
        "The temple’s name and design point toward Kailasa, Shiva’s sacred mountain.",
        "The building’s rising form turns that mountain association into architecture, with the central shrine as its summit.",
        "An older interpretation by Havell compared the elephants at the base to rain clouds beneath Himalayan peaks.",
        "In that reading, elephants evoke clouds gathering below a mountain, making the temple appear borne above them.",
        "It is an evocative interpretation, not a certainty that the original sculptors left us in writing.",
        "Other readings emphasize royal power, auspicious abundance, or the familiar image of elephants supporting a cosmic mountain.",
        "The surviving carving alone cannot choose one meaning for every viewer or every figure.",
        "What we can say securely is that the animals and the mountain form a deliberate visual relationship.",
        "The plinth makes the sacred mountain seem animated at its base.",
    ]),
    ("act_06_one_stone_many_images", "Act VI — One Stone, Many Images", [
        "There is a paradox here: the elephants look like separate creatures, but the monument is rock-cut.",
        "The sculptor has made the basalt read as bodies, folds, legs, and patterned surfaces.",
        "At a distance, the repeating animals form a band beneath the temple.",
        "Up close, each figure can interrupt that repetition with its own pose and detail.",
        "This shift between a unified procession and individual bodies is part of the carving’s visual intelligence.",
        "We should not invent a workshop sequence or claim every sculptural detail was carved in a known order.",
        "The finished stone lets us study form and placement, while leaving many production choices undocumented.",
        "A single rock mass can become architecture, ornament, and an imagined procession at the same time.",
        "The temple’s unity does not flatten its images; it gives them a shared ground.",
    ]),
    ("act_07_the_viewer_completes_the_image", "Act VII — The Viewer Completes the Image", [
        "The plinth is also something you move past.",
        "From the courtyard, the raised base lifts the temple above eye level and gives the main shrine a commanding presence.",
        "As you walk, the relief appears in changing fragments: an elephant, a lion, a repeated band, then the larger mass above.",
        "The viewer connects those partial views into an imagined ring of animals around the building.",
        "This is why the sculpture works at more than one scale.",
        "Its repetition binds the base together, while its details invite a slower encounter.",
        "The temple’s height feels physical, but the carved creatures make that height feel supported and alive.",
        "The image is completed not by a mechanical trick, but by the meeting of stone, viewpoint, and movement.",
        "Kailasa turns looking into a small act of discovery.",
    ]),
    ("act_08_beneath_the_mountain", "Act VIII — Beneath the Mountain", [
        "Return to the elephants beneath the plinth.",
        "They do not reveal a concealed system of animal-shaped pillars.",
        "They reveal a sculptural decision: make the base of a sacred mountain appear to move and bear weight.",
        "The architecture gives the temple its mass; the figures give that mass a story the eye can follow.",
        "Some meanings remain open, and that uncertainty is part of reading a monument honestly.",
        "At Kailasa, a mountain was not only cut into a temple; it was made to seem alive around its edges.",
        "Next, we leave the plinth and turn toward the stories carved across the temple walls.",
        "What happens when a whole epic is translated into stone panels around a sacred court?",
        "That is the next mystery waiting at Kailasa.",
    ]),
]

SHORTS = [
    ("short_01_the_elephants_that_carry_a_temple", "The Elephants Beneath Kailasa", [
        "Look beneath the Kailasa Temple at Ellora.",
        "A carved procession of elephants seems to hold the temple above the ground.",
        "But these figures are sculpted into the lower storey; they are not separate pillars carrying a building.",
        "The rock-cut plinth supports the architecture, while the elephants make that weight feel alive.",
        "The stone does the structural work. The sculpture gives the mountain a story.",
    ]),
    ("short_02_why_elephants_support_the_mountain", "Why Put Elephants Under a Mountain?", [
        "Why are elephants carved beneath Kailasa Temple’s raised base?",
        "They appear to bear the temple on their backs, turning its plinth into a living procession.",
        "One older interpretation compared the elephants to clouds gathered beneath a Himalayan peak.",
        "That is a compelling reading, but not a proven statement of the sculptors’ intent.",
        "What the carving shows clearly is a sacred mountain made to feel animated at its base.",
    ]),
]

VISUALS = [
    "Begin low at the plinth and reveal the carved elephant band beneath the temple; no generated imagery is included in this package.",
    "Orient the viewer with a simple, dimension-free plan of Kailasa court and central shrine.",
    "Study the sculpted lower storey, with close attention to elephant relief and surviving damage.",
    "Use a restrained diagram distinguishing the continuous rock-cut plinth from the sculpted relief; label interpretation clearly.",
    "Pair the rising temple silhouette with a clearly attributed note that the cloud reading is an older interpretation.",
    "Move from a broad view of the frieze to a detail study, without asserting undocumented carving steps.",
    "Trace a viewer’s path along the court and show how the relief is encountered in changing fragments.",
    "Return to the plinth, then hand off toward narrative panels for Episode 06.",
]
SOUND = [
    "Open-air courtyard ambience, restrained low drone; gentle tonal reveal as the elephant band appears.",
    "Light strings and open ambience; no faux-temple bells or generic exoticized cues.",
    "Quiet, close stone texture under the voice; keep the atmosphere spacious.",
    "Subtle low pulse as the support illusion is explained; no cracking or invented structural stress sounds.",
    "Warm, contemplative strings; leave space around the distinction between evidence and interpretation.",
    "Sparse, dry ambience with a soft transition between wide pattern and close detail.",
    "Measured, gently moving motif suggesting a walk through the courtyard, without literalized footsteps.",
    "Return to the opening motif; resolve into a restrained teaser for the next episode.",
]

def stamp(seconds: float) -> str:
    ms = max(0, round(seconds * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def clock(seconds: float) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02}:{s:02}"

def duration(path: Path) -> float:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], text=True)
    return float(out.strip())

def write_srt(cues: list[tuple[float, float, str]], path: Path) -> None:
    path.write_text("\n\n".join(f"{i}\n{stamp(a)} --> {stamp(b)}\n{text}" for i, (a,b,text) in enumerate(cues, 1)) + "\n", encoding="utf-8")

async def synthesize(text: str, path: Path) -> list[tuple[float, float, str]]:
    maker = edge_tts.SubMaker()
    with path.open("wb") as f:
        async for chunk in edge_tts.Communicate(text, VOICE, rate="-4%", pitch="-2Hz").stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                maker.feed(chunk)
    raw = maker.get_srt()
    timed = []
    for block in raw.strip().split("\n\n"):
        lines = block.splitlines()
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        def parse(t: str) -> float:
            hh, mm, rem = t.strip().replace(",", ".").split(":")
            return int(hh)*3600 + int(mm)*60 + float(rem)
        a, b = [parse(x) for x in lines[1].split("-->")]
        timed.append((a,b))
    sentences = [x.strip() for x in re.findall(r"[^.!?]+[.!?]+(?:[’'\"])?", text)]
    if len(timed) != len(sentences):
        raise RuntimeError(f"Sentence timing mismatch in {path.name}: {len(timed)} timed, {len(sentences)} source")
    cues = []
    for (a,b), sentence in zip(timed, sentences):
        if cues and a < cues[-1][1]:
            pa,pb,pt = cues[-1]
            cues[-1] = (pa, max(pa + .1, a - .01), pt)
        cues.append((a,b,sentence))
    return cues

async def main() -> None:
    for folder in (AUDIO, SUBS, SCRIPT, KIT):
        folder.mkdir(parents=True, exist_ok=True)
    master_cues, narration, act_starts = [], [], []
    offset = 0.0
    lines = [
        "# Episode 05 — The Elephants Beneath Kailasa",
        "### Why the temple appears to rise on a living procession",
        "",
        "**Series:** Kailasa: The Mountain Carved From Above  ",
        "**Format:** 16:9 documentary; act timings are measured from synthesized narration.  ",
        "**Evidence note:** The lower storey is carved with elephants and lions, and the elephant relief appears to support the basement. Do not describe the elephants as freestanding structural columns. An older cloud-and-mountain interpretation is attributed and presented as interpretation, not settled intent.  ",
        "**Assets:** No images or videos are generated. Visual briefs are planning notes only; narration, audio, subtitles, sound cues, and publishing kits are included.",
        "", "## Story and pacing", "", "| Act | Timing | Story turn |", "|---|---:|---|",
    ]
    all_cues = []
    shorts_meta = []
    for i, (slug,title,sentences) in enumerate(ACTS):
        act_starts.append(offset)
        aud = AUDIO / f"{slug}.mp3"
        cues = await synthesize(" ".join(sentences), aud)
        write_srt(cues, SUBS / f"{slug}.srt")
        dur = duration(aud)
        lines.append(f"| {title} | {clock(offset)} | {title.split('—',1)[1].strip()} |")
        lines += ["", f"## {title}", ""]
        for j, sentence in enumerate(sentences):
            a,b,_ = cues[j]
            lines += [f"### Beat {sum(len(x[2]) for x in ACTS[:i]) + j + 1:02d} — {clock(offset+a)}–{clock(offset+b)}",
                      f"- **Narration:** {sentence}", f"- **Visual brief (not generated):** {VISUALS[i]}",
                      f"- **Sound cue:** {SOUND[i]}", ""]
            all_cues.append((offset+a, offset+b, sentence))
        narration.extend(sentences)
        offset += dur

    master = AUDIO / "episode_05_full_narration.mp3"
    concat = AUDIO / "_episode05_concat.txt"
    concat.write_text("".join(f"file '{(AUDIO / (x[0] + '.mp3')).as_posix()}'\n" for x in ACTS), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(master)], check=True, capture_output=True)
    concat.unlink()
    write_srt(all_cues, SUBS / "episode_05_full.srt")

    short_cue_data = []
    for slug,title,sentences in SHORTS:
        aud = AUDIO / f"{slug}.mp3"
        cues = await synthesize(" ".join(sentences), aud)
        write_srt(cues, SUBS / f"{slug}.srt")
        short_cue_data.append((slug,title,duration(aud),sentences))

    lines += ["## Narration transcript", "", *narration, "", "## Sources and interpretive limits", "",
        "- Sahapedia, [The Architecture of Ellora Caves](https://www.sahapedia.org/the-architecture-of-ellora-caves): Cave 16 plan and the elephants gathering lotus flowers on the lower storey.",
        "- Impart Encyclopedia of Art, [Kailasanatha Temple, Ellora](https://imp-art.org/articles/kailasanatha-temple-ellora/): monolithic form, sculptural plinth, and architectural context.",
        "- E. B. Havell, [The Himalayas in Indian Art](https://ignca.gov.in/Asi_data/39131.pdf), p. 27: an older interpretation comparing the plinth elephants to rain clouds beneath a sacred mountain. This is presented as interpretation, not proven original intent.",
        "", "The stonework supports a description of the carved figures and their placement. It does not provide a definitive written key to every symbolic meaning or a claim that the relief figures are freestanding structural supports.", ""]
    (SCRIPT / "episode-05-the-elephants-beneath-kailasa.md").write_text("\n".join(lines), encoding="utf-8")

    sound = ["# Episode 05 Sound Design Cue Sheet", "", "**Mix intent:** Keep narration forward and the courtyard spacious. Music supports the visual shift between architectural mass and animated relief; no cue implies undocumented historical sounds.", "", "| Act | In point | Ambience / score / foley |", "|---|---:|---|"]
    for (_,title,_), start, cue in zip(ACTS, act_starts, SOUND):
        sound.append(f"| {title} | {clock(start)} | {cue} |")
    sound += ["", "## Mix notes", "", "- Duck music beneath every spoken line and keep the opening courtyard ambience consistent with Episode 04.", "- Avoid faux-temple bells, generic exoticized palettes, and dramatic stone stress or collapse effects.", "- Treat all stone texture as editorial sound design, not historical field recording.", "- Let the final motif bridge into the next episode’s focus on narrative sculpture.", ""]
    (AUDIO / "sound_design_cue_sheet.md").write_text("\n".join(sound), encoding="utf-8")

    chapters = [f"{clock(t)} - {title.split('—',1)[1].strip()}" for (_,title,_),t in zip(ACTS,act_starts)]
    tags = "Kailasa Temple,Ellora Caves,Cave 16,Ellora architecture,rock cut temple,monolithic temple,elephant sculptures,Indian sculpture,Rashtrakuta,Shiva temple,Deccan art,Indian history documentary,temple architecture"
    desc = "At Ellora’s Kailasa Temple, a procession of carved elephants runs beneath the raised plinth. They appear to carry the temple, but the relief figures are part of the rock-cut lower storey, not freestanding pillars. This episode looks at how sculpture gives architectural weight a vivid, living image—and separates what the stone shows from interpretations of what it may mean.\n\n" + "\n".join(chapters)
    (KIT / "master_publish_kit.md").write_text(f"""# YouTube Publish Kit — Episode 05: The Elephants Beneath Kailasa

## Title options
1. Why Are Elephants Carved Beneath Kailasa Temple?
2. The Elephants That Seem to Carry a Mountain
3. What the Kailasa Temple’s Elephant Plinth Really Shows
4. A Temple Raised on Elephants? The Sculpture at Ellora Explained
5. The Living Base of Kailasa Temple

## Description
{desc}

## SEO tags ({len(tags)} characters)
```text
{tags}
```

## Pinned comment
Do the elephants feel like structural supports, sacred imagery, or both when you stand before the plinth? Tell us what you notice—and where you draw the line between evidence and interpretation.

## Thumbnail brief (not generated)
16:9 low-angle view of the plinth elephant relief beneath the temple mass; clear contrast between animal band and towering stone above. Maximum three-word text: “CARRIED BY ELEPHANTS?” Keep the question mark and avoid implying literal free-standing supports.
""", encoding="utf-8")

    for i,(slug,title,dur,sentences) in enumerate(short_cue_data,1):
        short_tags = "Kailasa Temple,Ellora Caves,elephant sculpture,Indian art,rock cut temple,history shorts"
        short_desc = " ".join(sentences)
        (KIT / f"{slug}_publish_kit.md").write_text(f"""# YouTube Publish Kit — Short {i}: {title}

## Title options
1. {title}
2. The Elephants Beneath Kailasa Temple
3. Why Elephants Appear to Carry This Temple
4. What the Kailasa Plinth Really Shows
5. A Mountain Made to Look Alive

## Description
{short_desc}

Watch the full episode: The Elephants Beneath Kailasa (add the episode link after upload).

## SEO tags ({len(short_tags)} characters)
```text
{short_tags}
```

## Pinned comment
Watch the full episode for the architectural evidence and different interpretations of the plinth: [add link after upload].

## Thumbnail / cover brief (not generated)
Vertical close crop of the carved elephant band and projecting plinth above; keep text to “CARRIED?” and do not suggest separate structural pillars.
""", encoding="utf-8")

    print(f"Episode 05 assets written to {EP}")
    print(f"Narration duration: {duration(master):.2f}s; storyboard beats: {sum(len(a[2]) for a in ACTS)}")
    for slug,title,dur,_ in short_cue_data:
        print(f"{slug}: {dur:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
