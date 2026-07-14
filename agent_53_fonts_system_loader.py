import os
import sys
import json
import platform

class FontsSystemLoader:
    def __init__(self, workspace_dir="znet_workspace"):
        self.agent_name = "Agent 53: fonts_system_loader"
        self.workspace_dir = workspace_dir
        self.output_fonts_manifest = os.path.join(self.workspace_dir, "53_fonts_system_manifest.json")

        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _get_os_font_directories(self):
        # Alag-alag Operating Systems ke default font directories identify karta hai
        current_os = platform.system().lower()
        directories = []

        if current_os == "windows":
            # Windows standard path
            windir = os.environ.get("WINDIR", "C:\\Windows")
            directories.append(os.path.join(windir, "Fonts"))
            # User specific local fonts path (Windows 10/11)
            local_app_data = os.environ.get("LOCALAPPDATA", "")
            if local_app_data:
                directories.append(os.path.join(local_app_data, "Microsoft\\Windows\\Fonts"))

        elif current_os == "darwin":
            # macOS standard paths
            directories.extend([
                "/Library/Fonts",
                "/System/Library/Fonts",
                os.path.expanduser("~/Library/Fonts")
            ])

        else:
            # Linux standard paths
            directories.extend([
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                os.path.expanduser("~/.local/share/fonts"),
                os.path.expanduser("~/.fonts")
            ])

        return directories

    def scan_and_load_fonts(self):
        print(f"[{self.agent_name}] Initializing system fonts loader & scanner...")
        font_dirs = self._get_os_font_directories()
        
        registered_fonts = {}
        high_ctr_keywords = ["impact", "arial", "bold", "black", "montserrat", "bebas", "gotham"]

        print(f"[{self.agent_name}] Scanning system paths: {font_dirs}")

        # Walking through directories to find TTF and OTF fonts
        font_count = 0
        for directory in font_dirs:
            if not os.path.exists(directory):
                continue
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in [".ttf", ".otf"]:
                        font_name = os.path.splitext(file)[0]
                        font_path = os.path.join(root, file)
                        
                        # Normalize name for easy matching
                        normalized_name = font_name.lower().replace(" ", "_")
                        
                        # Category Tagging: Check if this font is ideal for High-CTR Anime thumbnails
                        is_high_ctr = any(keyword in normalized_name for keyword in high_ctr_keywords)
                        
                        registered_fonts[font_name] = {
                            "font_family": font_name,
                            "file_name": file,
                            "absolute_path": font_path,
                            "extension": ext,
                            "is_high_ctr_recommended": is_high_ctr
                        }
                        font_count += 1

        # Fallback layer: Agar system me security restrictions ki wajah se fonts na milein (or dry-run test)
        if font_count == 0:
            print(f"[{self.agent_name}] No system fonts scanned. Creating standard web-safe fallback registry.")
            fallback_fonts = ["Arial", "Impact", "Helvetica", "TrebuchetMS"]
            for f in fallback_fonts:
                registered_fonts[f] = {
                    "font_family": f,
                    "file_name": f"{f}.ttf",
                    "absolute_path": f"system_fallback_path/{f}.ttf",
                    "extension": ".ttf",
                    "is_high_ctr_recommended": True if f in ["Impact", "Arial"] else False
                }
            font_count = len(fallback_fonts)

        # Output payload compilation
        manifest_payload = {
            "agent_executed": self.agent_name,
            "detected_os": platform.system(),
            "scanned_directories": font_dirs,
            "total_fonts_registered": font_count,
            "fonts_database": registered_fonts
        }

        self._save_manifest(manifest_payload)
        return manifest_payload

    def _save_manifest(self, data):
        try:
            with open(self.output_fonts_manifest, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[{self.agent_name}] Fonts system loader manifest saved to '{self.output_fonts_manifest}'")
        except Exception as e:
            print(f"[{self.agent_name}] Error writing fonts database manifest: {str(e)}")

if __name__ == "__main__":
    loader = FontsSystemLoader()
    result = loader.scan_and_load_fonts()
    
    print("\n--- Z-NET FONTS SYSTEM LOADER: AGENT 53 COMPLETE ---")
    print(f"Operating System: {result['detected_os']}")
    print(f"Total Fonts Scanned & Registered: {result['total_fonts_registered']}")
    
    # Recommended high CTR fonts display filter
    high_ctr_list = [meta["font_family"] for name, meta in result["fonts_database"].items() if meta["is_high_ctr_recommended"]]
    print(f"High-CTR Recommended Fonts Found: {len(high_ctr_list)}")
    if high_ctr_list:
        print(f"  Top Picks: {', '.join(high_ctr_list[:8])}...")
    print("---------------------------------------------------------")
