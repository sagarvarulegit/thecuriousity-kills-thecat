#!/usr/bin/env python3
"""
synthesize_ep05_hindi_narration.py — ElevenLabs Hindi Narration Synthesizer & Audio Track Builder
Synthesizes Episode 05 narration in high-register documentary Hindi using ElevenLabs API.
Extracts millisecond-accurate timestamps using /with-timestamps endpoint.
Generates:
1. 8 individual Hindi Act MP3s with exact duration tracking in audio_hindi/
2. Perfectly monotonic, non-overlapping Devanagari .srt subtitles in subtitles_hindi/
3. Master Hindi narration stem with <= 10.0 ms concatenation drift
4. Full YouTube-ready Hindi Audio Track (episode_05_hindi_track.m4a) mixed with ducked orchestral bed (-16 LUFS)
"""

import os
import re
import sys
import json
import base64
import requests
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP05_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode05"
AUDIO_HINDI_DIR = EP05_DIR / "audio_hindi"
SUB_HINDI_DIR = EP05_DIR / "subtitles_hindi"
FINAL_VIDEOS_DIR = EP05_DIR / "final_videos"
SCRIPTS_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "scripts"

AUDIO_HINDI_DIR.mkdir(parents=True, exist_ok=True)
SUB_HINDI_DIR.mkdir(parents=True, exist_ok=True)

# Voice: Adam Stone (auq43ws1oslv0tO4BDa7) with eleven_multilingual_v2
VOICE_ID = "auq43ws1oslv0tO4BDa7"
MODEL_ID = "eleven_multilingual_v2"

def get_api_key() -> str:
    env_p = WORKSPACE_ROOT / ".env"
    if env_p.exists():
        lines = env_p.read_text(encoding="utf-8").splitlines()
        for l in lines:
            if l.startswith("ELEVEN_LABS_API_KEY=") or l.startswith("ELEVENLABS_API_KEY="):
                return l.split("=", 1)[1].strip()
    key = os.getenv("ELEVEN_LABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVEN_LABS_API_KEY not found in .env or environment!")
    return key

