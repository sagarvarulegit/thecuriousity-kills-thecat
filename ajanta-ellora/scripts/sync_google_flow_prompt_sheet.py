import json
from pathlib import Path

# Data for 16 Google Flow action shots sorted chronologically by cut
ACTION_SHOTS = [
    {
        "shot_num": 1,
        "cut_num": 16,
        "act": "Act II",
        "title": "Pecking the Basalt Mechanical Key",
        "base_img": "ep08_gf_05_chipping_basalt_key_sparks_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_05_chipping_basalt_key_sparks.mp4",
        "duration": "4.5s",
        "spoken_beat": "First, stonecutters used pointed iron picks to peck thousands of small pits into the rock, creating a rough surface for the mud to grip.",
        "prompt": "Authentic historical action. A skilled ancient stonecutter striking a pointed iron pick chisel against dark volcanic basalt wall. Rapid, precise hammer strikes pecking small pit dimples across the stone face. Tiny sharp rock chips fly off, momentary bright orange sparks flick off the dark igneous rock, fine basalt dust puffs in raking sunlight. Intense focus, sweat on the craftsman's brow, raw tactile stonecraft.",
        "camera": "Macro side-profile push-in focusing on the chisel impact point and spark bursts."
    },
    {
        "shot_num": 2,
        "cut_num": 18,
        "act": "Act II",
        "title": "Kneading the Organic Mud Matrix",
        "base_img": "ep08_gf_04_plaster_kneading_cowdung_matrix_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_04_plaster_kneading_cowdung_matrix.mp4",
        "duration": "5.5s",
        "spoken_beat": "Using fermented cow dung was not dirty—it was pure organic chemistry.",
        "prompt": "Historical reenactment documentary. Barefoot ancient Indian craftsmen in coarse dhoti waistcloths rhythmically treading and kneading thick organic reddish-brown mud plaster inside a rough wooden mixing pit. Golden rice husks, dry plant fibers, and dense wet clay squishing between toes with real physical weight and viscous mud resistance. Splashes of muddy water, realistic organic texture, warm natural daylight outside the rock shelter.",
        "camera": "Low-angle panning shot across the mud trough showing rhythmic footwork and wet mud texture."
    },
    {
        "shot_num": 3,
        "cut_num": 21,
        "act": "Act II",
        "title": "Spreading the Lime Plaster Finish Coat",
        "base_img": "ep08_gf_17_artisan_spreading_lime_plaster_finish_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_17_artisan_spreading_lime_plaster_finish.mp4",
        "duration": "5.0s",
        "spoken_beat": "Finally, craftsmen spread a paper-thin finish coat made of slaked lime, powdered gypsum, and crushed sea shells.",
        "prompt": "Ancient master craftsmanship documentary. Close-up of an ancient Indian artisan in coarse linen using a curved teak wooden float trowel to spread a paper-thin, brilliant white slaked lime and crushed oyster shell plaster finish across a dry red clay bio-mud wall. The creamy white plaster flows smoothly under the wooden float, forming a pristine, porcelain-like coating over the dark red mud. Raking warm lantern light, realistic wet plaster spread.",
        "camera": "Macro tracking shot following the curved wooden float as it glides upward, laying down the smooth white plaster."
    },
    {
        "shot_num": 4,
        "cut_num": 23,
        "act": "Act II",
        "title": "Agate Stone Burnishing",
        "base_img": "ep08_gf_06_agate_burnishing_intonaco_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_06_agate_burnishing_intonaco.mp4",
        "duration": "5.0s",
        "spoken_beat": "Under the friction of the smooth agate stone, the chalky lime compacted into a gleaming, ivory-smooth surface ready for paint.",
        "prompt": "Tactile macro craftsmanship. An artisan's strong, steady hand pressing a banded river agate stone against a fresh white slaked lime wall. Steady, circular rubbing strokes burnishing the wet plaster, visibly compressing the chalky surface into a smooth, glossy porcelain-like ivory sheen. Natural light glinting across the newly polished plaster surface. Intimate, authentic, zero digital effects.",
        "camera": "Close-up steady tracking following the smooth circular rubbing stroke of the agate stone."
    },
    {
        "shot_num": 5,
        "cut_num": 24,
        "act": "Act III",
        "title": "Uncapping Pigment Bowls & Dipping Brush",
        "base_img": "ep08_gf_18_dipping_bamboo_brush_pigment_bowl_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_18_dipping_bamboo_brush_pigment_bowl.mp4",
        "duration": "4.5s",
        "spoken_beat": "Once the plaster dried, the painters uncapped their earthenware pigment bowls.",
        "prompt": "Intimate artist studio documentary. Weathered, paint-flecked hand of an ancient Indian master painter lifting an earthenware lid off a rustic terracotta pigment bowl, then dipping the fine natural bristles of a bamboo brush into thick, wet, vibrant lapis lazuli ultramarine paint. Swirls of deep azure liquid pigment pool around the dipping brush, soft natural morning daylight raking across clay jars and pigment bowls.",
        "camera": "Macro push-in onto the terracotta bowl as the brush dips and swirls the deep blue paint."
    },
    {
        "shot_num": 6,
        "cut_num": 25,
        "act": "Act III",
        "title": "Crushing Volcanic Ochre Minerals",
        "base_img": "ep08_gf_20_crushing_volcanic_ochre_pestle_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_20_crushing_volcanic_ochre_pestle.mp4",
        "duration": "4.5s",
        "spoken_beat": "For red and yellow colors, they crushed local volcanic ochre rocks dug right from the Deccan soil.",
        "prompt": "Ancient pigment chemistry craft. Close-up of strong hands using a heavy stone pestle to pound and pulverize raw chunks of volcanic red hematite and yellow ochre rocks inside a deep basalt mortar. The brittle ochre rocks fracture under the rhythmic blows, bursting into vivid terracotta-red and saffron-yellow mineral dust that settles into smooth paint powder. Raking golden sunlight, realistic rock splintering and mineral dust.",
        "camera": "Low-angle macro shot capturing the rhythmic impact of the pestle and bursts of ochre powder."
    },
    {
        "shot_num": 7,
        "cut_num": 26,
        "act": "Act III",
        "title": "Mustard Oil Lamp & Soot Collection",
        "base_img": "ep08_gf_14_mustard_oil_lamp_soot_smoke_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_14_mustard_oil_lamp_soot_smoke.mp4",
        "duration": "4.5s",
        "spoken_beat": "For green, they ground green earth minerals; for pure black, they collected soot from burning mustard oil lamps.",
        "prompt": "Traditional ancient chemistry craft. A small terracotta oil diya lamp burning with a steady golden flame fed by mustard oil. An inverted earthenware bowl held just above the flame collecting dense, velvety black carbon soot. A thin curl of realistic dark smoke rises gently against dark clay walls. Authentic craftsmanship, warm firelight reflections on clay vessels.",
        "camera": "Macro focus pulling from burning yellow flame to dense black carbon soot collecting on pottery."
    },
    {
        "shot_num": 8,
        "cut_num": 34,
        "act": "Act III",
        "title": "Grinding Lapis Lazuli Crystals",
        "base_img": "ep08_gf_03_mortar_grinding_lapis_powder_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_03_mortar_grinding_lapis_powder.mp4",
        "duration": "5.0s",
        "spoken_beat": "Only the wealthiest royal emperors and ministers could afford to paint entire cave ceilings in imported blue.",
        "prompt": "Macro documentary realism. Weathered, clay-stained hands of an ancient Indian artisan holding a heavy granite pestle, grinding raw deep-blue crystalline lapis lazuli minerals inside a stone mortar. Solid stone-on-stone crushing friction, blue mineral shards fracturing into intense azure powder, clear water poured from an earthenware jug creating swirling deep-blue paint paste. Natural raking daylight through cave archway, 100% tangible physical textures.",
        "camera": "Slow macro push-in focusing on the grinding contact point in the mortar."
    },
    {
        "shot_num": 9,
        "cut_num": 45,
        "act": "Act IV",
        "title": "Bronze Mirror Sunlight Diversion",
        "base_img": "ep08_gf_07_bronze_mirror_sunlight_beam_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_07_bronze_mirror_sunlight_beam.mp4",
        "duration": "5.5s",
        "spoken_beat": "Outside in the blazing sunshine, assistants positioned large, circular mirrors made of highly polished cast bronze.",
        "prompt": "Historical optical engineering. An ancient Indian apprentice adjusting a large, circular cast-bronze mirror mounted on a heavy timber tripod on the sunlit cave veranda. The mirror's hand-polished golden metal catches the blazing midday tropical sun, casting a powerful, solid beam of reflected natural sunlight cutting straight through the dusty air into the dark cavern doorway. Physically accurate optics, dust motes drifting through the solar ray.",
        "camera": "Dynamic slow pan from bronze mirror surface down the bright reflected beam of light into cave portal."
    },
    {
        "shot_num": 10,
        "cut_num": 48,
        "act": "Act IV",
        "title": "Wet Linen Sheet Sunlight Diffuser",
        "base_img": "ep08_gf_15_wet_linen_diffuser_light_beam_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_15_wet_linen_diffuser_light_beam.mp4",
        "duration": "5.0s",
        "spoken_beat": "When the intense sunbeam hit the wet white cloth, the light bounced and scattered, filling the dark underground hall with a soft, bright, shadowless glow.",
        "prompt": "Ancient optical demonstration. Two young Indian apprentice boys holding a stretched sheet of bleached, wet white cotton fabric inside a dark rock cave. A concentrated beam of reflected sunlight strikes the wet cloth, instantly diffusing into a bright, glowing lantern effect that bathes the surrounding dark stone pillars and carved wall reliefs in soft, even, shadowless white light. Pure practical physics, tangible wet cloth weave.",
        "camera": "Smooth tracking shot from the bright point of impact on the cloth to the glowing cave wall behind it."
    },
    {
        "shot_num": 11,
        "cut_num": 49,
        "act": "Act IV",
        "title": "Reflected Sun Illuminating the Great Hall",
        "base_img": "ep08_gf_09_cave_interior_sunlit_murals_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_09_cave_interior_sunlit_murals.mp4",
        "duration": "6.0s",
        "spoken_beat": "The ancient painters were literally painting forty meters underground using captured natural sunlight.",
        "prompt": "Subterranean architectural reveal. Moving smoothly forward between colossal carved stone columns inside Cave One. Gentle, soft, diffused golden sunlight sweeps across the painted ceiling mandalas and wall murals, revealing vibrant turquoise lapis blues, terracotta reds, and golden figures glowing in natural daylight deep inside the rock cave. Ancient monks and painters quietly working along scaffolding in background. Majestic, quiet, authentic.",
        "camera": "Slow forward dolly gliding between carved columns, gazing up as murals emerge into soft light."
    },
    {
        "shot_num": 12,
        "cut_num": 50,
        "act": "Act V",
        "title": "Painting the Eyelashes of Padmapani",
        "base_img": "ep08_gf_08_brush_applying_lapis_eyelash_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_08_brush_applying_lapis_eyelash.mp4",
        "duration": "5.0s",
        "spoken_beat": "Illuminated by this soft, redirected sunlight, ancient artists created the greatest masterpieces of ancient world art.",
        "prompt": "Extreme macro art restoration footage. A thin bamboo brush tipped with ultra-fine squirrel hair gently painting a razor-sharp, flowing black eyeliner contour on the smooth ivory plaster face of Bodhisattva Padmapani. Hand trembles slightly with human breath, liquid pigment soaking smoothly into plaster pores, soft diffused natural daylight softly illuminating the artwork. Intimate historical masterwork in progress.",
        "camera": "Extreme macro slow push-in tracking the brush tip gliding across ivory plaster."
    },
    {
        "shot_num": 13,
        "cut_num": 52,
        "act": "Act V",
        "title": "Painting the Blue Lotus Blossom",
        "base_img": "ep08_gf_19_painting_blue_lotus_padmapani_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_19_painting_blue_lotus_padmapani.mp4",
        "duration": "5.0s",
        "spoken_beat": "Look closely at his gentle expression, his regal crown, and the downward curve of his eyes full of compassion.",
        "prompt": "Masterpiece craftsmanship in progress. Extreme macro view of an ancient master artist's hand holding a fine bamboo brush, delicately applying vivid electric-blue lapis lazuli paint onto the petals of the sacred lotus blossom held in the fingers of Bodhisattva Padmapani on the ivory cave wall. The wet ultramarine paint flows smoothly across the white plaster, glowing under soft diffused natural sunlight. Intimate, sacred artistry.",
        "camera": "Slow macro push-in focusing on the brush tip painting the rich blue lotus petals."
    },
    {
        "shot_num": 14,
        "cut_num": 53,
        "act": "Act V",
        "title": "Executing 3D Vartana Gradient Shading",
        "base_img": "ep08_gf_21_vartana_3d_gradient_shading_brushwork_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_21_vartana_3d_gradient_shading_brushwork.mp4",
        "duration": "5.0s",
        "spoken_beat": "Notice the realistic three-dimensional shading along his nose and jawline, making his body look soft and alive against the flat stone.",
        "prompt": "Microscopic ancient painting technique. An Indian master artist executing the revolutionary 'vartana' 3D gradient shading technique on Padmapani's face. A soft hair brush gently feathers delicate parallel micro-strokes of warm translucent ochre along the bridge of the nose and the contour of the jawline, creating lifelike cylindrical volume, soft human skin texture, and realistic anatomical depth on the flat stone wall.",
        "camera": "Macro tracking shot following the delicate feathering brush strokes along the nose and jawline."
    },
    {
        "shot_num": 15,
        "cut_num": 54,
        "act": "Act V",
        "title": "Sculpting Raised Pearl Tiara Highlights",
        "base_img": "ep08_gf_22_painting_pearl_tiara_highlights_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_22_painting_pearl_tiara_highlights.mp4",
        "duration": "5.0s",
        "spoken_beat": "A thousand years before Leonardo da Vinci painted in Europe, Indian painters had already mastered human anatomy, emotion, and realistic 3D depth.",
        "prompt": "Extreme macro jewelry painting craftsmanship. The ultra-fine tip of a miniature bamboo brush dabbing tiny, raised droplets of pure white slaked-lime and crushed-shell paste onto the painted royal tiara of Bodhisattva Padmapani. Each opaque white dot instantly forms a glistening, three-dimensional pearl bead catching raking side light, surrounded by intricate gold filigree and glowing blue gemstones. Tactile impasto masterwork.",
        "camera": "Microscopic macro push-in as the brush tip deposits glistening 3D pearl dots onto the royal crown."
    },
    {
        "shot_num": 16,
        "cut_num": 60,
        "act": "Act V",
        "title": "Dropped Brush & Sudden Abandonment",
        "base_img": "ep08_gf_16_abandoned_chisel_dropped_brush_GENERATE_VIDEO.jpg",
        "target_mp4": "ep08_gf_16_abandoned_chisel_dropped_brush.mp4",
        "duration": "5.0s",
        "spoken_beat": "Down the cliff, stonecutters abandoned half-carved pillars, painters dropped their wet brushes on the stone floor, and monks fled into the hills.",
        "prompt": "Poignant historical stillness. Close-up on the stone floor of an unfinished cave. A fine bamboo paintbrush with wet ultramarine blue paint lying dropped across a terracotta pigment bowl, blue paint slowly seeping into the stone dust. Nearby, an iron chisel rests against a half-carved column base. Wind blows dry dust across the floor as footsteps hurry away in the distant corridor. Chilling, realistic historical abandonment.",
        "camera": "Slow low-angle tilt up from the dropped paintbrush on dusty stone floor to silent shadowy corridor."
    }
]

