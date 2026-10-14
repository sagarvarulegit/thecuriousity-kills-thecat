"""
Episode 1 Narration & Subtitle Synthesizer using Edge-TTS
Generates high-definition neural voiceovers and synchronized .srt subtitles.
"""

import asyncio
import os
import edge_tts

# Target voice: en-US-ChristopherNeural (authoritative, cinematic) or en-IN-PrabhatNeural
VOICE = "en-US-ChristopherNeural"

EPISODE_ACTS = [
    {
        "act": "act_01_the_vow",
        "title": "Act I: The Crisis & The Fatal Vow",
        "text": (
            "In the year 756 of our common era, an impossible crisis gripped the royal court of the Rashtrakuta Empire. "
            "Deep within the stone corridors of the capital, King Krishna the First lay struck down by a mysterious, wasting illness. "
            "Imperial physicians could do nothing. With each passing night, the ruler of western India slipped closer to the grave. "
            "According to the ancient chronicles of the Katha-Kalpataru, his queen made a desperate, terrifying vow. "
            "She swore an oath to Shiva: she would touch no food, she would fast to death, until she could gaze upon the finished spire of a temple raised in his honor. "
            "The King miraculously recovered. The royal court rejoiced. But their celebration turned instantly to horror. "
            "The queen was already weakening. The vow could not be broken. She would not eat until she saw the shikhara, the pinnacle of the temple. "
            "The King summoned the greatest master builders of the Deccan. He demanded an immediate solution. "
            "Their reply was a death sentence. To quarry stone, build foundations, and erect timber scaffolding to raise a spire would take twenty years. "
            "Before the foundation stones could even settle into the earth, the queen would starve to death."
        )
    },
    {
        "act": "act_02_the_heresy",
        "title": "Act II: The Architect's Heresy",
        "text": (
            "Into the despair of the imperial council stepped a solitary master builder whose name would live for twelve hundred years: Kokasa. "
            "Kokasa was a master Sthapati from central India, an engineer who did not merely follow tradition; he commanded the laws of physics. "
            "Before the astonished king, Kokasa made an outrageous declaration: 'Your Majesty, the Queen will behold the temple's pinnacle in seven days.' "
            "The court scoffed. Seven days? Seven days was impossible even to clear the brushwood, let alone build a spire. "
            "Every temple in the world was additive: quarried blocks stacked from the ground up, requiring years of wooden scaffolding. "
            "Kokasa's plan was pure subtractive heresy. They would not build up. They would climb to the mountain's crest, and carve downward. "
            "By starting at the very summit, the spire, the shikhara, would be carved first. In one week, the queen could look up from the valley and see it gleaming in the sun. "
            "This was the secret doctrine of the Shilpa Shastras: deductive excavation. The mountain was not raw material; it was the temple itself, waiting to be freed. "
            "No scaffolding. No hauling granite from distant quarries. The mountain's own stone would serve as its working platform. "
            "The King made his choice: 'Find the mountain. We begin immediately.'"
        )
    },
    {
        "act": "act_03_geology",
        "title": "Act III: Scouting & Geology of Charanandri",
        "text": (
            "Kokasa rode out into the rugged expanse of the Western Deccan. He was not looking for beauty; he was looking for raw lithological strength. "
            "Sixty-six million years earlier, at the end of the age of dinosaurs, the earth tore open. Millions of cubic kilometers of molten lava flooded the region. "
            "Layer upon layer cooled into stacked horizontal sheets of tholeiitic basalt, creating the towering terraces of the Sahyadri mountains. "
            "Kokasa arrived at Elapura, the sacred Charanandri ridge. A gently sloping escarpment rising thirty meters above the plain. "
            "The location was geographically perfect: it stood adjacent to the sacred Shiva shrine of Ghrishneshwar, and directly guarded the Dakshinapatha trade corridor. "
            "Existing caves had already been carved here by Buddhist and Hindu ascetics. Kokasa knew the rock held together. But was it strong enough for a monolith? "
            "He took a bronze testing mallet and struck the upper rock shelf. If the stone rang with a dull, hollow thud, it was amygdaloidal, full of weak zeolite bubbles that would shatter under stress. "
            "He moved further down the ridge and struck again. This time, the stone rang out like a temple bell: a clear, high-pitched metallic chime. "
            "This was dense microcrystalline basalt. Its compressive strength exceeded one hundred and forty megapascals, twice as strong as modern structural concrete. "
            "Kokasa turned to his apprentices: 'Here is our mountain. It will hold the house of Shiva.'"
        )
    },
    {
        "act": "act_04_capital",
        "title": "Act IV: The Imperial War Chest & Capital",
        "text": (
            "Carving four hundred thousand tons of mountain is not merely an act of faith; it is an astronomical economic undertaking. "
            "In modern terms, Kailasa was a billion-dollar megaproject. Where did King Krishna the First find such capital? "
            "First: Imperial conquest. Krishna had just crushed the legendary Chalukyas of Badami, looting their royal treasuries and seizing decades of accumulated gold. "
            "Second: Agrarian tax decentralization. The king did not simply spend gold; he re-engineered the economy of the region. "
            "By issuing royal copper-plate grants, he transferred the tax revenues of dozens of surrounding farming villages directly to the temple works. "
            "Every week, convoys of bullock carts arrived at Elapura carrying tons of rice, lentils, dried cow dung, and sesame oil to sustain the workforce. "
            "Third: The merchant guilds, the Shrenis. Wealthy caravan syndicates operating along the Silk Road branches poured private fortunes into the temple. "
            "In exchange for funding, merchants received royal tax exemptions, toll-free passage through mountain passes, and sacred merit in the eyes of the gods. "
            "Even the Buddhist and Hindu monasteries on the ridge functioned as financial escrow hubs, managing endowments and lending credit to caravan travelers. "
            "The war chest was full. The supply lines were locked. Now, Kokasa needed to assemble the greatest engineering guild in human history."
        )
    },
    {
        "act": "act_05_guilds",
        "title": "Act V: The Guild of Masters & Weaponry",
        "text": (
            "Over the course of three months, hundreds of specialized artisans and their families arrived at the base of the Charanandri ridge. "
            "Kokasa did not use slave labor. This was a professional hereditary guild of freemen, organized into strict technical hierarchies. "
            "At the top were the Sutradharas, the Holders of the String. The elite geometricians who would translate three-dimensional temple geometry into raw stone. "
            "Beneath them were the Takshakas, the stone hewers. Men with iron wrists who understood how to shatter volcanic basalt without cracking the strata below. "
            "Waiting in reserve were the Rupakaras, the sculptors. Artists whose chisels would liberate dancing deities, charging elephants, and celestial maidens from the rock. "
            "But without weapons, the army was useless. Diamond-hard basalt destroys iron tools in hours. "
            "Day and night, specialized blacksmiths kept charcoal furnaces blazing at twelve hundred degrees Celsius. "
            "They forged high-carbon wootz-type steel chisels, quenching red-hot iron in oil and water to give the tips diamond-like hardness. "
            "Three tools were perfected: the pointed punch for bulk splitting, the claw chisel for leveling, and the flat gouge for fine sculpture. "
            "Ten thousand iron chisels were stacked ready for battle. The tools were forged. The army stood waiting."
        )
    },
    {
        "act": "act_06_survey",
        "title": "Act VI: Surveying the Living Stone",
        "text": (
            "At dawn on the auspicious day of the full moon, Kokasa and his senior surveyors climbed to the flat summit of the Charanandri ridge. "
            "Their first act was not carving, but astronomy. In the center of the summit, they drove a tapered wooden pole into the bedrock: the sacred Shanku. "
            "Using a cord tied to the pole, they etched a circle in the rock. As the sun rose and set, the shadow touched the circle at dawn and dusk, revealing the true East-West line. "
            "This established the sacred axis: Kailasa would face exact West, greeting the setting sun. "
            "The surveyors held a long twisted cord soaked in brilliant red vermilion powder taut across eighty meters of flat rock summit. "
            "The surveyor pulled the cord three feet into the air, and released it. "
            "A razor-straight red line cut across the volcanic stone. Then another. And another. "
            "They laid out the master boundary: an enormous U-shaped trench footprint: eighty-four meters long, forty-seven meters wide. "
            "Between those trenches lay a colossal monolith of isolated mountain: fifty meters long, thirty-three meters deep. Inside that uncarved stone was the entire temple. "
            "To guarantee the trenches descended perfectly vertical, they used water leveling troughs. If one cut drifted by even three inches, a column below would shatter. "
            "By sunset, the mountain was chained in sacred geometry. The blueprint was physically etched into the living earth."
        )
    },
    {
        "act": "act_07_council",
        "title": "Act VII: The Royal Council & The Imperial Seal",
        "text": (
            "Kokasa returned to the imperial court carrying a miniature terracotta model of the mountain, carved with its descending trenches. "
            "King Krishna gazed upon the miniature. For the first time, he saw how the miracle would work. "
            "He looked toward the inner chambers where his queen lay fading. Seven days. The promise had to be kept. "
            "He called for the royal seal. "
            "King Krishna pressed his heavy gold signet ring, the winged eagle Garuda, emblem of the Rashtrakutas, into the molten red wax. "
            "The royal decree was sealed: 'Let the mountain of Elapura be fashioned into the abode of the Lord of Kailasa.' "
            "Kokasa accepted the copper plate. He did not smile. He knew that from this moment on, every blow of the hammer was a fight against time. "
            "That night, an endless serpentine river of torches climbed the road to Charanandri. The quarrymen took their stations."
        )
    },
    {
        "act": "act_08_first_strike",
        "title": "Act VIII: The First Strike & Cliffhanger",
        "text": (
            "Dawn, the seventh day before the queen's deadline. Total silence descended upon the mountain ridge. "
            "At the exact center of the grid, Kokasa placed the point of a heavy steel punch against the virgin black basalt. "
            "Beside him stood the master striker. A seasoned quarryman with arms like iron bands. He raised a thirty-pound basalt sledgehammer high into the morning air. "
            "Four hundred thousand tons of mountain. Hundreds of thousands of man-hours. It all began with a single breath. "
            "Iron met basalt. "
            "And the living stone cracked. "
            "In Episode Two: Kokasa unleashes the ancient world's most destructive engineering weapon, fire and cold water, to carve three colossal trenches thirty meters into the earth. "
            "Subscribe, and step into the fire."
        )
    }
]