# The 8 Acts with exact sentence cues matching the 72 micro-beats in Hindi
HINDI_ACTS_DATA = [
    {
        "id": "act_01_the_animals_beneath",
        "title": "Act I — नींव के जीवंत प्रहरी",
        "sentences": [
            "मंदिर के आधार को देखिए।",
            "कैलाश मंदिर के उठे हुए अधिष्ठान पर, काले बेसाल्ट पत्थर से कंधे से कंधा मिलाए विशाल हाथी उभरते हैं।",
            "पहली नज़र में लगता है मानो वे पूरे मंदिर को ज़मीन से ऊपर थामे हुए हैं।",
            "लेकिन यह दृश्य एक ऐसा सवाल खड़ा करता है, जिसका जवाब यह वास्तुकला और भी हैरान करने वाले अंदाज़ में देती है।",
            "क्या ये जीव सचमुच इस इमारत का बोझ उठाए हुए हैं, या हमें इसे देखने का एक नया नज़रिया दे रहे हैं?",
            "एलोरा में, इसका उत्तर पत्थर की वास्तविक क्षमता और मूर्तिकला के अहसास के बीच के अंतर से शुरू होता है।",
            "ये हाथी मंदिर के निचले तल में तराशे गए हैं; और स्वयं मंदिर एक विशाल एकाश्मक शैल-कृत रचना का अभिन्न अंग है।",
            "आज, हम इस अधिष्ठान के तराशे गए जीवों से लेकर, उस रहस्य को समझेंगे जिसके कारण यह पर्वत आकाश में उठता हुआ प्रतीत होता है।",
            "रहस्य यह नहीं है कि ये हाथी कितने सुंदर हैं, बल्कि यह है कि मंदिर को आखिर इनकी ज़रूरत क्यों महसूस हुई।"
        ]
    },
    {
        "id": "act_02_a_mountain_as_temple",
        "title": "Act II — मंदिर के रूप में खड़ा पर्वत",
        "sentences": [
            "इस आधार के असली उद्देश्य को समझने के लिए, खुले प्रांगण में थोड़ा पीछे हटिए।",
            "कैलाश मंदिर का निर्माण ज़मीन से पत्थर के खंड जोड़कर ऊपर की ओर नहीं किया गया था।",
            "शिल्पकारों ने बेसाल्ट चट्टान में ऊपर से नीचे की ओर खाई काटी, एक ही विशाल शिलाखंड को अलग किया, और ऊपर से मंदिर को तराशते चले गए।",
            "अधिष्ठान मुख्य मंदिर के नीचे का वह ऊंचा चबूतरा है, जो गर्भगृह को प्रांगण के फर्श से काफी ऊपर स्थापित करता है।",
            "इसकी सतहें केवल सपाट नींव नहीं हैं: उन पर चारों ओर निरंतर फैली हुई मूर्तियों की एक समृद्ध श्रृंखला मौजूद है।",
            "इसलिए दर्शक की दृष्टि के लिए इस आधार के दो कार्य हैं: यह ऊंचाई स्थापित करता है और उस ऊंचाई को एक जीवंत रूप देता है।",
            "मूर्तियों, जानवरों और नक्काशीदार पट्टियों की कतारें ज़मीन से मंदिर के इस जुड़ाव को एक विस्मयकारी अनुभव में बदल देती हैं।",
            "यह स्मारक केवल भूभाग पर खड़ा नहीं है; बल्कि यह तय करता है कि हम इसके विराट स्वरूप को कैसे महसूस करें।",
            "इन हाथियों को समझने के लिए, हमें पहले इस अधिष्ठान को वास्तुकला और दृश्य कला के संयुक्त रूप में देखना होगा।"
        ]
    },
    {
        "id": "act_03_reading_the_plinth",
        "title": "Act III — अधिष्ठान का गहन अध्ययन",
        "sentences": [
            "अपनी दृष्टि को निचले तल के साथ-साथ आगे बढ़ाइए।",
            "ऐतिहासिक विवरणों में इस ऊंचे तल के नीचे हाथियों को अपनी सूंड में कमल के फूल समेटे हुए गहराई से तराशा गया बताया गया है।",
            "ये जीव किसी आधुनिक अग्रभाग पर सजाए गए अलग-थलग आभूषण नहीं हैं।",
            "वे एक अखंड नक्काशीदार पट्टी का हिस्सा हैं, जो हाथियों, सिंहों और अन्य आकृतियों के साथ पूरे आधार को घेरे हुए है।",
            "इसका विशाल पैमाना और उभार इसे प्रांगण से भी स्पष्ट दिखाते हैं, जबकि पास से देखने पर इसकी बारीकियाँ चकित कर देती हैं।",
            "कुछ सूंडें खंडित हैं और समय की मार ने इनके स्वरूप को बदला है; आज हम जो देखते हैं वह बिल्कुल अछूती मूल सतह नहीं है।",
            "ऐतिहासिक वृत्तांतों में भी एक झुंड द्वारा मंदिर को धारण करने का उल्लेख मिलता है, जो इस रचना के प्रभाव को दर्शाता है।",
            "यह विवरण हमें बताता है कि नक्काशी क्या दिखाती है, न कि यह निर्माताओं की कोई गुप्त इंजीनियरिंग रिपोर्ट है।",
            "पहला संकेत दृश्य है: ये जीव भूमि और ऊपर की पवित्र संरचना के बीच एक सजीव देहरी का निर्माण करते हैं।"
        ]
    },
    {
        "id": "act_04_the_illusion_of_support",
        "title": "Act IV — भार वहन का दृष्टि-भ्रम",
        "sentences": [
            "अब उस रेखा को देखिए जहां अधिष्ठान मंदिर के मुख्य ढांचे से मिलता है।",
            "हाथी ऊपर की ओर जोर लगाते प्रतीत होते हैं, उनकी पीठ बाहर निकले हुए आधार के ठीक नीचे संरेखित है।",
            "यह मूर्तिकला की एक शक्तिशाली परंपरा है: ऐसा लगता है मानो इमारत जीवित शरीरों की एक शोभायात्रा पर टिकी है।",
            "फिर भी कैलाश में, ये हाथी उसी एकाश्मक स्मारक के भीतर, निचले तल पर उभारदार नक्काशी में उकेरे गए हैं।",
            "वे स्वतंत्र खंभों की कोई कतार नहीं हैं जो किसी अलग इमारत को गुप्त रूप से ऊपर थामे हुए हों।",
            "चट्टान का मूल आंतरिक भाग और अधिष्ठान ही संरचनात्मक भार उठाते हैं; जबकि ये मूर्तियाँ इस भार की केवल कल्पना कराती हैं।",
            "यह बात इन मूर्तियों के महत्व को कम नहीं करती।",
            "बल्कि यह उनके कलात्मक उद्देश्य को और अधिक सटीक बनाती है।",
            "यह पशु-शृंखला एक भारी-भरकम आधार को निरंतर प्रयास, गति और ऊपर उठते हुए बल के दृश्य में बदल देती है।",
            "एक भारी पाषाण मंदिर भी कुछ पलों के लिए भारहीन महसूस हो सकता है, क्योंकि इसका आधार भार उठाए जाने का आभास कराता है।"
        ]
    },
    {
        "id": "act_05_animals_and_the_sacred_mountain",
        "title": "Act V — पशु और पवित्र पर्वत कैलाश",
        "sentences": [
            "मंदिर का नाम और स्वरूप भगवान शिव के पवित्र पर्वत, कैलाश की ओर संकेत करते हैं।",
            "इमारत का ऊपर उठता आकार पर्वत की इस अवधारणा को वास्तुकला में ढालता है, जिसका केंद्रीय शिखर पर्वत-शृंग जैसा है।",
            "कला मर्मज्ञ हैवेल की एक प्राचीन व्याख्या में आधार के हाथियों की तुलना हिमालयी चोटियों के नीचे घिरते वर्षा-मेघों से की गई थी।",
            "उस दृष्टिकोण के अनुसार, हाथी पर्वत के नीचे एकत्र बादलों का प्रतीक हैं, जिससे मंदिर उनके ऊपर तैरता हुआ प्रतीत होता है।",
            "यह एक अत्यंत सम्मोहक व्याख्या है, हालांकि मूल शिल्पकारों ने इसका कोई लिखित प्रमाण नहीं छोड़ा।",
            "अन्य व्याख्याएं राजसी शक्ति, मांगलिक समृद्धि या ब्रह्मांडीय पर्वत को सहारा देते दिग्गजों की पारंपरिक छवि पर बल देती हैं।",
            "केवल बची हुई नक्काशी हर दर्शक या हर मूर्ति के लिए कोई एक निश्चित अर्थ तय नहीं कर सकती।",
            "हम निश्चित रूप से केवल इतना कह सकते हैं कि इन जीवों और पर्वत के बीच एक सुविचारित दृश्य संबंध है।",
            "यह अधिष्ठान पवित्र पर्वत को अपने आधार पर अत्यंत जीवंत और गतिशील बना देता है।"
        ]
    },
    {
        "id": "act_06_one_stone_many_images",
        "title": "Act VI — एक शिला, अनेक छवियां",
        "sentences": [
            "यहाँ एक अनोखा विरोधाभास है: हाथी अलग-अलग जीव दिखाई देते हैं, लेकिन पूरा स्मारक एक ही अखंड चट्टान से कटा है।",
            "मूर्तिकार ने कठोर बेसाल्ट को सजीव शरीरों, सिलवटों, पैरों और नक्काशीदार सतहों के रूप में रूपांतरित कर दिया है।",
            "दूर से देखने पर, ये दोहराए गए जीव मंदिर के नीचे एक समरूप पट्टी बनाते हैं।",
            "लेकिन पास जाने पर, प्रत्येक आकृति अपनी विशिष्ट मुद्रा और विवरण के साथ उस एकरसता को तोड़ती है।",
            "एक समूची शोभायात्रा और व्यक्तिगत शरीरों के बीच का यह संतुलन इस शिल्पकला की अद्भुत प्रतिभा को दर्शाता है।",
            "हमें किसी मनगढ़ंत कार्यशाला क्रम की कल्पना नहीं करनी चाहिए और न ही यह दावा करना चाहिए कि सब कुछ एक ज्ञात क्रम में गढ़ा गया था।",
            "तराशा गया पाषाण हमें इसके रूप और स्थान का अध्ययन करने देता है, जबकि निर्माण के कई रहस्य आज भी अलिखित हैं।",
            "एक ही विशाल चट्टान एक साथ वास्तुकला, आभूषण और एक काल्पनिक शोभायात्रा का रूप धारण कर सकती है।",
            "मंदिर की अखंडता इसकी छवियों को धुंधला नहीं करती; बल्कि उन्हें एक साझा आधार प्रदान करती है।"
        ]
    },
    {
        "id": "act_07_the_viewer_completes_the_image",
        "title": "Act VII — दर्शक की दृष्टि से पूर्ण होता दृश्य",
        "sentences": [
            "यह अधिष्ठान एक ऐसी संरचना भी है जिसके पास से होकर आप गुजरते हैं।",
            "प्रांगण से देखने पर, यह ऊंचा आधार मंदिर को आँखों के स्तर से ऊपर उठाता है और मुख्य देवालय को एक भव्य गरिमा देता है।",
            "जैसे-जैसे आप आगे बढ़ते हैं, नक्काशी टुकड़ों में प्रकट होती है: कभी एक हाथी, कभी एक सिंह, एक कतार, और फिर ऊपर का विराट ढांचा।",
            "दर्शक अपनी कल्पना में उन आंशिक दृश्यों को जोड़कर इमारत के चारों ओर हाथियों का एक पूर्ण चक्र बना लेता है।",
            "यही कारण है कि यह शिल्पकला एक से अधिक पैमानों पर अपना प्रभाव छोड़ती है।",
            "इसकी निरंतरता आधार को एक सूत्र में बांधती है, जबकि इसके सूक्ष्म विवरण ठहरकर देखने को विवश करते हैं।",
            "मंदिर की ऊंचाई भौतिक रूप से महसूस होती है, लेकिन ये तराशे गए जीव उस ऊंचाई को सहारा और जीवन प्रदान करते हैं।",
            "यह दृश्य किसी यांत्रिक तकनीक से नहीं, बल्कि पत्थर, दृष्टिकोण और दर्शक की गति के संगम से पूर्ण होता है।",
            "कैलाश मंदिर केवल देखने को भी खोज की एक आध्यात्मिक यात्रा में बदल देता है।"
        ]
    },
    {
        "id": "act_08_beneath_the_mountain",
        "title": "Act VIII — पर्वत की छाया तले",
        "sentences": [
            "अधिष्ठान के नीचे खड़े हाथियों की ओर पुनः लौटिए।",
            "वे पशु-आकार के गुप्त खंभों की किसी छिपी हुई व्यवस्था को प्रकट नहीं करते।",
            "वे एक असाधारण कलात्मक निर्णय को प्रकट करते हैं: एक पवित्र पर्वत के आधार को गतिशील और भार-वाहक दिखाना।",
            "वास्तुकला मंदिर को उसका आकार और भार देती है; जबकि ये मूर्तियाँ उस भार को एक ऐसी कहानी देती हैं जिसे आँखें पढ़ सकें।",
            "कुछ अर्थ आज भी अनसुलझे हैं, और यह अनिश्चितता किसी प्राचीन स्मारक को निष्पक्षता से समझने का ही हिस्सा है।",
            "कैलाश में, एक पर्वत को केवल मंदिर के रूप में नहीं काटा गया था; बल्कि उसके किनारों को चारों ओर से सजीव बना दिया गया था।",
            "अगली कड़ी में, हम इस अधिष्ठान को पीछे छोड़कर मंदिर की दीवारों पर उकेरी गई अमर गाथाओं की ओर बढ़ेंगे।",
            "क्या होता है जब एक संपूर्ण महाकाव्य को इस पवित्र प्रांगण की पाषाण पट्टिकाओं पर उकेर दिया जाता है?",
            "यह है कैलाश का अगला रहस्य, जो हमारा इंतज़ार कर रहा है।"
        ]
    }
]

