#!/usr/bin/env python3
"""
organize_ep07_videos.py
Maps downloaded Google Flow video files into canonical filenames inside ajanta-ellora/episode07/videos/
"""

import shutil
from pathlib import Path

VIDEOS_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat/ajanta-ellora/episode07/videos")

MAPPINGS = [
    # Batch 1 (download)
    ("download/Drone_descending_over_river_gorge_20261013105912.mp4", "ep07_gf_01_fpv_canyon_reveal.mp4"),
    ("download/Buddhist_monks_walking_cliff_trail_20261013105912.mp4", "ep07_gf_02_satavahana_monks_cliff_path.mp4"),
    ("download/Stonemasons_carving_rock_cave_20261013105912.mp4", "ep07_gf_03_topdown_roofline_excavation.mp4"),
    ("download/Tilt_along_rock_ceiling_20261013105912.mp4", "ep07_gf_04_vaulted_chaitya_ribbing_macro.mp4"),
    ("download/Monsoon_rainwater_flowing_over_p*_20261013105912.mp4", "ep07_gf_05_monsoon_plateau_gutter_sheet.mp4"),
    ("download/Water_dripping_in_subterranean_c*_20261013105912.mp4", "ep07_gf_06_podhi_cistern_water_filtration.mp4"),
    ("download/Monk_chanting_in_stone_cave_20261013105912.mp4", "ep07_gf_07_monk_chanting_acoustic_resonance.mp4"),
    ("download/Jungle_vines_swallowing_cave_ent*_20261013105912.mp4", "ep07_gf_08_jungle_overgrowth_dormancy.mp4"),
    
    # Batch 2 (download (1))
    ("download (1)/Caravan_crossing_rocky_mountain_*_20261013111429.mp4", "ep07_gf_09_dakshinapatha_caravan_crossing.mp4"),
    ("download (1)/Quarryman_splitting_basalt_rock_*_20261013111429.mp4", "ep07_gf_10_columnar_basalt_quarry_split.mp4"),
    ("download (1)/Chisel_carving_basalt_ceiling_20261013111429.mp4", "ep07_gf_12_carpentry_peg_socket_carving.mp4"),
    ("download (1)/Waterfall_plunging_into_canyon_r*_20261013111429.mp4", "ep07_gf_13_monsoon_waterfall_clearing_portal.mp4"),
    ("download (1)/Monk_carrying_lamp_down_steps_20261013111429.mp4", "ep07_gf_14_torchlit_podhi_descent.mp4"),
    ("download (1)/Monks_circumambulating_rock_stupa_20261013111429.mp4", "ep07_gf_15_stupa_pradakshina_ritual.mp4"),
    ("download (1)/FPV_drone_flying_over_river_20261013111429.mp4", "ep07_gf_16_flash_flood_canyon_river_rush.mp4"),
]

def organize():
    print("=" * 60)
    print("  Organizing Episode 07 Google Flow Action Videos")
    print("=" * 60)
    
    found_count = 0
    for pattern, target_name in MAPPINGS:
        target_path = VIDEOS_DIR / target_name
        parent_dir, file_pattern = pattern.split("/", 1)
        search_dir = VIDEOS_DIR / parent_dir
        
        matches = list(search_dir.glob(file_pattern))
        if matches:
            src = matches[0]
            shutil.copy2(src, target_path)
            size_mb = target_path.stat().st_size / (1024 * 1024)
            print(f"[OK] {target_name} ({size_mb:.2f} MB) <- {src.name}")
            found_count += 1
        else:
            print(f"[MISSING] Pattern not found: {pattern}")
            
    print("=" * 60)
    print(f"Mapped and copied: {found_count}/{len(MAPPINGS)} video files into {VIDEOS_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    organize()