SHORTS = [
    {
        "id": "short_01",
        "name": "short_01_the_queen_vow",
        "text": (
            "In the 8th century, an Indian Queen made a vow that should have killed her. "
            "Her husband, the King, recovered from a deadly illness. In gratitude, she vowed to fast to death until she could see the pinnacle of a temple built for Shiva. "
            "Royal architects told the king: 'It will take twenty years to build from the ground up. The Queen will starve.' "
            "Then one architect named Kokasa stepped forward with an engineering heresy: 'I will show you the spire in seven days.' "
            "How? Every builder built from the ground up. He decided to climb the mountain and carve downward from the clouds! "
            "In seven days, the queen saw the pinnacle and broke her fast. Beneath it lay four hundred thousand tons of solid rock that became the world's greatest monolithic temple. "
            "Watch Episode One of our full documentary series linked below to see how this impossible plan was actually funded and engineered!"
        )
    },
    {
        "id": "short_02",
        "name": "short_02_billion_dollar_mountain",
        "text": (
            "How much did it cost to carve a multi-story cathedral out of solid mountain? "
            "In modern money: over one billion dollars. "
            "Source one: War spoils. King Krishna the First crushed the rival Chalukyan empire and dumped entire wagon loads of captured royal gold and silver directly into the project's war chest. "
            "Source two: The king signed copper charters donating the taxes of dozens of farming villages to feed thousands of quarrymen every single day. "
            "And source three: Silk Road merchant guilds, who traded fortunes in gold for tax-free mountain trade passes. "
            "Without this financial machine, the mountain would never have been touched. "
            "See how the master engineers were recruited in Episode One linked below!"
        )
    }
]

