import SDK.GameLoop as GameLoop
from Tool.Process import *
import UI.MainUI as GUI
import threading, signal, sys, os, webbrowser
import Function.Visual as Visual
import Function.AimBot as AimBot
import Function.TriggerBot as TriggerBot
import Function.AutoPistol as AutoPistol
import Function.BunnyHop as BunnyHop
import Function.RecoilControl as RecoilControl

Game.Connect("cs2.exe", "Counter-Strike 2")
GameLoop.GameLoop.Start()

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

   
    app.run()