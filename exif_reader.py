# --- START OF FILE exif_reader.py ---

import os
import json
import torch
import numpy as np
from PIL import Image, ExifTags
from folder_paths import get_input_directory
import traceback

class ReadExifData:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = get_input_directory()
        supported_formats = ['.jpg', '.jpeg', '.tiff', '.tif', '.webp']
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and os.path.splitext(f)[1].lower() in supported_formats]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True})
            }
        }

    # --- CHANGE 1: Added Artist and Copyright to outputs ---
    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image_out", "exif_summary", "exif_raw_json", "camera_model", "lens_model", "f_number", "exposure_time", "iso", "focal_length", "date_time", "artist", "copyright")
    FUNCTION = "read_exif"
    CATEGORY = "Data pro"

    def read_exif(self, image):
        image_path = os.path.join(get_input_directory(), image)
        
        empty_tensor = torch.zeros((1, 64, 64, 3))
        empty_results = (empty_tensor, "File not found.",) + ("",) * 10

        if not os.path.exists(image_path):
            return empty_results

        try:
            img = Image.open(image_path)
            img_rgb = img.convert("RGB")
            tensor = torch.from_numpy(np.array(img_rgb).astype(np.float32) / 255.0).unsqueeze(0)

            # --- CHANGE 2: Read multiple metadata types (EXIF and XMP) and merge them ---
            full_metadata = {}
            
            # 1. Read standard EXIF data
            raw_exif = img.getexif()
            if raw_exif:
                for tag_id, value in raw_exif.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    if isinstance(value, bytes):
                        try: value = value.decode('utf-8', errors='ignore').strip('\x00')
                        except: pass
                    full_metadata[tag_name] = value
            
            # 2. Read XMP data (from Adobe software etc.)
            if hasattr(img, 'getxmp'):
                try:
                    xmp_data = img.getxmp()
                    if xmp_data and 'xmpmeta' in xmp_data:
                        # XMP data is complex XML, we look for common creator/copyright tags
                        xmp_str = xmp_data['xmpmeta'].decode('utf-8', errors='ignore')
                        creator_match = re.search(r'<dc:creator>\s*<rdf:Seq>\s*<rdf:li>(.*?)</rdf:li>\s*</rdf:Seq>\s*</dc:creator>', xmp_str)
                        if creator_match: full_metadata['Artist'] = creator_match.group(1).strip()
                        
                        copyright_match = re.search(r'<dc:rights>\s*<rdf:Alt>\s*<rdf:li.*?>(.*?)</rdf:li>\s*</rdf:Alt>\s*</dc:rights>', xmp_str)
                        if copyright_match: full_metadata['Copyright'] = copyright_match.group(1).strip()
                except Exception as xmp_e:
                    print(f"Could not parse XMP data: {xmp_e}")


            if not full_metadata:
                return (tensor, "No EXIF or XMP data found.",) + ("",) * 10

            # --- CHANGE 3: Extract from the combined metadata dictionary ---
            camera_model = str(full_metadata.get('Model', 'N/A')).strip()
            lens_model = str(full_metadata.get('LensModel', 'N/A')).strip()
            f_number = str(full_metadata.get('FNumber', 'N/A'))
            exposure_time_raw = full_metadata.get('ExposureTime', 'N/A')
            iso = str(full_metadata.get('ISOSpeedRatings', 'N/A'))
            focal_length = str(full_metadata.get('FocalLength', 'N/A'))
            date_time = str(full_metadata.get('DateTimeOriginal', full_metadata.get('DateTime', 'N/A'))).strip()
            artist = str(full_metadata.get('Artist', 'N/A')).strip()
            copyright_notice = str(full_metadata.get('Copyright', 'N/A')).strip()

            exposure_time_str = str(exposure_time_raw)
            try:
                if isinstance(exposure_time_raw, (float, int)) and 0 < exposure_time_raw < 1:
                    exposure_time_str = f"1/{int(1/exposure_time_raw)}s"
                elif isinstance(exposure_time_raw, (float, int)):
                     exposure_time_str = f"{exposure_time_raw}s"
            except: pass

            summary_parts = [
                f"Camera: {camera_model}", f"Lens: {lens_model}", f"Artist: {artist}", f"Copyright: {copyright_notice}",
                f"Date/Time: {date_time}", "--- Settings ---", f"Aperture: f/{f_number}",
                f"Shutter Speed: {exposure_time_str}", f"ISO: {iso}", f"Focal Length: {focal_length}mm"
            ]
            summary = "\n".join(part for part in summary_parts if 'N/A' not in part or '---' in part)

            serializable_exif = {k: str(v) for k, v in full_metadata.items()}
            raw_json = json.dumps(serializable_exif, indent=2)

            return (tensor, summary, raw_json, camera_model, lens_model, f_number, exposure_time_str, iso, focal_length, date_time, artist, copyright_notice)

        except Exception as e:
            error_details = traceback.format_exc()
            print(f"[ERROR] ReadExifData failed:\n{error_details}")
            return (empty_tensor, f"Failed to read EXIF data: {e}",) + ("",) * 10

# --- Node Mappings ---
NODE_CLASS_MAPPINGS = { "ReadExifData": ReadExifData }
NODE_DISPLAY_NAME_MAPPINGS = { "ReadExifData": "Read EXIF Data" }