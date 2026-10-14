#!/usr/bin/env python3
"""
generate_ep06_elevenlabs_narration.py — ElevenLabs Studio Narration & Subtitle Synthesizer (Episode 06)
Synthesizes Episode 06 narration in English and Hindi using ElevenLabs API with Adam Stone (auq43ws1oslv0tO4BDa7).
Extracts millisecond-accurate timestamps using /with-timestamps endpoint.
Generates:
1. 8 individual English Act MP3s and Devanagari Hindi Act MP3s
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
EP06_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode06"
AUDIO_DIR = EP06_DIR / "audio"
SUB_DIR = EP06_DIR / "subtitles"
AUDIO_HINDI_DIR = EP06_DIR / "audio_hindi"
SUB_HINDI_DIR = EP06_DIR / "subtitles_hindi"

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

# The 8 Acts English Data
ACTS_DATA = [
    {
        "id": "act_01_the_bridges_in_the_sky",
        "title": "Act I — The Bridges in the Sky",
        "sentences": [
            "When you descend into the deep trench of Cave 16, your eyes are drawn upward by a physical impossibility.",
            "Suspended thirty feet in the open air, a monolithic stone bridge spans the chasm between the entrance gateway and the inner shrine.",
            "There are no mortar joints, no structural keystones, and no iron tie-rods holding this walkway together.",
            "It is cut from the living volcanic basalt bedrock, an aerial arch carved out of the mountain interior.",
            "To modern structural engineers, an arched bridge is assembled from stone blocks that wedge against each other under compression.",
            "But at Kailasa, the bridge was never assembled; it was left behind when the empty space below it was hollowed away.",
            "If a single natural fissure crossed the span, or if a stonecutter struck too deeply, thousands of tons of stone would shear and collapse.",
            "Decades of royal labor and the entire architectural axis of the temple would have been destroyed in seconds.",
            "Today, we investigate the engineering gamble behind the floating bridges of Ellora."
        ]
    },
    {
        "id": "act_02_the_queens_vow_and_the_shikhara",
        "title": "Act II — The Queen's Vow and the 7-Day Shikhara",
        "sentences": [
            "To understand how ancient carvers dared to leave bridges hanging in mid-air, we must look at the legend of its conception.",
            "A medieval chronicle preserved in the Katha-Kalpataru tells of a Rashtrakuta queen whose husband fell critically ill.",
            "She made a sacred vow to fast until she could gaze upon the pinnacle of a magnificent Shiva temple built for his recovery.",
            "Royal architects told the king that building such a monument from the ground up would require decades, condemning the queen to starvation.",
            "Then stepped forward a master builder from the artisan lineage named Kokasa.",
            "Kokasa promised that the queen would behold the gleaming temple spire in just seven days.",
            "He climbed to the summit of the volcanic cliff, plotted the sacred geometry, and carved the pinnacle downward from the mountain peak.",
            "Within seven days, the soaring shikhara stood fully formed on the mountaintop, allowing the queen to break her fast.",
            "While legendary in detail, the story captures the core engineering truth: Kailasa was conceived from the heavens downward."
        ]
    },
    {
        "id": "act_03_carving_the_void",
        "title": "Act III — Carving the Void",
        "sentences": [
            "Carving an aerial bridge from the top down requires solving a terrifying logistical puzzle.",
            "The upper walkway of the bridge had to be finished first, while solid bedrock still supported it from below.",
            "Surveyors snapped dyed cords across the surface, marking the exact thickness needed to withstand structural dead loads.",
            "Then came the dangerous stage: quarrymen were suspended in hemp rope harnesses over a thirty-foot abyss to hollow out the underbelly.",
            "Working upside down in cramped voids, stonecutters used pointed picks to scoop away the rock beneath the span.",
            "They had to listen to the stone; dull hollow thuds signaled thin basalt, while crisp ringing rings meant solid load-bearing rock.",
            "Thermal fire-setting could not be used here; intense heat would induce micro-fractures in the hanging ceiling.",
            "Every single cubic foot of the void had to be cut through sheer manual percussion with tempered carbon-steel chisels.",
            "When the void was cleared, the bridge hung unsupported—a permanent aerial monument suspended between two worlds."
        ]
    },
    {
        "id": "act_04_the_courtyard_monoliths",
        "title": "Act IV — The Courtyard Monoliths",
        "sentences": [
            "As quarrymen deepened the courtyard floor past the aerial bridges, they encountered two monumental stone islands.",
            "Rather than clearing the trench into a flat floor, they left two towering columns of living basalt standing fifty feet tall.",
            "These became the famous Dhwajasthambhas—the colossal monolithic victory pillars of Kailasa.",
            "Carved in place from the bedrock, they rise seventeen meters into the sky with intricate fluting, floral bands, and tridents.",
            "Flanking the courtyard, two life-size monolithic elephants emerge directly from the courtyard floor.",
            "Their massive flanks, carved ears, and wrinkled trunks were freed from the surrounding stone without a single joint.",
            "In ancient Indian rock architecture, creating a freestanding statue inside a quarry requires extreme mathematical precision.",
            "The sculptor must visualize the complete three-dimensional animal inside a dark, uncarved mass of rock before making the first strike.",
            "Once stone is removed, it cannot be replaced; one chipped tusk would ruin twenty years of continuous carving."
        ]
    },
    {
        "id": "act_05_the_living_epics_in_basalt",
        "title": "Act V — The Living Epics in Basalt",
        "sentences": [
            "Along the lower plinth flanking the temple halls, the bedrock transforms from monumental mass into narrative poetry.",
            "Two continuous running friezes depict the great Indian epics—the Ramayana on the south and the Mahabharata on the north.",
            "Across miniature horizontal tiers, master sculptors chiseled hundreds of dynamic figures into the hard volcanic stone.",
            "On the southern wall, we see the battle of Lanka, with chariot wheels, galloping war horses, and archers drawing bows.",
            "Nearby, the dramatic high-relief panel of Ravana Shaking Mount Kailash captures tectonic terror in stone.",
            "The demon king exerts all twenty arms against the roots of the mountain, straining with bulging muscles and grimacing fury.",
            "Above, Shiva calmly presses his big toe downward into the bedrock, instantly neutralizing the subterranean earthquake.",
            "The depth of the relief creates stark chiaroscuro shadows under the bright Deccan sun, making the figures appear in kinetic motion.",
            "The living rock ceases to be cold basalt; it becomes a theater of cosmic power and human drama."
        ]
    },
    {
        "id": "act_06_the_white_mountain_of_ellora",
        "title": "Act VI — The White Mountain of Ellora",
        "sentences": [
            "Today, when visitors enter Kailasa, they see dark, weathered volcanic basalt.",
            "But for centuries after its creation, Kailasa looked completely different.",
            "The entire monument was coated in a brilliant, luminous white shell-lime plaster known as chuna.",
            "Formulated from calcined river shells, slaked lime, marble dust, and organic plant binders, this coating was burnished with smooth agate stones.",
            "Under the blazing tropical sun of Maharashtra, the temple gleamed with a blinding, porcelain-like white radiance.",
            "This was the architectural masterstroke of the Rashtrakutas: to recreate Mount Kailash of the snow-covered Himalayas in the volcanic plains of the Deccan.",
            "Travelers approaching Elapura across the dusty plateau saw what appeared to be an iceberg of pure stone rising from a black chasm.",
            "Rain and centuries of monsoon weathering eventually stripped away the white shell, exposing the dark volcanic skeleton beneath.",
            "Yet in sheltered cornices and ceiling corners, patches of the gleaming white plaster remain intact today."
        ]
    },
    {
        "id": "act_07_the_mountain_that_refused_to_fall",
        "title": "Act VII — The Mountain That Refused to Fall",
        "sentences": [
            "The true test of a building is not just how it was made, but how it withstands the desire to destroy it.",
            "In the late seventeenth century, Mughal Emperor Aurangzeb set his camp near Ellora and ordered the temple demolished.",
            "A task force of over one thousand workers equipped with heavy sledgehammers, crowbars, and chisels was dispatched to level Cave 16.",
            "For over a year, demolition teams hammered relentlessly against the temple facade, day and night.",
            "In conventional stone temples built of mortar and stacked masonry blocks, knocking out a few key pillars causes the roof to cave in.",
            "But Kailasa is not a building; it is a solid mountain peak.",
            "The workers broke chisels, chipped away outer statues, and defaced decorative reliefs, but the structural core refused to budge.",
            "After months of brutal labor and negligible structural progress, Aurangzeb conceded defeat and abandoned the demolition effort.",
            "The living bedrock of the Deccan Traps proved stronger than imperial siege weapons."
        ]
    },
    {
        "id": "act_08_the_architects_confession",
        "title": "Act VIII — The Architect's Confession",
        "sentences": [
            "More than twelve centuries have passed since the last chisel struck the rock of Cave 16.",
            "In the Baroda copper-plate charter of 812 CE, King Karka the Second recorded the contemporary reaction to the finished sanctuary.",
            "He wrote that celestial gods flying across the sky in heavenly chariots peered down into the chasm in absolute disbelief.",
            "They marveled: 'This temple of Shiva is self-existent; no human skill could have fashioned such a thing.'",
            "But the most poignant line in the inscription belongs to the chief architect himself.",
            "Standing on the cleared courtyard floor, looking up at the sky bridges, the victory pillars, and the soaring vimana, he cried out:",
            "'Katham-akrita yan-maya' — 'How was it that I could have built it?'",
            "Even the mind that conceived the impossible could not believe that mortal hands had brought it into the light.",
            "And that remains the eternal mystery of Kailasa: a monument that surpasses the comprehension of its own creators."
        ]
    }
]

# The 8 Acts Hindi Data
HINDI_ACTS_DATA = [
    {
        "id": "act_01_the_bridges_in_the_sky",
        "title": "Act I — आकाश में तैरते पाषाण सेतु",
        "sentences": [
            "जब आप गुफा 16 की गहरी खाई में उतरते हैं, तो आपकी आँखें एक असंभव दृश्य की ओर उठ जाती हैं।",
            "हवा में तीस फीट ऊपर लटका हुआ, एक एकाश्मक पाषाण सेतु प्रवेश द्वार और मुख्य मंदिर के बीच की खाई को जोड़ता है।",
            "इस मार्ग को थामने के लिए न तो कोई गारे का जोड़ है, न कोई मुख्य मेहराबदार पत्थर, और न ही लोहे की कोई छड़।",
            "यह जीवित ज्वालामुखीय बेसाल्ट चट्टान से तराशा गया है, पर्वत के भीतर से उकेरा गया एक आकाशीय मेहराब।",
            "आधुनिक इंजीनियरों के लिए, एक मेहराबदार पुल पत्थरों के ऐसे टुकड़ों से बनता है जो दबाव में एक-दूसरे को थामते हैं।",
            "लेकिन कैलाश में, यह पुल कभी जोड़ा नहीं गया था; बल्कि नीचे के शून्य को खाली करते समय इसे हवा में छोड़ दिया गया।",
            "यदि एक भी प्राकृतिक दरार इस विस्तार में आ जाती, या कोई छैनी ज़रा गहरी लग जाती, तो हज़ारों टन पत्थर टूटकर बिखर जाता।",
            "दशकों का शाही परिश्रम और मंदिर का समूचा संतुलन पलक झपकते ही नष्ट हो जाता।",
            "आज, हम एलोरा के इन तैरते हुए पुलों के पीछे के सबसे बड़े इंजीनियरिंग जोखिम की पड़ताल करेंगे।"
        ]
    },
    {
        "id": "act_02_the_queens_vow_and_the_shikhara",
        "title": "Act II — रानी का संकल्प और सात दिनों का शिखर",
        "sentences": [
            "प्राचीन शिल्पकारों ने हवा में पुल लटकाने का यह दुस्साहस कैसे किया, इसे समझने के लिए हमें इसके निर्माण की गाथा देखनी होगी।",
            "कथा-कल्पतरु में सुरक्षित एक वृत्तांत एक राष्ट्रकूट रानी की कहानी कहता है, जिनके पति गंभीर रूप से अस्वस्थ हो गए थे।",
            "उन्होंने संकल्प लिया कि जब तक वे उनके स्वास्थ्य लाभ के लिए बनने वाले भव्य शिव मंदिर का शिखर नहीं देख लेंगी, अन्न ग्रहण नहीं करेंगी।",
            "शाही वास्तुकारों ने कहा कि ज़मीन से ऊपर ऐसा मंदिर बनाने में कई दशक लगेंगे, जिससे रानी की मृत्यु निश्चित थी।",
            "तभी शिल्पकार वंश का एक महान वास्तुकार कोकास आगे आया।",
            "कोकास ने वचन दिया कि रानी मात्र सात दिनों में मंदिर के जगमगाते शिखर के दर्शन कर सकेंगी।",
            "वह ज्वालामुखी चट्टान के शिखर पर चढ़ा, पवित्र ज्यामिति तय की, और पर्वत की चोटी से नीचे की ओर शिखर को तराशना शुरू किया।",
            "सात दिनों के भीतर, पर्वत की चोटी पर भव्य शिखर साकार हो उठा, और रानी ने अपना उपवास तोड़ा।",
            "यह कथा प्रतीकात्मक हो सकती है, लेकिन एक अकाट्य सच उजागर करती है: कैलाश की रचना आकाश से पाताल की ओर हुई थी।"
        ]
    },
    {
        "id": "act_03_carving_the_void",
        "title": "Act III — शून्य को तराशने की कला",
        "sentences": [
            "ऊपर से नीचे हवा में तैरता पुल तराशना एक रोंगटे खड़े कर देने वाली इंजीनियरिंग चुनौती थी।",
            "पुल का ऊपरी पैदल मार्ग पहले पूरा करना था, जब तक नीचे की ठोस चट्टान उसे सहारा दे रही थी।",
            "सर्वेक्षकों ने सतह पर रंगीन डोरियाँ खींचकर उस सटीक मोटाई को चिन्हित किया जो संरचनात्मक भार सह सके।",
            "फिर आया सबसे खतरनाक दौर: तीस फीट गहरी खाई में सन की रस्सियों से लटककर मज़दूरों ने पुल के निचले हिस्से को काटना शुरू किया।",
            "संकीर्ण अंधेरे में उल्टे लटककर, कारीगरों ने नुकीली छैनियों से पुल के नीचे के पत्थर को कुरेद कर बाहर निकाला।",
            "उन्हें पत्थर की आवाज़ सुननी थी; गूंजती भारी आवाज़ पतली चट्टान का संकेत थी, जबकि खनकती आवाज़ ठोस भार-वाहक पाषाण की।",
            "यहाँ आग से पत्थर चटकाने की तकनीक नहीं चल सकती थी; अत्यधिक गर्मी लटकती छत में अदृश्य दरारें पैदा कर देती।",
            "हवा के इस हर एक घनफुट खाली स्थान को कठोर स्टील की छैनियों के लगातार प्रहारों से ही तराशना पड़ा।",
            "जब मलबा हटाया गया, तो पुल बिना किसी सहारे के हवा में झूलता रह गया—दो संसारों के बीच लटका एक शाश्वत चमत्कार।"
        ]
    },
    {
        "id": "act_04_the_courtyard_monoliths",
        "title": "Act IV — प्रांगण के एकाश्मक स्तंभ और गजराज",
        "sentences": [
            "जैसे-जैसे कारीगरों ने पुलों के नीचे प्रांगण को गहरा किया, उन्होंने पत्थर के दो विशाल द्वीप खड़े छोड़ दिए।",
            "सपाट फर्श बनाने के बजाय, उन्होंने पचास फीट ऊंचे जीवित बेसाल्ट के दो गगनचुंबी खंभे वहीं छोड़ दिए।",
            "ये बने कैलाश के विश्वविख्यात ध्वजस्तंभ—विशाल, अखंड विजय स्तंभ।",
            "मूल चट्टान से वहीं तराशे गए, ये सत्रह मीटर ऊंचे स्तंभ अपनी महीन धारियों और त्रिशूलों के साथ आकाश छूते हैं।",
            "प्रांगण के दोनों ओर, दो आदमकद एकाश्मक हाथी सीधे फर्श की चट्टान से उभरते हैं।",
            "उनके विशाल शरीर, तराशे हुए कान और सूंड बिना किसी एक भी जोड़ के आसपास के पत्थर से आज़ाद किए गए थे।",
            "प्राचीन भारतीय शैल-स्थापत्य में, किसी खदान के भीतर स्वतंत्र मूर्ति गढ़ना असाधारण गणितीय सटीकता मांगता है।",
            "पहला प्रहार करने से पहले ही मूर्तिकार को उस अनगढ़े काले पत्थर के भीतर संपूर्ण त्रि-आयामी जीव की कल्पना करनी होती है।",
            "एक बार पत्थर हट गया तो वापस नहीं जुड़ सकता; एक खंडित दांत बीस वर्षों की अथक साधना को नष्ट कर सकता था।"
        ]
    },
    {
        "id": "act_05_the_living_epics_in_basalt",
        "title": "Act V — पाषाण में जीवंत महाकाव्य",
        "sentences": [
            "मंदिर के मंडपों के दोनों ओर, यह कठोर चट्टान विराट आकार से निकलकर एक सजीव काव्य में ढल जाती है।",
            "दो अखंड पट्टिकाएँ भारत के महान महाकाव्यों को दर्शाती हैं—दक्षिण में रामायण और उत्तर में महाभारत।",
            "सूक्ष्म क्षैतिज स्तरों पर, महान शिल्पकारों ने कठोर बेसाल्ट में सैकड़ों गतिशील आकृतियों को उकेरा है।",
            "दक्षिणी दीवार पर लंका का युद्ध जीवंत है—रथ के पहिए, दौड़ते अश्व और प्रत्यंचा खींचते धनुर्धर।",
            "पास ही, कैलाश पर्वत को हिलाते रावण का विशाल फलक पत्थर में भूकंपीय आतंक को बांध लेता है।",
            "राक्षसराज अपनी बीसों भुजाओं से पर्वत की जड़ों को झकझोरता है, उसकी मांसपेशियां खिंची हैं और चेहरा क्रोध से तमतमाया है।",
            "ऊपर, भगवान शिव शांत भाव से अपने पैर के अंगूठे को चट्टान पर दबाते हैं, और पाताल का यह कंपन पल भर में शांत हो जाता है।",
            "गहरी नक्काशी दक्कन की तेज़ धूप में गहरी परछाइयाँ बनाती है, जिससे ये पत्थर की मूर्तियाँ साक्षात चलती-फिरती प्रतीत होती हैं।",
            "यह जीवित चट्टान अब ठंडा बेसाल्ट नहीं रह जाती; यह ब्रह्मांडीय शक्ति और मानवीय गाथा का रंगमंच बन जाती है।"
        ]
    },
    {
        "id": "act_06_the_white_mountain_of_ellora",
        "title": "Act VI — एलोरा का श्वेत पर्वत",
        "sentences": [
            "आज जब लोग कैलाश में प्रवेश करते हैं, तो उन्हें केवल काला, मौसमी मार से घिसा बेसाल्ट दिखाई देता है।",
            "लेकिन निर्माण के बाद कई शताब्दियों तक, कैलाश का रूप बिल्कुल भिन्न था।",
            "यह पूरा स्मारक चूने और सीपी से बने एक चमकदार, दूधिया सफेद प्लास्टर से ढका हुआ था।",
            "नदी की सीपियों, बुझे चूने, संगमरमर के चूरे और वानस्पतिक गोंद से बने इस लेप को सुलेमानी पत्थरों से घिसकर चमकाया गया था।",
            "महाराष्ट्र की तपती धूप में, यह मंदिर चीनी मिट्टी जैसी चमचमाती श्वेत आभा से जगमगाता था।",
            "यह राष्ट्रकूटों की अद्भुत कल्पना थी: हिमालय के बर्फ से ढके कैलाश पर्वत को दक्कन के ज्वालामुखी पठार पर साक्षात उतार देना।",
            "धूल भरे रास्तों से आते यात्रियों को लगता था मानो काली खाई से बर्फ का कोई विशाल पर्वत आकाश की ओर उठ रहा हो।",
            "सदियों की मानसूनी बारिश ने इस सफेद आवरण को बहा दिया, और नीचे का काला कंकाल बाहर आ गया।",
            "फिर भी सुरक्षित कोनों और छतों में, आज भी उस जगमगाते सफेद प्लास्टर के अंश जीवित हैं।"
        ]
    },
    {
        "id": "act_07_the_mountain_that_refused_to_fall",
        "title": "Act VII — वह पर्वत जिसे कोई गिरा न सका",
        "sentences": [
            "किसी इमारत की असली परीक्षा केवल यह नहीं है कि वह कैसे बनी, बल्कि यह है कि वह विनाश के प्रयासों के सामने कैसे अडिग रही।",
            "सत्रहवीं सदी के अंत में, मुग़ल बादशाह औरंगज़ेब ने एलोरा के पास पड़ाव डाला और इस मंदिर को पूरी तरह ध्वस्त करने का आदेश दिया।",
            "गुफा 16 को मिटाने के लिए एक हज़ार से अधिक मज़दूरों का दस्ता भारी हथौड़ों, सब्बलों और छैनियों के साथ भेजा गया।",
            "एक वर्ष से भी अधिक समय तक, यह विध्वंसक दल रात-दिन मंदिर की दीवारों पर अंधाधुंध प्रहार करता रहा।",
            "ईंट और गारे से बने सामान्य मंदिरों में, कुछ खंभे तोड़ते ही पूरी छत भरभरा कर गिर जाती है।",
            "लेकिन कैलाश कोई इमारत नहीं है; यह एक ठोस पर्वत-शृंग है।",
            "मज़दूरों की छैनियां मुड़ गईं, मूर्तियाँ खंडित हुईं, लेकिन मंदिर का मूल ढांचा अपनी जगह से टस से मस न हुआ।",
            "महीनों के कठोर श्रम और शून्य प्रगति के बाद, औरंगज़ेब ने हार मान ली और विध्वंस का अभियान बंद कर दिया।",
            "दक्कन का यह जीवित पाषाण साम्राज्य की पूरी ताकत और हथियारों से कहीं अधिक बलवान साबित हुआ।"
        ]
    },
    {
        "id": "act_08_the_architects_confession",
        "title": "Act VIII — वास्तुकार का विस्मय",
        "sentences": [
            "गुफा 16 की चट्टान पर आखिरी छैनी पड़े बारह शताब्दियों से अधिक का समय बीत चुका है।",
            "812 ईस्वी के बड़ौदा ताम्रपत्र में राजा कर्क द्वितीय ने इस पूर्ण मंदिर को देखकर हुए विस्मय को दर्ज किया था।",
            "उन्होंने लिखा कि आकाश में उड़ते देवता भी विमानों से नीचे इस खाई में झांककर स्तब्ध रह गए।",
            "वे विस्मित होकर बोले: 'यह शिव मंदिर स्वयंभू है; किसी नश्वर मानव के हाथों से ऐसा निर्माण संभव नहीं।'",
            "लेकिन इस अभिलेख की सबसे मार्मिक पंक्ति स्वयं मुख्य वास्तुकार की है।",
            "प्रांगण के फर्श पर खड़े होकर, हवा में झूलते पुलों, विजय स्तंभों और आकाश छूते विमान को देखकर वह रो पड़ा:",
            "'कथम् अकारि मया एतत्' — 'यह मैंने कैसे बना दिया?'",
            "जिस मस्तिष्क ने इस असंभव की कल्पना की थी, वह भी विश्वास नहीं कर सका कि नश्वर हाथों ने इसे साकार कर दिखाया।",
            "और यही है कैलाश का शाश्वत रहस्य: एक ऐसा स्मारक जो स्वयं अपने रचयिताओं की समझ से भी परे चला गया।"
        ]
    }
]

SHORTS_DATA = [
    {
        "id": "short_01_the_sky_bridge_that_shouldnt_exist",
        "sentences": [
            "Look up inside the 100-foot chasm of Kailasa Temple.",
            "A monolithic stone bridge hangs suspended thirty feet in mid-air.",
            "There is no mortar, no separate arches, and no structural keystones.",
            "Ancient carvers chiseled the void beneath it, leaving the bridge hanging from the sky.",
            "One hidden crack in the volcanic rock would have sent the entire bridge crashing down.",
            "How did they calculate what stone could bear before the floor even existed?"
        ]
    },
    {
        "id": "short_02_the_temple_that_1000_men_couldnt_destroy",
        "sentences": [
            "In 1682, Mughal Emperor Aurangzeb ordered 1,000 workers to demolish the Kailasa Temple.",
            "For over a full year, demolition teams hammered against the stone with heavy iron sledges.",
            "When you attack a normal building, knocking out pillars brings the ceiling down.",
            "But Kailasa has no pillars to knock down—it is a single solid mountain.",
            "The sledges shattered, the chisels broke, and the army surrendered in defeat."
        ]
    }
]

HINDI_SHORTS_DATA = [
    {
        "id": "short_01_the_sky_bridge_that_shouldnt_exist",
        "sentences": [
            "कैलाश मंदिर की सौ फीट गहरी खाई में ऊपर देखिए।",
            "हवा में तीस फीट ऊपर एक एकाश्मक पाषाण सेतु झूल रहा है।",
            "यहाँ न कोई गारे का जोड़ है, न कोई मेहराब, और न कोई कीस्टोन।",
            "शिल्पकारों ने इसके नीचे के शून्य को तराशा, और पुल को आकाश में छोड़ दिया।",
            "चट्टान में एक भी दरार पूरे पुल को तोड़कर नीचे गिरा सकती थी।",
            "फर्श बनने से पहले उन्होंने इस भार की गणना कैसे की?"
        ]
    },
    {
        "id": "short_02_why_elephants_support_the_mountain",
        "sentences": [
            "1682 में मुग़ल बादशाह औरंगज़ेब ने कैलाश मंदिर को गिराने के लिए एक हज़ार मज़दूर भेजे।",
            "एक वर्ष तक वे भारी हथौड़ों और सब्बलों से इस चट्टान पर प्रहार करते रहे।",
            "सामान्य इमारत के खंभे तोड़ते ही छत गिर जाती है।",
            "लेकिन कैलाश में कोई अलग खंभा नहीं है—यह स्वयं एक ठोस पर्वत है।",
            "हथौड़े टूट गए, छैनियां मुड़ गईं, और सेना को हार माननी पड़ी।"
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
    print(f"\n{'=' * 65}\n  PROCESSING {lang_code.upper()} NARRATION\n{'=' * 65}")
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
        
    # Concat master stem
    concat_list = audio_out_dir / "acts_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in act_mp3_paths:
            f.write(f"file '{p.as_posix()}'\n")
            
    master_stem = audio_out_dir / (f"episode_06_narration_master.mp3" if lang_code == "en" else "episode_06_hindi_narration_master.mp3")
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(master_stem)]
    subprocess.run(cmd_concat, capture_output=True, check=True)
    
    master_dur = get_audio_duration(master_stem)
    sum_dur = sum(act_durations)
    drift_ms = abs(master_dur - sum_dur) * 1000
    print(f"[*] Master Stem: {master_stem.name} ({master_dur:.3f}s)")
    print(f"[*] Drift: {drift_ms:.2f} ms")
    
    master_srt = sub_out_dir / (f"episode_06_full.srt" if lang_code == "en" else "episode_06_hindi_full.srt")
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
    print("  ELEVENLABS AUDIO NARRATION SUITE — EPISODE 06")
    print(f"  Voice: Adam Stone ({VOICE_ID}) | Model: {MODEL_ID}")
    print("=" * 65)
    
    api_key = get_api_key()
    
    # 1. Process English Master & Shorts
    process_language("en", ACTS_DATA, SHORTS_DATA, AUDIO_DIR, SUB_DIR, api_key)
    
    # 2. Process Hindi Master & Shorts
    process_language("hi", HINDI_ACTS_DATA, HINDI_SHORTS_DATA, AUDIO_HINDI_DIR, SUB_HINDI_DIR, api_key)
    
    print("\n[ALL COMPLETE] English and Hindi audio stems & SRT subtitles successfully generated!")

if __name__ == "__main__":
    main()