HINDI_SHORTS_DATA = [
    {
        "id": "short_01_the_elephants_that_carry_a_temple",
        "sentences": [
            "एलोरा के कैलाश मंदिर के आधार को देखिए।",
            "तराशे गए हाथियों की एक शोभायात्रा मंदिर को ज़मीन से ऊपर थामे प्रतीत होती है।",
            "लेकिन ये आकृतियाँ निचले तल में उकेरी गई हैं; वे कोई अलग खंभे नहीं हैं।",
            "शैल-कृत अधिष्ठान वास्तुकला को सहारा देता है, जबकि हाथी उस भार को सजीव बना देते हैं।",
            "पत्थर संरचनात्मक भार वहन करता है।",
            "और यह मूर्तिकला पर्वत को एक अमर गाथा प्रदान करती है।"
        ]
    },
    {
        "id": "short_02_why_elephants_support_the_mountain",
        "sentences": [
            "कैलाश मंदिर के उठे हुए आधार के नीचे हाथी क्यों तराशे गए हैं?",
            "वे मंदिर को अपनी पीठ पर धारण करते प्रतीत होते हैं, जिससे इसका अधिष्ठान एक सजीव शोभायात्रा बन जाता है।",
            "एक प्राचीन व्याख्या में इन हाथियों की तुलना हिमालयी शिखरों के नीचे एकत्र बादलों से की गई थी।",
            "यह एक सम्मोहक दृष्टि है, हालांकि शिल्पकारों ने इसका कोई लिखित प्रमाण नहीं छोड़ा।",
            "नक्काशी स्पष्ट दिखाती है कि यह पवित्र पर्वत अपने आधार पर अत्यंत जीवंत बना दिया गया है।"
        ]
    }
]

