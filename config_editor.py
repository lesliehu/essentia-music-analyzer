#!/usr/bin/env python3
"""
Konfiguráció szerkesztő az Essentia Music Analyzer számára
"""
import json
import os
import sys

class ConfigEditor:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Konfiguráció betöltése"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Konfiguráció nem található: {self.config_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON hiba: {e}")
            return None
    
    def save_config(self):
        """Konfiguráció mentése"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"✅ Konfiguráció mentve: {self.config_path}")
            return True
        except Exception as e:
            print(f"❌ Mentési hiba: {e}")
            return False
    
    def show_current_config(self):
        """Jelenlegi konfiguráció megjelenítése"""
        if not self.config:
            return
        
        print("\n🔧 JELENLEGI KONFIGURÁCIÓ")
        print("=" * 50)
        
        # Aktív modell
        active = self.config["model_settings"]["active_model"]
        models = self.config["model_settings"]["models"]
        
        if active in models:
            model_info = models[active]
            print(f"🤖 Aktív modell: {active}")
            print(f"   Név: {model_info['name']}")
            print(f"   Műfajok: {model_info['genre_count']}")
            print(f"   Sebesség: {model_info['performance']}")
            print(f"   Pontosság: {model_info['accuracy']}")
        
        # Feldolgozási beállítások
        proc = self.config["processing_settings"]
        print(f"\n⚙️ Feldolgozás:")
        print(f"   BPM elemzés: {'✅' if proc['enable_bpm_analysis'] else '❌'}")
        print(f"   Top műfajok: {proc['top_genres_count']}")
        print(f"   Min. konfidencia: {proc['confidence_threshold']:.2f}")
        
        # Kimeneti beállítások
        out = self.config["output_settings"]
        print(f"\n💾 Kimenet:")
        print(f"   Fájl előtag: {out['filename_prefix']}")
        print(f"   Kódolás: {out['csv_encoding']}")
    
    def show_available_models(self):
        """Elérhető modellek listája"""
        if not self.config:
            return
        
        print("\n🎭 ELÉRHETŐ MODELLEK")
        print("=" * 50)
        
        models = self.config["model_settings"]["models"]
        active = self.config["model_settings"]["active_model"]
        
        for i, (key, model) in enumerate(models.items(), 1):
            status = "🟢 AKTÍV" if key == active else f"⚪ [{i}]"
            print(f"\n{status} {key.upper()}")
            print(f"  📛 {model['name']}")
            print(f"  📝 {model['description']}")
            print(f"  🎯 {model['genre_count']} műfaj")
            print(f"  ⚡ {model['performance']} sebesség")
            print(f"  🎯 {model['accuracy']} pontosság")
            
            # Fájl ellenőrzés
            if os.path.exists(model['model_file']):
                size = os.path.getsize(model['model_file']) / (1024*1024)
                print(f"  💾 {model['model_file']} ({size:.1f} MB) ✅")
            else:
                print(f"  💾 {model['model_file']} ❌")
    
    def change_active_model(self):
        """Aktív modell változtatása"""
        if not self.config:
            return False
        
        self.show_available_models()
        
        models = list(self.config["model_settings"]["models"].keys())
        print(f"\n🔄 Modell választás:")
        
        for i, model in enumerate(models, 1):
            print(f"  {i}. {model}")
        
        try:
            choice = input(f"\nVálassz modellt (1-{len(models)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(models):
                new_model = models[choice_idx]
                old_model = self.config["model_settings"]["active_model"]
                
                self.config["model_settings"]["active_model"] = new_model
                
                print(f"\n🔄 Modell váltás:")
                print(f"   Régi: {old_model}")
                print(f"   Új: {new_model}")
                
                return self.save_config()
            else:
                print("❌ Érvénytelen választás!")
                return False
                
        except (ValueError, KeyboardInterrupt):
            print("❌ Megszakítva")
            return False
    
    def edit_processing_settings(self):
        """Feldolgozási beállítások szerkesztése"""
        if not self.config:
            return False
        
        proc = self.config["processing_settings"]
        
        print("\n⚙️ FELDOLGOZÁSI BEÁLLÍTÁSOK")
        print("=" * 40)
        
        settings = [
            ("enable_bpm_analysis", "BPM elemzés", "bool"),
            ("top_genres_count", "Top műfajok száma", "int"),
            ("confidence_threshold", "Min. konfidencia (0.0-1.0)", "float"),
            ("verbose_output", "Részletes kimenet", "bool")
        ]
        
        for key, description, value_type in settings:
            current = proc.get(key, "N/A")
            print(f"\n🔧 {description}")
            print(f"   Jelenlegi: {current}")
            
            try:
                if value_type == "bool":
                    new_val = input("   Új érték (true/false): ").strip().lower()
                    if new_val in ['true', 't', '1', 'yes', 'y']:
                        proc[key] = True
                    elif new_val in ['false', 'f', '0', 'no', 'n']:
                        proc[key] = False
                    elif new_val == "":
                        continue  # Megtartja a régit
                    else:
                        print("   ❌ Érvénytelen bool érték")
                        continue
                
                elif value_type == "int":
                    new_val = input("   Új érték: ").strip()
                    if new_val:
                        proc[key] = int(new_val)
                
                elif value_type == "float":
                    new_val = input("   Új érték: ").strip()
                    if new_val:
                        val = float(new_val)
                        if 0.0 <= val <= 1.0:
                            proc[key] = val
                        else:
                            print("   ❌ Érték 0.0-1.0 között kell legyen")
                
            except (ValueError, KeyboardInterrupt):
                print("   ❌ Érvénytelen érték vagy megszakítva")
                continue
        
        return self.save_config()
    
    def interactive_menu(self):
        """Interaktív menü"""
        if not self.config:
            print("❌ Nem lehet szerkeszteni - konfiguráció hiányzik!")
            return
        
        while True:
            print("\n🎛️  ESSENTIA KONFIGURÁCIÓ SZERKESZTŐ")
            print("=" * 50)
            print("1. 📋 Jelenlegi konfiguráció megjelenítése")
            print("2. 🎭 Elérhető modellek listája")
            print("3. 🔄 Aktív modell változtatása")
            print("4. ⚙️  Feldolgozási beállítások")
            print("5. 💾 Konfiguráció mentése és kilépés")
            print("6. 🚪 Kilépés mentés nélkül")
            
            try:
                choice = input("\nVálasztás (1-6): ").strip()
                
                if choice == "1":
                    self.show_current_config()
                elif choice == "2":
                    self.show_available_models()
                elif choice == "3":
                    self.change_active_model()
                elif choice == "4":
                    self.edit_processing_settings()
                elif choice == "5":
                    if self.save_config():
                        print("👋 Konfiguráció mentve, kilépés...")
                        break
                elif choice == "6":
                    print("👋 Kilépés mentés nélkül...")
                    break
                else:
                    print("❌ Érvénytelen választás!")
                    
            except KeyboardInterrupt:
                print("\n👋 Kilépés...")
                break


def main():
    """Főprogram"""
    print("🎛️  ESSENTIA CONFIG EDITOR")
    print("=" * 40)
    
    # Argumentum parsing javítva
    config_path = "config.json"  # Alapértelmezett
    command_start = 1  # Hol kezdődnek a parancsok
    
    # Ha az első argumentum .json-ra végződik, az config fájl
    if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
        config_path = sys.argv[1]
        command_start = 2
    
    # Config fájl ellenőrzése
    if not os.path.exists(config_path):
        print(f"❌ Konfiguráció nem található: {config_path}")
        print("💡 Futtasd először a konfigurálható verziót a config létrehozásához!")
        return 1
    
    editor = ConfigEditor(config_path)
    
    # Parancs feldolgozás az új logikával
    if len(sys.argv) > command_start:
        # Van parancs
        command = sys.argv[command_start]
        
        if command == "show":
            editor.show_current_config()
        elif command == "models":
            editor.show_available_models()
        elif command == "set-model":
            if len(sys.argv) > command_start + 1:
                model_name = sys.argv[command_start + 1]
                if editor.config and model_name in editor.config["model_settings"]["models"]:
                    old_model = editor.config["model_settings"]["active_model"]
                    editor.config["model_settings"]["active_model"] = model_name
                    if editor.save_config():
                        print(f"✅ Modell váltás: {old_model} → {model_name}")
                    else:
                        print(f"❌ Mentési hiba!")
                else:
                    if not editor.config:
                        print("❌ Konfiguráció nem betöltött!")
                    else:
                        print(f"❌ Ismeretlen modell: {model_name}")
                        available = list(editor.config["model_settings"]["models"].keys())
                        print(f"Elérhető: {', '.join(available)}")
            else:
                print("❌ Hiányzó modell név!")
                print("Használat: python3 config_editor.py set-model <model_name>")
        else:
            print(f"❌ Ismeretlen parancs: {command}")
            print("Használat:")
            print(f"  {sys.argv[0]} [config.json] show")
            print(f"  {sys.argv[0]} [config.json] models") 
            print(f"  {sys.argv[0]} [config.json] set-model <model_name>")
    else:
        # Interaktív mód
        editor.interactive_menu()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())