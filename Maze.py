import SDK.GameLoop as GameLoop
from Tool.Process import *
import UI.MainUI as GUI
import threading, signal, sys, os, webbrowser, requests, time, atexit, shutil, glob
import Function.Visual as Visual
import Function.AimBot as AimBot
import Function.TriggerBot as TriggerBot
import Function.AutoPistol as AutoPistol
import Function.BunnyHop as BunnyHop
import Function.RecoilControl as RecoilControl


Game.Connect("cs2.exe", "Counter-Strike 2")
GameLoop.GameLoop.Start()

def cleanup_pycache():
    """Remove all __pycache__ directories and files."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for pycache_path in glob.glob(os.path.join(base_dir, "**", "__pycache__"), recursive=True):
        try:
            shutil.rmtree(pycache_path)
            print(f"Removed: {pycache_path}")
        except Exception as e:
            print(f"Error removing {pycache_path}: {e}")

atexit.register(cleanup_pycache)

if __name__ == "__main__":
    app = GUI.Widget()
    
    def StartVisual():
        Visual.VisualStatus = app.visual_check_var
        if Visual.VisualStatus:
            threading.Thread(target=Visual.Function, daemon=True).start()

    def StartAimBot():
        AimBot.AimBotStatus = app.aim_check_var
        if AimBot.AimBotStatus:
            threading.Thread(target=AimBot.Function, daemon=True).start()

    def StartTriggerBot():
        TriggerBot.TriggerBotStatus = app.trigger_check_var
        if TriggerBot.TriggerBotStatus:
            threading.Thread(target=TriggerBot.Function, daemon=True).start()

    def StartAutoPistol():
        AutoPistol.AutoPistolStatus = app.auto_pistol_check_var
        if AutoPistol.AutoPistolStatus:
            threading.Thread(target=AutoPistol.Function, daemon=True).start()

    def StartBunnyHop():
        BunnyHop.BunnyHopStatus = app.bunny_hop_check_var
        if BunnyHop.BunnyHopStatus:
            threading.Thread(target=BunnyHop.Function, daemon=True).start()

    def StartRecoilControl():
        RecoilControl.RecoilControlStatus = app.recoil_check_var
        if RecoilControl.RecoilControlStatus:
            threading.Thread(target=RecoilControl.Function, daemon=True).start()



    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Формируем путь к папке Tool\Offsets
    output_dir = os.path.join(base_dir, "Tool", "Offsets")

    # Создаем папку, если она не существует
    os.makedirs(output_dir, exist_ok=True)

    # Ссылки на файлы
    urls = [
        "https://raw.githubusercontent.com/a2x/cs2-dumper/refs/heads/main/output/offsets.json",
        "https://raw.githubusercontent.com/a2x/cs2-dumper/refs/heads/main/output/client_dll.json"
    ]

    # Имена файлов
    filenames = ["offsets.json", "client_dll.json"]
    print("Обновляю оффсеты")
    # Скачиваем каждый файл
    for url, filename in zip(urls, filenames):
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "wb") as file:
                file.write(response.content)


    time.sleep(1.4)


   
    app.run()