def format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    seconds %= 3600
    m = int(seconds // 60)
    seconds %= 60
    s = int(seconds)
    ms = int(round((seconds - s) * 1000))
    if ms >= 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def synthesize_with_timestamps(text: str, api_key: str) -> Tuple[bytes, Dict[str, Any]]:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.80,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=90)
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs API Error ({resp.status_code}): {resp.text}")
    data = resp.json()
    audio_bytes = base64.b64decode(data["audio_base64"])
    return audio_bytes, data["alignment"]

def build_act_cues(sentences: List[str], full_text: str, alignment: Dict[str, Any], total_audio_dur: float) -> List[Dict[str, Any]]:
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    
    cues = []
    curr_pos = 0
    for s in sentences:
        idx = full_text.find(s, curr_pos)
        if idx == -1:
            idx = curr_pos
        end_idx = min(idx + len(s) - 1, len(ends) - 1)
        s_time = starts[idx] if idx < len(starts) else (cues[-1]["end"] + 0.05 if cues else 0.0)
        e_time = ends[end_idx] if end_idx < len(ends) else total_audio_dur
        cues.append({
            "text": s,
            "start": s_time,
            "end": e_time
        })
        curr_pos = idx + len(s)
        
    for i in range(len(cues)):
        if cues[i]["end"] <= cues[i]["start"]:
            cues[i]["end"] = cues[i]["start"] + 1.5
        if i < len(cues) - 1:
            if cues[i]["end"] >= cues[i+1]["start"]:
                cues[i]["end"] = max(cues[i]["start"] + 1.0, cues[i+1]["start"] - 0.02)
                
    return cues

