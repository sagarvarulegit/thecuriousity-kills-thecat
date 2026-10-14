"""
sync_generated_brain_images.py — Syncs images generated in the brain directory into ajanta-ellora/episode06/images/
"""

import shutil
import re
from pathlib import Path

BRAIN_DIR = Path("C:/Users/sunwa/.gemini/antigravity-cli/brain/f8a607f6-1331-42a8-87f5-e594d6e7fbe3")
IMAGES_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat/ajanta-ellora/episode06/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Map prefix or keyword to target filename
TARGET_MAP = {
    "ep06_11_shikhara": "ep06_11_shikhara_finial_kalasha_PAN_ZOOM.jpg",
    "ep06_12_top_down": "ep06_12_top_down_stepped_terraces_PAN_ZOOM.jpg",
    "ep06_13_rope_rigging": "ep06_13_rope_rigging_anchor_points_PAN_ZOOM.jpg",
    "ep06_14_inverted_quarry": "ep06_14_inverted_quarry_technique_PAN_ZOOM.jpg",
    "ep06_15_acoustic_sounding": "ep06_15_acoustic_sounding_chisel_tap_PAN_ZOOM.jpg",
    "ep06_16_tempered_chisel": "ep06_16_tempered_chisel_arsenal_PAN_ZOOM.jpg",
    "ep06_17_void_clearance": "ep06_17_void_clearance_moment_hero_PAN_ZOOM.jpg",
    "ep06_18_twin_dhwajasthambha": "ep06_18_twin_dhwajasthambha_symmetry_PAN_ZOOM.jpg",
    "ep06_19_dhwajasthambha": "ep06_19_dhwajasthambha_trident_capital_PAN_ZOOM.jpg",
    "ep06_20_freestanding_elephant": "ep06_20_freestanding_elephant_flank_PAN_ZOOM.jpg",
    "ep06_21_elephant_ear": "ep06_21_elephant_ear_rock_texture_PAN_ZOOM.jpg",
    "ep06_22_3d_spatial": "ep06_22_3d_spatial_visualization_still_PAN_ZOOM.jpg",
    "ep06_23_ramayana": "ep06_23_ramayana_running_frieze_overview_PAN_ZOOM.jpg",
    "ep06_24_battle_of_lanka": "ep06_24_battle_of_lanka_warriors_PAN_ZOOM.jpg",
    "ep06_25_ravana_anugraha": "ep06_25_ravana_anugraha_wide_recess_PAN_ZOOM.jpg",
    "ep06_26_shiva_calm": "ep06_26_shiva_calm_foot_press_PAN_ZOOM.jpg",
    "ep06_27_chiaroscuro": "ep06_27_chiaroscuro_relief_depth_PAN_ZOOM.jpg",
    "ep06_28_ancient_white": "ep06_28_ancient_white_plaster_reconstruction_PAN_ZOOM.jpg",
    "ep06_29_calcined_river": "ep06_29_calcined_river_shells_chuna_PAN_ZOOM.jpg",
    "ep06_30_agate_burnishing": "ep06_30_agate_burnishing_stone_macro_PAN_ZOOM.jpg",
    "ep06_31_surviving_plaster": "ep06_31_surviving_plaster_remnants_cornice_PAN_ZOOM.jpg",
    "ep06_32_iceberg": "ep06_32_iceberg_in_black_chasm_hero_PAN_ZOOM.jpg",
    "ep06_33_1682_aurangzeb": "ep06_33_1682_aurangzeb_royal_camp_PAN_ZOOM.jpg",
    "ep06_34_demolition": "ep06_34_demolition_taskforce_tools_PAN_ZOOM.jpg",
    "ep06_35_failed_demolition": "ep06_35_failed_demolition_scars_basalt_PAN_ZOOM.jpg",
    "ep06_36_baroda_copper": "ep06_36_baroda_copper_plate_charter_PAN_ZOOM.jpg",
    "ep06_37_celestial_gods": "ep06_37_celestial_gods_view_downward_PAN_ZOOM.jpg",
    "ep06_38_architect": "ep06_38_architect_katham_akrita_hero_PAN_ZOOM.jpg",
    "ep06_archive_01_ellora": "ep06_archive_01_ellora_ridge_topography_PAN_ZOOM.jpg",
    "ep06_archive_02_kailasa": "ep06_archive_02_kailasa_ground_plan_schematic_PAN_ZOOM.jpg",
    "ep06_archive_03_top_down": "ep06_archive_03_top_down_cross_section_elevation_PAN_ZOOM.jpg",
    "ep06_archive_04_ancient_vasthu": "ep06_archive_04_ancient_vasthu_shastra_compass_PAN_ZOOM.jpg",
    "ep06_archive_05_baroda": "ep06_archive_05_baroda_plates_garuda_seal_PAN_ZOOM.jpg",
    "ep06_archive_06_james": "ep06_archive_06_james_burgess_1883_report_plate_PAN_ZOOM.jpg",
    "ep06_archive_07_rashtrakuta": "ep06_archive_07_rashtrakuta_iron_mine_smelting_PAN_ZOOM.jpg",
    "ep06_archive_08_plaster": "ep06_archive_08_plaster_microscopic_cross_section_PAN_ZOOM.jpg",
    "ep06_archive_09_19th": "ep06_archive_09_19th_century_collo_type_kailasa_bridge_PAN_ZOOM.jpg",
    "ep06_archive_10_aurangzeb": "ep06_archive_10_aurangzeb_court_chronicle_manuscript_PAN_ZOOM.jpg",
    "ep06_archive_11_stone_mason": "ep06_archive_11_stone_mason_guild_emblems_PAN_ZOOM.jpg",
    "ep06_archive_12_kailasa": "ep06_archive_12_kailasa_vimana_starry_night_PAN_ZOOM.jpg",
    "ep06_infographic_02": "ep06_infographic_02_kokasa_top_down_timeline.jpg",
    "ep06_infographic_04": "ep06_infographic_04_dhwajasthambha_quarry_isolation.jpg",
    "ep06_infographic_05": "ep06_infographic_05_white_chuna_plaster_stratigraphy.jpg",
    "ep06_infographic_06": "ep06_infographic_06_aurangzeb_demolition_structural_comparison.jpg",
}

def sync():
    brain_files = list(BRAIN_DIR.glob("*.jpg"))
    copied = 0
    for f in brain_files:
        name_lower = f.name.lower()
        for key, target_name in TARGET_MAP.items():
            if key in name_lower:
                dest = IMAGES_DIR / target_name
                # Overwrite if dest does not exist or if dest is a smaller PIL card (< 500KB)
                if not dest.exists() or dest.stat().st_size < 500000 or f.stat().st_size > dest.stat().st_size:
                    shutil.copy2(f, dest)
                    print(f"  [COPIED] {f.name} -> {target_name} ({f.stat().st_size} bytes)")
                    copied += 1
                break
    print(f"Sync complete. Newly copied: {copied}. Total in images/: {len(list(IMAGES_DIR.glob('*.jpg')))}")

if __name__ == "__main__":
    sync()