html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Episode 08: Reliving History in the Making — Google Flow Prompt Sheet</title>
<style>
  :root {
    --bg: #0f1117;
    --card: #181c27;
    --border: #2a324b;
    --text: #e2e8f0;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-gold: #f59e0b;
    --accent-emerald: #10b981;
    --tag-bg: #1e293b;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: var(--bg); color: var(--text); padding: 2rem; line-height: 1.6; }
  .container { max-width: 1200px; margin: 0 auto; }
  header { border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 2rem; }
  h1 { font-size: 2rem; color: #fff; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.75rem; }
  .subtitle { color: var(--text-muted); font-size: 1.05rem; }
  .banner { background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(245, 158, 11, 0.1)); border: 1px solid var(--border); border-left: 4px solid var(--accent-gold); padding: 1.25rem; border-radius: 8px; margin-bottom: 2rem; }
  .banner h3 { color: var(--accent-gold); margin-bottom: 0.5rem; font-size: 1.15rem; }
  .banner p { color: #cbd5e1; font-size: 0.95rem; }
  
  .grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; display: grid; grid-template-columns: 320px 1fr; }
  @media (max-width: 860px) { .card { grid-template-columns: 1fr; } }
  .preview-col { background: #000; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 1rem; border-right: 1px solid var(--border); position: relative; }
  .preview-img { width: 100%; border-radius: 6px; aspect-ratio: 16/9; object-fit: cover; border: 1px solid #334155; }
  .img-badge { margin-top: 0.75rem; font-size: 0.75rem; color: var(--accent); font-family: monospace; word-break: break-all; text-align: center; }
  .details-col { padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; }
  .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
  .card-title { font-size: 1.2rem; font-weight: 700; color: #fff; }
  .badge-tag { background: var(--tag-bg); border: 1px solid var(--border); color: var(--accent-gold); font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.6rem; border-radius: 9999px; }
  
  .meta-row { display: flex; gap: 1.5rem; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem; border-bottom: 1px solid #232a3f; padding-bottom: 0.75rem; }
  .meta-item strong { color: #cbd5e1; }
  
  .field-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent); font-weight: 700; margin-bottom: 0.35rem; }
  .spoken-beat { font-style: italic; color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1rem; background: rgba(0,0,0,0.25); padding: 0.6rem 0.85rem; border-radius: 6px; border-left: 3px solid var(--accent); }
  
  .prompt-box { background: #0b0d13; border: 1px solid #28324a; border-radius: 6px; padding: 1rem; position: relative; margin-bottom: 1rem; }
  .prompt-text { font-size: 0.95rem; color: #f1f5f9; line-height: 1.55; padding-right: 100px; }
  .copy-btn { position: absolute; top: 0.6rem; right: 0.6rem; background: #1e293b; color: #38bdf8; border: 1px solid #334155; padding: 0.35rem 0.75rem; font-size: 0.75rem; font-weight: 600; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
  .copy-btn:hover { background: #38bdf8; color: #0f1117; }
  
  .camera-motion { font-size: 0.85rem; color: var(--text-muted); }
  .camera-motion strong { color: #f59e0b; }
  
  /* Feedback Sidebar */
  #feedback-toggle { position: fixed; bottom: 20px; right: 20px; background: var(--accent-gold); color: #000; font-weight: 700; border: none; padding: 12px 20px; border-radius: 50px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 999; }
  #feedback-panel { position: fixed; top: 0; right: -420px; width: 400px; height: 100vh; background: #131722; border-left: 1px solid var(--border); box-shadow: -5px 0 25px rgba(0,0,0,0.7); padding: 20px; transition: right 0.3s ease; z-index: 1000; display: flex; flex-direction: column; }
  #feedback-panel.open { right: 0; }
  .fb-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 15px; }
  .fb-header h3 { color: #fff; font-size: 1.1rem; }
  .fb-close { background: none; border: none; color: #94a3b8; font-size: 1.5rem; cursor: pointer; }
  .fb-list { flex: 1; overflow-y: auto; margin-bottom: 15px; display: flex; flex-direction: column; gap: 10px; }
  .fb-item { background: #1c2233; padding: 10px; border-radius: 6px; border-left: 3px solid var(--accent); font-size: 0.85rem; position: relative; }
  .fb-item .fb-tag { display: inline-block; font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 3px; margin-bottom: 4px; text-transform: uppercase; }
  .fb-item.tag-change .fb-tag { background: #f59e0b; color: #000; }
  .fb-item.tag-approval .fb-tag { background: #10b981; color: #000; }
  .fb-item.tag-issue .fb-tag { background: #ef4444; color: #fff; }
  .fb-item.tag-idea .fb-tag { background: #38bdf8; color: #000; }
  .fb-item .fb-del { position: absolute; top: 8px; right: 8px; background: none; border: none; color: #64748b; cursor: pointer; }
  .fb-item .fb-del:hover { color: #ef4444; }
  .fb-form { display: flex; flex-direction: column; gap: 8px; }
  .fb-form select, .fb-form textarea, .fb-form input { background: #1c2233; border: 1px solid var(--border); color: #fff; padding: 8px; border-radius: 4px; font-size: 0.85rem; }
  .fb-form button { background: var(--accent); color: #000; font-weight: 700; border: none; padding: 10px; border-radius: 4px; cursor: pointer; }
  .fb-actions { display: flex; gap: 8px; margin-top: 10px; }
  .fb-btn-sec { flex: 1; background: #2a324b; color: #cbd5e1; border: none; padding: 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; cursor: pointer; text-align: center; }
  .fb-btn-sec:hover { background: #38bdf8; color: #000; }
</style>
</head>
<body>

<div class="container">
  <header>
    <h1>🎬 Episode 08: Google Flow Action Prompts</h1>
    <div class="subtitle">16 Action-Shot Google Flow / Veo Motion Prompts — 5th-Century Historical Realism (No Fantasy Movie CGI)</div>
  </header>

  <div class="banner">
    <h3>🎬 Director's Production Directive: Reliving the Era Through Their Eyes</h3>
    <p>Every single video clip in this episode must put the audience directly inside the 5th-century mountain workshop. Viewers must feel the grit of the clay underfoot, hear the acoustic clinking of bronze and iron against volcanic basalt, watch the blinding sun beam reflected through cave darkness, and see the squirrel-hair brush lay down wet lapis lazuli on ivory plaster. <strong>Strictly zero magical glowing or fantasy tropes: 100% authentic human craftsmanship.</strong></p>
  </div>

  <div class="grid">
''')

for shot in ACTION_SHOTS:
    html_parts.append(f'''
    <!-- SHOT {shot['shot_num']:02d} -->
    <div class="card" id="cut_{shot['cut_num']:02d}">
      <div class="preview-col">
        <img class="preview-img" src="../google_flow_input_images/{shot['base_img']}" alt="{shot['base_img']}">
        <div class="img-badge">{shot['base_img']}</div>
      </div>
      <div class="details-col">
        <div>
          <div class="card-header">
            <div class="card-title">Shot {shot['shot_num']:02d}: {shot['title']}</div>
            <span class="badge-tag">Cut #{shot['cut_num']} ({shot['act']})</span>
          </div>
          <div class="meta-row">
            <div class="meta-item"><strong>Target Output:</strong> <code>{shot['target_mp4']}</code></div>
            <div class="meta-item"><strong>Duration:</strong> {shot['duration']}</div>
          </div>
          <div class="field-label">Spoken Beat</div>
          <div class="spoken-beat">"{shot['spoken_beat']}"</div>
          <div class="field-label">Google Flow / Veo Motion Prompt</div>
          <div class="prompt-box">
            <div class="prompt-text">{shot['prompt']}</div>
            <button class="copy-btn" onclick="copyPrompt(this)">Copy Prompt</button>
          </div>
        </div>
        <div class="camera-motion"><strong>Camera Motion:</strong> {shot['camera']}</div>
      </div>
    </div>
''')

html_parts.append('''
  </div>
</div>

<!-- Interactive Feedback System -->
<button id="feedback-toggle" onclick="toggleFeedback()">💬 Feedback (<span id="fb-count">0</span>)</button>

<div id="feedback-panel">
  <div class="fb-header">
    <h3>Feedback & Changes</h3>
    <button class="fb-close" onclick="toggleFeedback()">&times;</button>
  </div>
  <div class="fb-list" id="fb-items"></div>
  <div class="fb-form">
    <select id="fb-tag">
      <option value="tag-change">✏️ Change Request</option>
      <option value="tag-approval">✅ Approval</option>
      <option value="tag-issue">⚠️ Issue / Bug</option>
      <option value="tag-idea">💡 Idea / Note</option>
    </select>
    <input type="text" id="fb-cut" placeholder="Cut # or Clip Name (optional)">
    <textarea id="fb-text" rows="3" placeholder="Type your feedback here..."></textarea>
    <button onclick="addFeedback()">Add Feedback</button>
  </div>
  <div class="fb-actions">
    <button class="fb-btn-sec" onclick="copyFeedbackForAgent()">📋 Copy for Agent</button>
    <button class="fb-btn-sec" onclick="exportFeedbackJSON()">💾 Export JSON</button>
    <button class="fb-btn-sec" onclick="clearFeedback()">🗑️ Clear</button>
  </div>
</div>

<script>
function copyPrompt(btn) {
  const text = btn.previousElementSibling.innerText;
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.innerText;
    btn.innerText = "✓ Copied!";
    btn.style.background = "#10b981";
    btn.style.color = "#000";
    setTimeout(() => {
      btn.innerText = orig;
      btn.style.background = "#1e293b";
      btn.style.color = "#38bdf8";
    }, 2000);
  });
}

const STORAGE_KEY = "ep08_google_flow_prompts_feedback";
let feedbackList = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");

function toggleFeedback() {
  document.getElementById("feedback-panel").classList.toggle("open");
}

function renderFeedback() {
  const container = document.getElementById("fb-items");
  document.getElementById("fb-count").innerText = feedbackList.length;
  container.innerHTML = "";
  feedbackList.forEach((item, idx) => {
    const div = document.createElement("div");
    div.className = `fb-item ${item.tag}`;
    div.innerHTML = `
      <span class="fb-tag">${item.tag.replace("tag-", "")}</span>
      ${item.cut ? `<strong>[${item.cut}]</strong> ` : ""}
      <div>${item.text}</div>
      <button class="fb-del" onclick="deleteFeedback(${idx})">&times;</button>
    `;
    container.appendChild(div);
  });
}

function addFeedback() {
  const tag = document.getElementById("fb-tag").value;
  const cut = document.getElementById("fb-cut").value.trim();
  const text = document.getElementById("fb-text").value.trim();
  if (!text) return;
  feedbackList.push({ tag, cut, text, time: new Date().toISOString() });
  localStorage.setItem(STORAGE_KEY, JSON.stringify(feedbackList));
  document.getElementById("fb-text").value = "";
  renderFeedback();
}

function deleteFeedback(idx) {
  feedbackList.splice(idx, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(feedbackList));
  renderFeedback();
}

function clearFeedback() {
  if (confirm("Clear all feedback notes?")) {
    feedbackList = [];
    localStorage.removeItem(STORAGE_KEY);
    renderFeedback();
  }
}

function copyFeedbackForAgent() {
  if (feedbackList.length === 0) {
    alert("No feedback items to copy!");
    return;
  }
  let md = "### Episode 08 Google Flow Prompt Sheet Feedback:\\n";
  feedbackList.forEach(item => {
    md += `- **[${item.tag.replace("tag-", "").toUpperCase()}]** ${item.cut ? `(${item.cut}) ` : ""}${item.text}\\n`;
  });
  navigator.clipboard.writeText(md).then(() => {
    alert("Copied feedback to clipboard! You can paste it directly to the agent.");
  });
}

function exportFeedbackJSON() {
  const blob = new Blob([JSON.stringify(feedbackList, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "ep08_google_flow_feedback.json";
  a.click();
}

renderFeedback();
</script>

</body>
</html>
''')

output_path = Path("ajanta-ellora/episode08/GOOGLE_FLOW_PROMPT_SHEET.html")
output_path.write_text("".join(html_parts), encoding="utf-8")
print(f"[OK] Successfully regenerated {output_path} with all 16 synchronized action shots!")
