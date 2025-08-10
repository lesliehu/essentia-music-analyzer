#!/usr/bin/env python3
"""
Telepítés ellenőrző script az Essentia Music Analyzer számára
"""
import sys
import os
import subprocess

def check_python_version():
    """Python verzió ellenőrzés"""
    version = sys.version_info
    print(f"🐍 Python verzió: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 8:
        print("❌ Python 3.8+ szükséges!")
        return False
    else:
        print("✅ Python verzió megfelelő")
        return True

def check_imports():
    """Függőségek ellenőrzése"""
    imports_to_check = {
        'essentia': 'essentia-tensorflow',
        'numpy': 'numpy', 
        'pandas': 'pandas',
        'tensorflow': 'tensorflow (essentia-tensorflow részében)'
    }
    
    print("\n📦 Függőségek ellenőrzése:")
    all_good = True
    
    for module, package in imports_to_check.items():
        try:
            if module == 'essentia':
                import essentia
                print(f"✅ {module}: {essentia.__version__}")
            elif module == 'tensorflow':
                import tensorflow as tf
                print(f"✅ {module}: {tf.__version__}")
            else:
                exec(f"import {module}")
                print(f"✅ {module}: OK")
        except ImportError:
            print(f"❌ {module} hiányzik (telepítés: pip install {package})")
            all_good = False
    
    return all_good

def check_model_files():
    """Modell fájlok ellenőrzése"""
    print("\n🤖 Modell fájlok ellenőrzése:")
    
    models_to_check = {
        'models/classifier_model.pb': (15 * 1024 * 1024, 20 * 1024 * 1024),  # 15-20MB
        'models/classifier_labels.json': (10 * 1024, 20 * 1024),  # 10-20KB
    }
    
    all_good = True
    
    for model_path, (min_size, max_size) in models_to_check.items():
        if os.path.exists(model_path):
            size = os.path.getsize(model_path)
            size_mb = size / (1024 * 1024)
            
            if min_size <= size <= max_size:
                print(f"✅ {model_path}: {size_mb:.1f} MB")
            else:
                print(f"⚠️ {model_path}: {size_mb:.1f} MB (várt: {min_size/(1024*1024):.1f}-{max_size/(1024*1024):.1f} MB)")
                if size < 1000:  # Ha túl kicsi, valószínűleg Git LFS probléma
                    print(f"   💡 Futtasd: git lfs pull")
                all_good = False
        else:
            print(f"❌ {model_path}: nem található")
            all_good = False
    
    return all_good

def check_git_lfs():
    """Git LFS ellenőrzés"""
    print("\n📡 Git LFS ellenőrzés:")
    
    try:
        result = subprocess.run(['git', 'lfs', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git LFS telepítve: {result.stdout.strip()}")
            
            # LFS fájlok ellenőrzése
            result = subprocess.run(['git', 'lfs', 'ls-files'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                lfs_files = result.stdout.strip().split('\n')
                print(f"✅ Git LFS fájlok: {len(lfs_files)} db")
                return True
            else:
                print("⚠️ Nincsenek Git LFS fájlok")
                return False
        else:
            print("❌ Git LFS nem elérhető")
            return False
    except FileNotFoundError:
        print("❌ Git LFS nincs telepítve (sudo apt install git-lfs)")
        return False

def check_directories():
    """Könyvtár struktúra ellenőrzése"""
    print("\n📁 Könyvtárak ellenőrzése:")
    
    required_dirs = ['models', 'audio_mp3', 'essentia-models']
    all_good = True
    
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            file_count = len([f for f in os.listdir(directory) 
                            if os.path.isfile(os.path.join(directory, f))])
            print(f"✅ {directory}/: {file_count} fájl")
        else:
            print(f"❌ {directory}/: nem található")
            all_good = False
    
    return all_good

def main():
    """Fő ellenőrző függvény"""
    print("🔍 ESSENTIA MUSIC ANALYZER - TELEPÍTÉS ELLENŐRZÉS")
    print("=" * 60)
    
    checks = [
        ("Python verzió", check_python_version),
        ("Függőségek", check_imports),
        ("Modell fájlok", check_model_files),
        ("Git LFS", check_git_lfs),
        ("Könyvtárak", check_directories)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name}: Hiba - {e}")
            results.append((check_name, False))
    
    # Összesítés
    print("\n" + "=" * 60)
    print("📊 ÖSSZESÍTÉS:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    print(f"\n🏆 EREDMÉNY: {passed}/{total} ellenőrzés sikeres")
    
    if passed == total:
        print("🎉 A rendszer teljesen működőképes!")
        print("\n🚀 Futtatáshoz:")
        print("   source essentia_env/bin/activate")
        print("   python3 linux_essentia_optimized.py")
    else:
        print("\n⚠️ Javítási javaslatok:")
        if not any(name == "Git LFS" and result for name, result in results):
            print("   - sudo apt install git-lfs && git lfs pull")
        if not any(name == "Függőségek" and result for name, result in results):
            print("   - pip install -r requirements.txt")
        if not any(name == "Modell fájlok" and result for name, result in results):
            print("   - git lfs pull")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)