async def generate_speech(text: str, output_path: str, vtt_path: str = None):
    communicate = edge_tts.Communicate(text, VOICE, rate="-4%", pitch="-2Hz")
    if vtt_path:
        submaker = edge_tts.SubMaker()
        with open(output_path, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.feed(chunk)
        with open(vtt_path, "w", encoding="utf-8") as file:
            file.write(submaker.get_srt())
    else:
        await communicate.save(output_path)

async def main():
    audio_dir = "ajanta-ellora/assets/episode-01/audio"
    sub_dir = "ajanta-ellora/assets/episode-01/subtitles"
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(sub_dir, exist_ok=True)

    print(f"Synthesizing voiceover with neural voice: {VOICE}")

    # Generate each act
    for i, act in enumerate(EPISODE_ACTS):
        out_mp3 = os.path.join(audio_dir, f"{act['act']}.mp3")
        out_srt = os.path.join(sub_dir, f"{act['act']}.srt")
        print(f"Generating {act['title']}...")
        await generate_speech(act["text"], out_mp3, out_srt)

    # Generate full episode combined narration
    print("Generating Full Episode 1 Combined Voiceover...")
    full_text = " ".join([act["text"] for act in EPISODE_ACTS])
    full_mp3 = os.path.join(audio_dir, "episode_01_full_narration.mp3")
    full_srt = os.path.join(sub_dir, "episode_01_full.srt")
    await generate_speech(full_text, full_mp3, full_srt)

    # Generate Shorts
    for short in SHORTS:
        print(f"Generating {short['name']}...")
        s_mp3 = os.path.join(audio_dir, f"{short['name']}.mp3")
        s_srt = os.path.join(sub_dir, f"{short['name']}.srt")
        await generate_speech(short["text"], s_mp3, s_srt)

    print("\nAll Voiceovers and Subtitles generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