def write_srt_file(cues: List[Dict[str, Any]], out_path: Path, offset_seconds: float = 0.0):
    lines = []
    for i, cue in enumerate(cues, 1):
        s_str = format_srt_time(cue["start"] + offset_seconds)
        e_str = format_srt_time(cue["end"] + offset_seconds)
        lines.append(f"{i}\n{s_str} --> {e_str}\n{cue['text']}\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def main():
    print("=" * 65)
    print("  ELEVENLABS HINDI NARRATION & AUDIO TRACK PIPELINE (EP 05)")
    print(f"  Voice: Adam Stone ({VOICE_ID}) | Model: {MODEL_ID}")
    print("=" * 65)
    
    api_key = get_api_key()
    
    act_mp3_paths = []
    act_durations = []
    master_cues = []
    cumulative_offset = 0.0
    
    # 1. Synthesize 8 Acts in Hindi
    for idx, act in enumerate(HINDI_ACTS_DATA, 1):
        act_id = act["id"]
        full_text = " ".join(act["sentences"])
        out_mp3 = AUDIO_HINDI_DIR / f"{act_id}.mp3"
        out_srt = SUB_HINDI_DIR / f"{act_id}.srt"
        
        print(f"\n[*] Synthesizing [{idx}/8] {act['title']} ({len(act['sentences'])} cues)...")
        audio_bytes, alignment = synthesize_with_timestamps(full_text, api_key)
        out_mp3.write_bytes(audio_bytes)
        
        dur = get_audio_duration(out_mp3)
        act_durations.append(dur)
        act_mp3_paths.append(out_mp3)
        print(f"    Saved: {out_mp3.name} ({dur:.2f}s | {len(audio_bytes):,} bytes)")
        
        cues = build_act_cues(act["sentences"], full_text, alignment, dur)
        write_srt_file(cues, out_srt, offset_seconds=0.0)
        print(f"    Saved SRT: {out_srt.name} ({len(cues)} cues)")
        
        for c in cues:
            master_cues.append({
                "text": c["text"],
                "start": c["start"] + cumulative_offset,
                "end": c["end"] + cumulative_offset
            })
            
        cumulative_offset += dur
        
    # 2. Concatenate master narration stem
    print("\n" + "=" * 65)
    print("  CONCATENATING MASTER HINDI NARRATION STEM")
    print("=" * 65)
    
    concat_list_file = AUDIO_HINDI_DIR / "acts_concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for p in act_mp3_paths:
            f.write(f"file '{p.as_posix()}'\n")
            
    master_stem = AUDIO_HINDI_DIR / "episode_05_hindi_narration_master.mp3"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(master_stem)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)
    
    master_dur = get_audio_duration(master_stem)
    sum_dur = sum(act_durations)
    drift_ms = abs(master_dur - sum_dur) * 1000
    
    print(f"[*] Master Stem: {master_stem.name} ({master_dur:.3f}s)")
    print(f"[*] Sum of Acts: {sum_dur:.3f}s")
    print(f"[*] Concatenation Drift: {drift_ms:.2f} ms (Rule <= 10.0 ms)")
    
    # Write full master SRT
    master_srt = SUB_HINDI_DIR / "episode_05_hindi_full.srt"
    write_srt_file(master_cues, master_srt, offset_seconds=0.0)
    print(f"[*] Full Master Devanagari SRT: {master_srt.name} ({len(master_cues)} cues)")
    
    # 3. Synthesize Shorts in Hindi
    print("\n" + "=" * 65)
    print("  SYNTHESIZING COMPANION SHORTS IN HINDI")
    print("=" * 65)
    for s in HINDI_SHORTS_DATA:
        s_id = s["id"]
        full_text = " ".join(s["sentences"])
        out_mp3 = AUDIO_HINDI_DIR / f"{s_id}.mp3"
        out_srt = SUB_HINDI_DIR / f"{s_id}.srt"
        
        print(f"[*] Synthesizing Short: {s_id}...")
        audio_bytes, alignment = synthesize_with_timestamps(full_text, api_key)
        out_mp3.write_bytes(audio_bytes)
        dur = get_audio_duration(out_mp3)
        cues = build_act_cues(s["sentences"], full_text, alignment, dur)
        write_srt_file(cues, out_srt)
        print(f"    Saved: {out_mp3.name} ({dur:.2f}s) & {out_srt.name}")
        
    # 4. Mix YouTube Hindi Audio Track with Orchestral Bed (-16 LUFS)
    print("\n" + "=" * 65)
    print("  MIXING YOUTUBE MULTI-LANGUAGE AUDIO TRACK (-16 LUFS)")
    print("=" * 65)
    
    # Import mixing engine from mix_episode_05_audio
    import wave
    import numpy as np
    from mix_episode_05_audio import synthesize_orchestral_pad, synthesize_courtyard_wind, SAMPLE_RATE
    from audio_engine_v2 import apply_sidechain_ducking
    
    total_dur = master_dur
    print(f"[*] Synthesizing background music and ambient bed ({total_dur:.2f}s)...")
    pad_samples = synthesize_orchestral_pad(total_dur + 3.0, amplitude=0.18)
    wind_samples = synthesize_courtyard_wind(total_dur + 3.0, amplitude=0.14)
    min_len = min(len(pad_samples), len(wind_samples))
    blended_bed = (pad_samples[:min_len] * 0.85 + wind_samples[:min_len] * 0.65)
    
    peak = np.max(np.abs(blended_bed))
    if peak > 0.95:
        blended_bed = blended_bed / peak * 0.95
        
    hindi_bed_wav = AUDIO_HINDI_DIR / "_hindi_bgm_bed.wav"
    with wave.open(str(hindi_bed_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((blended_bed * 32767).astype(np.int16).tobytes())
        
    out_mixed_mp3 = AUDIO_HINDI_DIR / "episode_05_hindi_master_audio_mixed.mp3"
    out_m4a = FINAL_VIDEOS_DIR / "episode_05_hindi_track.m4a"
    
    print("[*] Applying -16 dB sidechain auto-ducking & EBU R128 normalization...")
    apply_sidechain_ducking(
        vocal_path=master_stem,
        bgm_path=hindi_bed_wav,
        out_path=out_mixed_mp3,
        ducking_db=-16,
        target_lufs=-16.0
    )
    
    # Export M4A container for YouTube Audio Track upload
    cmd_m4a = [
        "ffmpeg", "-y",
        "-i", str(out_mixed_mp3),
        "-c:a", "aac", "-b:a", "256k",
        str(out_m4a)
    ]
    subprocess.run(cmd_m4a, capture_output=True, check=True)
    
    if hindi_bed_wav.exists():
        hindi_bed_wav.unlink()
        
    print(f"\n[COMPLETE] YouTube Hindi Audio Track Exported:")
    print(f"  -> Studio Mixed MP3: {out_mixed_mp3.as_posix()} ({out_mixed_mp3.stat().st_size:,} bytes)")
    print(f"  -> YouTube Audio Track M4A: {out_m4a.as_posix()} ({out_m4a.stat().st_size:,} bytes)")
    print(f"  -> Master Devanagari SRT: {master_srt.as_posix()} ({len(master_cues)} cues)")

if __name__ == "__main__":
    main()
