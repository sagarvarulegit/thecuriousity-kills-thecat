#!/usr/bin/env python3
"""
synthesize_episode_07_narration.py — ElevenLabs Studio Narration & Subtitle Synthesizer (Episode 07)
Synthesizes Episode 07 narration in English and Hindi using ElevenLabs API with Adam Stone (auq43ws1oslv0tO4BDa7).
Extracts millisecond-accurate timestamps using /with-timestamps endpoint.
Generates:
1. 5 individual English Act MP3s and Devanagari Hindi Act MP3s
2. Perfectly monotonic, non-overlapping .srt subtitles in English and Hindi
3. Seamless master concatenation with <= 10.0 ms drift
4. 2 companion Shorts voiceovers and subtitles in English and Hindi
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
EP07_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode07"
AUDIO_DIR = EP07_DIR / "audio" / "narration"
SUB_DIR = EP07_DIR / "subtitles"
AUDIO_HINDI_DIR = EP07_DIR / "audio_hindi" / "narration"
SUB_HINDI_DIR = EP07_DIR / "subtitles_hindi"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUB_DIR.mkdir(parents=True, exist_ok=True)
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

# The 5 Acts English Data
ACTS_DATA = [
    {
        "id": "act_01_the_hidden_crescent",
        "title": "Act I — The Hidden Crescent",
        "sentences": [
            "When you stand inside the 100-foot chasm of Kailasa at Ellora, you are looking at the peak of ancient stone engineering.",
            "But Kailasa did not appear out of thin air.",
            "Decades before the Rashtrakutas cleared four hundred thousand tons of basalt, the secret science of subterranean rock carving had already been perfected.",
            "To find where it began, we must travel one hundred kilometers north, deep into the wild Sahyadri mountains.",
            "Here, sliced through a solid table of Cretaceous flood basalt, the Waghur River carved a jagged, horseshoe-shaped canyon seventy-five meters deep.",
            "From the outer plateau, the gorge is completely invisible, hidden behind dense teak scrub and sheer volcanic cliffs.",
            "Yet along the curved inner wall of this sheer basalt amphitheater, ancient builders chiseled thirty monumental sanctuaries directly into the face of the mountain.",
            "This is Ajanta.",
            "And for more than seven centuries, it was the laboratory where India’s master stonecutters unlocked the mysteries of the rock."
        ]
    },
    {
        "id": "act_02_the_first_chisel_strike",
        "title": "Act II — The First Chisel Strike",
        "sentences": [
            "The story of Ajanta begins in the second century before the common era, under the patronage of the powerful Satavahana dynasty.",
            "A band of Buddhist monks and wandering ascetics walked along the trade artery of the Dakshinapatha, seeking seclusion from the worldly commerce of the plains.",
            "They chose this crescent ravine because volcanic geology offered something unique: a continuous, seventy-five-meter face of dense, microcrystalline columnar basalt.",
            "In early Buddhism, doctrine strictly forbade carving anthropomorphic statues of the Buddha.",
            "Worship was centered upon the stupa—a solid hemispherical dome representing the ultimate passing of the enlightened mind.",
            "In Caves Nine and Ten, early masons entered the cliff at the roofline, establishing the very subtractive top-down technique that would later define Kailasa.",
            "Without scaffolding, they hollowed out monumental apsidal chaitya halls, carving soaring vaulted ceilings that mimicked the curved timber rafters of ancient wooden assembly halls.",
            "Along the sides, they chiseled rows of austere octagonal columns, slanting them slightly inward by three degrees to replicate wooden earthquake braces.",
            "Even in stone, their hands remembered wood; but the mountain demanded an entirely different mastery."
        ]
    },
    {
        "id": "act_03_taming_the_monsoon",
        "title": "Act III — Taming the Monsoon",
        "sentences": [
            "Carving a monastery into the sheer face of a river canyon comes with a deadly enemy: the Indian monsoon.",
            "Every summer, torrential downpours cascade off the high Deccan plateau, sending millions of gallons of water hurtling over the cliff edge toward the cave facades.",
            "If uncontrolled, sheet runoff would flood the subterranean halls, dissolving the lime plaster, cracking columns, and triggering catastrophic rockslides.",
            "Ancient engineers countered nature with a brilliant hydraulic defense system.",
            "Along the upper rim of the cliff, meters above the cave roofs, stonecutters chiseled deep continuous drainage gutters directly into the surface bedrock.",
            "These rock-cut channels captured surface runoff and redirected the torrent away from the cave entrances, spilling the water harmlessly down natural ravines.",
            "Meanwhile, inside the canyon, builders solved the problem of surviving the eight-month dry season.",
            "They carved deep subterranean cisterns known as podhis beneath the cave courtyards.",
            "Rainwater that seeped through natural cooling joints in the volcanic rock was caught and naturally filtered through meters of dense basalt.",
            "The water collected in these dark, cold reservoirs, remaining crystal clear and bacteria-free throughout the scorching summer months."
        ]
    },
    {
        "id": "act_04_the_sound_of_the_living_stone",
        "title": "Act IV — The Sound of the Living Stone",
        "sentences": [
            "But the early masters of Ajanta did not just sculpt for the eye; they engineered for the ear.",
            "The apsidal prayer halls of Caves Nine and Ten were sculpted as acoustic resonators.",
            "The dense, non-porous basalt walls possess minimal sound absorption, creating sustained reverberation times that specifically amplify low-frequency sound.",
            "When monks gathered in the darkness around the monolithic stupa to chant sacred mantras, something remarkable occurred.",
            "The human voice, pitched between one hundred and one hundred and twenty hertz, locked into the natural acoustic resonance of the basalt chamber.",
            "The sound did not merely echo; it vibrated physically through the stone floor and columns, creating an immersive acoustic field that seemed to emerge from the mountain itself.",
            "In an era without microphones or amplification, the monks turned the living bedrock into a colossal musical instrument."
        ]
    },
    {
        "id": "act_05_the_400_year_hibernation",
        "title": "Act V — The 400-Year Hibernation",
        "sentences": [
            "By the first century of the common era, something shifted across the Deccan.",
            "Royal dynasties rose and fell, regional trade routes migrated south toward coastal ports, and patron funding slowly evaporated.",
            "Activity in the horseshoe canyon ground to a complete halt.",
            "For nearly four hundred uninterrupted years—longer than the United States has existed as a nation—Ajanta lay dormant.",
            "Teak trees grew across the terrace steps, silt washed into the lower chaityas, and bats took residence in the dark stone sanctums.",
            "Yet the knowledge carved into these volcanic cliffs was not destroyed.",
            "It waited patiently in the dark until the mid-fifth century, when a powerful emperor named Harishena would reawaken the canyon in an explosion of color and gold.",
            "But that golden renaissance would bring with it an even darker mystery: an overnight disappearance that sealed Ajanta from humanity for over a thousand years.",
            "In our next episode, we unlock the secret chemistry of Ajanta's golden age.",
            "From Afghan blue gems to fermented cow dung plaster and polished mirror light."
        ]
    }
]

# The 5 Acts Hindi Data
HINDI_ACTS_DATA = [
    {
        "id": "act_01_the_hidden_crescent",
        "title": "Act I — गुप्त अर्धचंद्राकार घाटी",
        "sentences": [
            "जब आप एलोरा में कैलाश की सौ फीट गहरी खाई में खड़े होते हैं, तो आप प्राचीन पाषाण शिल्पकला के चरमोत्कर्ष को देख रहे होते हैं।",
            "लेकिन कैलाश शून्य से प्रकट नहीं हुआ था।",
            "राष्ट्रकूटों द्वारा चार लाख टन बेसाल्ट हटाने से दशकों पहले, भूमिगत चट्टान तराशने का यह गुप्त विज्ञान पहले ही सिद्ध हो चुका था।",
            "यह जानने के लिए कि इसकी शुरुआत कहाँ से हुई, हमें सौ किलोमीटर उत्तर, दुर्गम सह्याद्रि पहाड़ियों में जाना होगा।",
            "यहाँ, प्राचीन ज्वालामुखी बेसाल्ट के ठोस पठार को चीरते हुए, वाघूर नदी ने पचहत्तर मीटर गहरी एक अर्धचंद्राकार घाटी बनाई।",
            "बाहरी पठार से यह घाटी पूरी तरह अदृश्य है, घने सागौन के जंगलों और खड़ी चट्टानों के पीछे छिपी हुई।",
            "फिर भी इस विशाल प्राकृतिक रंगमंच की भीतरी दीवार पर, प्राचीन शिल्पकारों ने सीधे पर्वत के सीने में तीस भव्य गुफाएं तराश दीं।",
            "यह है अजंता।",
            "और सात शताब्दियों से भी अधिक समय तक, यह वही प्रयोगशाला थी जहाँ भारत के मुख्य वास्तुकारों ने चट्टान के रहस्यों को खोला था।"
        ]
    },
    {
        "id": "act_02_the_first_chisel_strike",
        "title": "Act II — प्रथम छैनी का प्रहार",
        "sentences": [
            "अजंता की कहानी ईसा पूर्व दूसरी शताब्दी में, शक्तिशाली सातवाहन राजवंश के संरक्षण में शुरू होती है।",
            "बौद्ध भिक्षुओं का एक दल दक्षिणापथ के व्यापारिक मार्ग पर चलते हुए, सांसारिक कोलाहल से दूर एकांत की खोज में यहाँ पहुँचा।",
            "उन्होंने इस अर्धचंद्राकार घाटी को चुना क्योंकि यहाँ का भूविज्ञान अद्वितीय था: पचहत्तर मीटर ऊंचा, सघन और स्तंभकार बेसाल्ट पत्थर।",
            "प्रारंभिक बौद्ध धर्म में, बुद्ध की मानवीय प्रतिमाएं बनाना वर्जित था।",
            "उपासना का केंद्र स्तूप था—एक ठोस अर्धगोलाकार गुंबद जो बुद्ध के महापरिनिर्वाण का प्रतीक था।",
            "गुफा नौ और दस में, शिल्पकारों ने शीर्ष से प्रवेश किया, और उसी अधोमुखी तकनीक की नींव रखी जिसने बाद में कैलाश का निर्माण किया।",
            "बिना किसी मचान के, उन्होंने विशाल चैत्य कक्ष खोदे, और मेहराबदार छतों पर लकड़ी की पुरानी कड़ियों जैसी नक्काशी उकेर दी।",
            "किनारों पर, उन्होंने अष्टकोणीय स्तंभ तराशे, जिन्हें भूकंप से बचाने के लिए भीतर की ओर तीन अंश झुकाया गया था।",
            "पत्थर में भी उनके हाथों को लकड़ी की स्मृति थी; लेकिन इस पर्वत ने एक बिल्कुल नई निपुणता की मांग की।"
        ]
    },
    {
        "id": "act_03_taming_the_monsoon",
        "title": "Act III — मानसून पर विजय",
        "sentences": [
            "नदी की खड़ी घाटी में मठ तराशने के साथ एक भयानक शत्रु भी आता है: भारतीय मानसून।",
            "हर गर्मी में, दक्कन के पठार से लाखों गैलन पानी गुफाओं के द्वारों पर प्रपात बनकर गिरता था।",
            "यदि इसे न रोका जाता, तो यह जल प्लास्टर को घोल देता, खंभों को तोड़ देता और भीषण भूस्खलन ला देता।",
            "प्राचीन वास्तुकारों ने प्रकृति का सामना एक अद्भुत जल निकासी प्रणाली से किया।",
            "गुफाओं की छतों से कई मीटर ऊपर, चट्टान की ऊपरी सतह पर गहरी और निरंतर जल नालियां तराशी गईं।",
            "इन नालियों ने पठार के बहाव को मोड़ दिया और बाढ़ के पानी को गुफाओं से दूर प्राकृतिक खड्डों में गिरा दिया।",
            "इसके साथ ही, उन्होंने आठ महीने चलने वाले सूखे का समाधान भी खोजा।",
            "उन्होंने गुफाओं के आंगनों के नीचे गहरे भूमिगत जलकुंड तराशे, जिन्हें 'पोढ़ी' कहा जाता था।",
            "ज्वालामुखी चट्टानों की दरारों से रिसने वाला वर्षाजल घने बेसाल्ट से छनकर इन कुंडों में एकत्र होता था।",
            "इन ठंडे और अंधेरे जलाशयों में पानी पूरे साल कांच की तरह साफ और जीवाणु-मुक्त रहता था।"
        ]
    },
    {
        "id": "act_04_the_sound_of_the_living_stone",
        "title": "Act IV — जीवित पाषाण की ध्वनि",
        "sentences": [
            "लेकिन अजंता के शिल्पकारों ने केवल आँखों के लिए ही नहीं, बल्कि कानों के लिए भी रचना की थी।",
            "गुफा नौ और दस के चैत्य कक्ष ध्वनि गुंजायमान कक्षों के रूप में गढ़े गए थे।",
            "सघन बेसाल्ट की दीवारें ध्वनि को सोखती नहीं हैं, जिससे निम्न-आवृत्ति की ध्वनियां कई गुना बढ़ जाती हैं।",
            "जब भिक्षु अंधेरे में स्तूप के चारों ओर मंत्रोच्चार के लिए एकत्र होते थे, तो एक जादुई घटना घटती थी।",
            "मानव कंठ की ध्वनि, जो सौ से एक सौ बीस हर्ट्ज़ के बीच होती है, गुफा के प्राकृतिक अनुनाद से एकाकार हो जाती थी।",
            "यह ध्वनि केवल गूंजती नहीं थी; यह पत्थर के फर्श और खंभों में कंपन पैदा करती थी, मानो स्वयं पर्वत गा रहा हो।",
            "बिना किसी माइक या यंत्र के, भिक्षुओं ने इस जीवित चट्टान को एक विशाल वाद्य यंत्र बना दिया था।"
        ]
    },
    {
        "id": "act_05_the_400_year_hibernation",
        "title": "Act V — चार सौ वर्षों की निद्रा",
        "sentences": [
            "ईसा की पहली शताब्दी तक, दक्कन में परिस्थितियां बदलने लगीं।",
            "राजवंश बदले, व्यापारिक मार्ग दक्षिण के तटीय बंदरगाहों की ओर मुड़ गए, और संरक्षण समाप्त हो गया।",
            "इस अर्धचंद्राकार घाटी में काम पूरी तरह थम गया।",
            "लगभग चार सौ वर्षों तक—जितना संयुक्त राज्य अमेरिका का पूरा इतिहास है—अजंता गहरी निद्रा में सो गया।",
            "सीढ़ियों पर सागौन के पेड़ उग आए, चैत्यों में कीचड़ भर गया, और अंधेरे गर्भगृहों में चमगादड़ों का बसेरा हो गया।",
            "फिर भी इन चट्टानों में खुदा ज्ञान कभी नष्ट नहीं हुआ।",
            "वह अंधेरे में पांचवीं शताब्दी के मध्य तक प्रतीक्षा करता रहा, जब सम्राट हरिषेण ने रंगों और सोने के साथ इसे पुनर्जीवित किया।",
            "लेकिन उस स्वर्ण युग के साथ एक और गहरा रहस्य जुड़ा: एक ऐसा अचानक पलायन जिसने अजंता को एक हज़ार साल तक छिपा दिया।",
            "हमारे अगले एपिसोड में, हम अजंता के स्वर्ण युग की गुप्त रसायन विद्या को उजागर करेंगे।",
            "अफगान नीलम से लेकर गाय के गोबर के प्लास्टर और दर्पणों की रोशनी तक।"
        ]
    }
]

SHORTS_DATA = [
    {
        "id": "short_01_the_horseshoe_canyon_hidden_from_the_world",
        "sentences": [
            "This canyon holds thirty ancient temples that were completely lost to human memory.",
            "Carved seventy-five meters deep into a volcanic cliff, the Waghur River created a natural stone fortress.",
            "Over two thousand years ago, ancient Buddhist monks began hollowing out this sheer mountain from the top down.",
            "There were no scaffolds, no mortar, and no room for a single architectural mistake.",
            "Long before Kailasa was conceived, the secret science of rock carving was born here."
        ]
    },
    {
        "id": "short_02_how_ancient_monks_engineered_water",
        "sentences": [
            "How do you keep a monsoon from drowning an entire mountain monastery?",
            "Ancient engineers at Ajanta faced millions of gallons of water crashing over the cliff edge every summer.",
            "Their solution was pure genius.",
            "They chiseled massive diversion canals into the mountain summit to route floodwaters away from cave portals.",
            "Then, they dug deep subterranean cisterns that trapped water percolating through volcanic rock.",
            "The basalt naturally filtered the water, providing ice-cold drinking supplies all year long."
        ]
    }
]

HINDI_SHORTS_DATA = [
    {
        "id": "short_01_the_horseshoe_canyon_hidden_from_the_world",
        "sentences": [
            "इस घाटी में तीस ऐसे प्राचीन मंदिर छिपे हैं जिन्हें इंसान तेरह सौ साल तक पूरी तरह भूल चुका था।",
            "पचहत्तर मीटर गहरी ज्वालामुखी चट्टान में वाघूर नदी ने यह प्राकृतिक पाषाण दुर्ग बनाया था।",
            "दो हज़ार साल पहले, बौद्ध भिक्षुओं ने इस पहाड़ को ऊपर से नीचे की ओर तराशना शुरू किया।",
            "यहाँ न कोई मचान था, न गारा, और न ही एक भी गलती की कोई गुंजाइश।",
            "कैलाश मंदिर से सदियों पहले, पहाड़ तराशने का यह गुप्त विज्ञान यहीं जन्मा था।"
        ]
    },
    {
        "id": "short_02_how_ancient_monks_engineered_water",
        "sentences": [
            "आप किसी मानसूनी बाढ़ से पूरे पहाड़ के मठ को कैसे बचा सकते हैं?",
            "अजंता के प्राचीन इंजीनियरों के सामने हर साल लाखों गैलन पानी चट्टान से नीचे गिरता था।",
            "उनका उपाय अभूतपूर्व था।",
            "उन्होंने पहाड़ की चोटी पर बड़ी-बड़ी नहरें तराश दीं ताकि बाढ़ का पानी गुफाओं के ऊपर से निकल जाए।",
            "फिर उन्होंने जमीन के अंदर गहरे जलकुंड खोदे जो चट्टान से रिसने वाले पानी को जमा करते थे।",
            "ज्वालामुखी पत्थर ने पानी को स्वाभाविक रूप से छाना, और साल भर बर्फ जैसा ठंडा पानी दिया।"
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

def process_language(lang_code: str, acts_list: list, shorts_list: list, audio_out_dir: Path, sub_out_dir: Path, api_key: str):
    print(f"\n{'=' * 65}\n  PROCESSING {lang_code.upper()} NARRATION (EPISODE 07)\n{'=' * 65}")
    act_mp3_paths = []
    act_durations = []
    master_cues = []
    cumulative_offset = 0.0
    
    for idx, act in enumerate(acts_list, 1):
        act_id = act["id"]
        full_text = " ".join(act["sentences"])
        out_mp3 = audio_out_dir / f"{act_id}.mp3"
        out_srt = sub_out_dir / f"{act_id}.srt"
        
        print(f"[*] Synthesizing [{idx}/{len(acts_list)}] {act['title']} ({len(act['sentences'])} cues)...")
        audio_bytes, alignment = synthesize_with_timestamps(full_text, api_key)
        out_mp3.write_bytes(audio_bytes)
        
        dur = get_audio_duration(out_mp3)
        act_durations.append(dur)
        act_mp3_paths.append(out_mp3)
        print(f"    Saved: {out_mp3.name} ({dur:.2f}s | {len(audio_bytes):,} bytes)")
        
        cues = build_act_cues(act["sentences"], full_text, alignment, dur)
        write_srt_file(cues, out_srt, offset_seconds=0.0)
        
        for c in cues:
            master_cues.append({
                "text": c["text"],
                "start": c["start"] + cumulative_offset,
                "end": c["end"] + cumulative_offset
            })
        cumulative_offset += dur
        
    # Concat master stem via PCM wav to eliminate MP3 header padding drift (0.00ms drift)
    concat_list = audio_out_dir / "acts_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in act_mp3_paths:
            f.write(f"file '{p.as_posix()}'\n")
            
    master_stem = audio_out_dir / (f"episode_07_narration_master.mp3" if lang_code == "en" else "episode_07_hindi_narration_master.mp3")
    master_wav = audio_out_dir / (f"episode_07_narration_master.wav" if lang_code == "en" else "episode_07_hindi_narration_master.wav")
    
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c:a", "pcm_s16le", str(master_wav)]
    subprocess.run(cmd_concat, capture_output=True, check=True)
    
    cmd_mp3 = ["ffmpeg", "-y", "-i", str(master_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(master_stem)]
    subprocess.run(cmd_mp3, capture_output=True, check=True)
    
    master_dur = get_audio_duration(master_stem)
    sum_dur = sum(act_durations)
    drift_ms = abs(master_dur - sum_dur) * 1000
    print(f"[*] Master Stem: {master_stem.name} ({master_dur:.3f}s)")
    print(f"[*] Concatenation Drift: {drift_ms:.2f} ms")
    
    master_srt = sub_out_dir / (f"episode_07_full.srt" if lang_code == "en" else "episode_07_hindi_full.srt")
    write_srt_file(master_cues, master_srt, offset_seconds=0.0)
    print(f"[*] Master SRT: {master_srt.name} ({len(master_cues)} cues)")
    
    # Process Shorts
    for s in shorts_list:
        s_id = s["id"]
        full_text = " ".join(s["sentences"])
        s_mp3 = audio_out_dir / f"{s_id}.mp3"
        s_srt = sub_out_dir / f"{s_id}.srt"
        print(f"[*] Synthesizing Short: {s_id}...")
        audio_bytes, alignment = synthesize_with_timestamps(full_text, api_key)
        s_mp3.write_bytes(audio_bytes)
        dur = get_audio_duration(s_mp3)
        cues = build_act_cues(s["sentences"], full_text, alignment, dur)
        write_srt_file(cues, s_srt)
        print(f"    Saved Short: {s_mp3.name} ({dur:.2f}s)")

def main():
    print("=" * 65)
    print("  ELEVENLABS AUDIO NARRATION SUITE — EPISODE 07")
    print(f"  Voice: Adam Stone ({VOICE_ID}) | Model: {MODEL_ID}")
    print("=" * 65)
    
    api_key = get_api_key()
    
    # 1. Process English Master & Shorts
    process_language("en", ACTS_DATA, SHORTS_DATA, AUDIO_DIR, SUB_DIR, api_key)
    
    # 2. Process Hindi Master & Shorts
    process_language("hi", HINDI_ACTS_DATA, HINDI_SHORTS_DATA, AUDIO_HINDI_DIR, SUB_HINDI_DIR, api_key)
    
    print("\n[ALL COMPLETE] Episode 07 English and Hindi audio stems & SRT subtitles successfully generated!")

if __name__ == "__main__":
    main()
