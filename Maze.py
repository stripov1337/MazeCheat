import SDK.GameLoop as GameLoop

from Tool.Process import *
import UI.MainUI as GUI
import threading, signal, sys, os, webbrowser

import Function.Visual as Visual
import Function.AimBot as AimBot
import Function.TriggerBot as TriggerBot
import Function.AutoPistol as AutoPistol
import Function.BunnyHop as BunnyHop


Game.Connect("cs2.exe", "Counter-Strike 2")
GameLoop.GameLoop.Start()   


if __name__ == "__main__":
   app = GUI.QtWidgets.QApplication(sys.argv)
   ui = GUI.Widget()
   ui.show()

   def StartVisual():
      Visual.VisualStatus = ui.visualCheckBox.checkState()

      if (Visual.VisualStatus):
         threading.Thread(target = Visual.Function).start()


   def StartAimBot():
      AimBot.AimBotStatus = ui.aimAsistCheckBox.checkState()

      if (AimBot.AimBotStatus):
         threading.Thread(target = AimBot.Function).start()


   def StartTriggerBot():
      TriggerBot.TriggerBotStatus = ui.triggerBotCheckBox.checkState()

      if (TriggerBot.TriggerBotStatus):
         threading.Thread(target = TriggerBot.Function).start()


   def StartAutoPistol():
      AutoPistol.AutoPistolStatus = ui.autoPistolCheckBox.checkState()

      if (AutoPistol.AutoPistolStatus):
         threading.Thread(target = AutoPistol.Function).start()


   def StartBunnyHop():
      BunnyHop.BunnyHopStatus = ui.bunnyHopCheckBox.checkState()

      if (BunnyHop.BunnyHopStatus):
         threading.Thread(target = BunnyHop.Function).start()
         

   ui.visualSettingButton.clicked.connect(ui.ShowVisualWindow)
   ui.aimAsistSettingButton.clicked.connect(ui.ShowAimBotWindow)
   ui.triggerBotSettingButton.clicked.connect(ui.ShowTriggerBotWindow)
   ui.autoPistolSettingButton.clicked.connect(ui.ShowAutoPistolWindow)

   ui.visualCheckBox.stateChanged.connect(StartVisual)
   ui.aimAsistCheckBox.stateChanged.connect(StartAimBot)
   ui.triggerBotCheckBox.stateChanged.connect(StartTriggerBot)
   ui.autoPistolCheckBox.stateChanged.connect(StartAutoPistol)
   ui.bunnyHopCheckBox.stateChanged.connect(StartBunnyHop)
   
   ui.closeButton.clicked.connect(lambda: os.kill(os.getpid(), signal.SIGTERM))
   ui.questionButton.clicked.connect(lambda: webbrowser.open("https://yougame.biz/threads/333315", new = 2))
   sys.exit(app.exec_())

    