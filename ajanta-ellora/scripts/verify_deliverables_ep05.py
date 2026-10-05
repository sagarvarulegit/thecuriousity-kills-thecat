"""Audit Episode 05 non-image/non-video deliverables."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "episode05"
AUDIO, SUBS, SCRIPT, KIT = (ROOT / x for x in ("audio", "subtitles", "script_and_storyboard", "publish_kit"))

def seconds(ts: str) -> float:
    h, m, rest = ts.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)

def cues(path: Path):
    blocks = path.read_text(encoding="utf-8-sig").strip().split("\n\n")
    parsed = []
    for block in blocks:
        rows = block.splitlines()
        assert len(rows) >= 3 and rows[0].isdigit() and " --> " in rows[1], f"Malformed cue in {path}"
        a,b = rows[1].split(" --> ")
        start,end = seconds(a),seconds(b)
        assert start < end, f"Non-positive cue duration in {path}: {rows[1]}"
        parsed.append((start,end," ".join(rows[2:])))
    assert all(parsed[i][0] >= parsed[i-1][0] and parsed[i][0] >= parsed[i-1][1] - .011 for i in range(1,len(parsed))), f"Non-monotonic/overlapping cues in {path}"
    return parsed

def audio_duration(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)], text=True).strip())

def decode_audio(path: Path) -> None:
    subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],check=True,capture_output=True)

def main():
    assert SCRIPT.joinpath("episode-05-the-elephants-beneath-kailasa.md").is_file()
    assert AUDIO.joinpath("sound_design_cue_sheet.md").is_file()
    assert KIT.joinpath("master_publish_kit.md").is_file()
    act_srts = sorted(SUBS.glob("act_*.srt"))
    act_audio = sorted(AUDIO.glob("act_*.mp3"))
    assert len(act_srts) == len(act_audio) == 8, "Expected eight act audio/SRT pairs"
    for srt, audio in zip(act_srts, act_audio):
        parsed = cues(srt)
        assert parsed and parsed[-1][1] <= audio_duration(audio) + .15, f"Subtitle exceeds act audio: {srt.name}"
        decode_audio(audio)
    full_srt = cues(SUBS / "episode_05_full.srt")
    master_audio = AUDIO / "episode_05_full_narration.mp3"
    master_dur = audio_duration(master_audio)
    decode_audio(master_audio)
    assert full_srt[-1][1] <= master_dur + .15, "Full subtitles exceed master narration"
    for stem in ("short_01_the_elephants_that_carry_a_temple", "short_02_why_elephants_support_the_mountain"):
        assert (AUDIO / f"{stem}.mp3").is_file() and (SUBS / f"{stem}.srt").is_file()
        short_audio = AUDIO / f"{stem}.mp3"
        assert cues(SUBS / f"{stem}.srt")[-1][1] <= audio_duration(short_audio) + .15
        decode_audio(short_audio)
        kit = next(KIT.glob(f"{stem}_publish_kit.md"))
        text = kit.read_text(encoding="utf-8")
        match = re.search(r"## SEO tags \((\d+) characters\)\n```text\n(.*?)\n```", text, re.S)
        assert match and len(match.group(2)) == int(match.group(1)) < 500, f"Invalid tags in {kit.name}"
        assert not re.search(r"\b(?:Episode|Ep\.)\s*0?5\b", text, re.I), f"Episodic marker in Shorts kit: {kit.name}"
    kit_text = (KIT / "master_publish_kit.md").read_text(encoding="utf-8")
    match = re.search(r"## SEO tags \((\d+) characters\)\n```text\n(.*?)\n```", kit_text, re.S)
    assert match and len(match.group(2)) == int(match.group(1)) < 500, "Invalid master tags"
    storyboard = (SCRIPT / "episode-05-the-elephants-beneath-kailasa.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^### Beat \d+", storyboard, re.M)) == 72, "Expected 72 sentence-level storyboard beats"
    print("PASS: 8 act narration/SRT pairs, full master audio/SRT, 2 Shorts, 3 publish kits, sentence-level storyboard, tags under 500 characters, and FFmpeg audio decode.")
    print(f"Master narration: {master_dur:.2f}s ({master_dur/60:.2f} min); full cues: {len(full_srt)}")

if __name__ == "__main__":
    main()
