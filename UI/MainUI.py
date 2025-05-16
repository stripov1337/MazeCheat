# -*- coding: utf-8 -*-
import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
import Function.Visual as Visual
import Function.AimBot as AimBot
import Function.TriggerBot as TriggerBot
import Function.AutoPistol as AutoPistol
import Function.RecoilControl as RecoilControl
import Function.BunnyHop as BunnyHop
import SDK.GameVar as GameVar

import threading, signal, sys, os, webbrowser, requests, time, atexit, shutil, glob

def cleanup_pycache():
    ctt=0
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)

    sibling_dirs = [os.path.join(parent_dir, d) for d in os.listdir(parent_dir) 
                   if os.path.isdir(os.path.join(parent_dir, d))]
    
    print("Сбрасываю хвосты...")
    for dir_path in sibling_dirs:
        ctt+=1
        for pycache_path in glob.glob(os.path.join(dir_path, "**", "__pycache__"), recursive=True):
            try:
                shutil.rmtree(pycache_path)
                print(f"Удалил: Файл номер {ctt}")
            except Exception as e:
                print(f"Неудачно удалил {pycache_path}: {e}")
    print("Готово")





class Widget:
    def __init__(self):
        
        self.visual_check_var = False
        self.aim_check_var = False
        self.trigger_check_var = False
        self.auto_pistol_check_var = False
        self.bunny_hop_check_var = False
        self.recoil_check_var = False

        
        self.box_check_var = Visual.BoxESPStatus
        self.team_check_var = Visual.TeamCheck
        self.health_check_var = Visual.HealthStatus
        self.weapon_check_var = Visual.WeaponStatus
        self.line_check_var = Visual.LineStatus
        self.crosshair_check_var = Visual.CrosshairStatus
        self.bomb_check_var = Visual.BombESPStatus
        self.crosshair_size = float(Visual.CrosshairSize)
        self.box_color = self.hex_to_rgb(Visual.BoxESPColor)
        self.line_color = self.hex_to_rgb(Visual.LineColor)
        self.crosshair_color = self.hex_to_rgb(Visual.CrosshairColor)

        
        self.aim_team_check_var = AimBot.TeamCheck
        self.fov_check_var = AimBot.AimBotFOVStatus
        self.fov = float(AimBot.Fov)
        self.smooth = float(AimBot.Smooth)
        self.aim_max_shot = float(AimBot.MaxShot)
        self.aim_mouse = "None" if AimBot.VirtualKey == 0 else f"MOUSE{AimBot.VirtualKey}"
        self.bone = GameVar.GameVar.BoneListName[AimBot.Bone]
        self.fov_color = self.hex_to_rgb(AimBot.AimFOVColor)

        
        self.trigger_team_check_var = TriggerBot.TeamCheck
        self.delay = float(TriggerBot.Delay)
        self.trigger_max_shot = float(TriggerBot.MaxShot)
        self.trigger_mouse = "None" if TriggerBot.VirtualKey == 0 else f"MOUSE{TriggerBot.VirtualKey}"

        
        self.auto_pistol_mouse = "None" if AutoPistol.VirtualKey == 0 else f"MOUSE{AutoPistol.VirtualKey}"

        
        self.sensitivity = RecoilControl.Sensitivity
        self.weapon = RecoilControl.Weapon

        
        self.is_dragging = False
        self.drag_start_pos = (0, 0)
        self.window_start_pos = (0, 0)

        
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)  # Disable window resizing and maximization
        
        self.window = glfw.create_window(430, 340, "Maze V7", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        glfw.make_context_current(self.window)
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        
       

        style = imgui.get_style()
        style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.12, 0.12, 0.14, 1.0)
        style.colors[imgui.COLOR_FRAME_BACKGROUND] = (0.2, 0.2, 0.22, 1.0)
        style.colors[imgui.COLOR_BUTTON] = (0.2, 0.2, 0.22, 1.0)
        style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.3, 0.3, 0.32, 1.0)
        style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.4, 0.4, 0.42, 1.0)
        style.colors[imgui.COLOR_CHECK_MARK] = (0.91, 0.26, 0.09, 1.0)
        style.colors[imgui.COLOR_SLIDER_GRAB] = (0.0, 0.59, 0.90, 1.0)
        style.colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (0.0, 0.69, 1.0, 1.0)

    def hex_to_rgb(self, hex_color):
        if not hex_color:
            return [1.0, 1.0, 1.0, 1.0]
        hex_color = hex_color.lstrip('#')
        rgb = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        return rgb + [1.0]

    def rgb_to_hex(self, rgb):
        rgb = [max(0, min(int(c * 255), 255)) for c in rgb[:3]]
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def get_screen_cursor_pos(self):

        window_x, window_y = glfw.get_window_pos(self.window)
        cursor_x, cursor_y = glfw.get_cursor_pos(self.window)
        return (window_x + cursor_x, window_y + cursor_y)

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            
            imgui.new_frame()
            

            imgui.begin("Maze V7", False, imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
            

            io = imgui.get_io()
            if imgui.is_window_hovered() and imgui.is_mouse_down(0) and not io.want_capture_mouse:
                if not self.is_dragging:
                    self.is_dragging = True
                    self.drag_start_pos = self.get_screen_cursor_pos()
                    self.window_start_pos = glfw.get_window_pos(self.window)
                else:
                    current_pos = self.get_screen_cursor_pos()
                    delta_x = current_pos[0] - self.drag_start_pos[0]
                    delta_y = current_pos[1] - self.drag_start_pos[1]
                    new_pos = (self.window_start_pos[0] + delta_x, self.window_start_pos[1] + delta_y)
                    glfw.set_window_pos(self.window, int(new_pos[0]), int(new_pos[1]))
            else:
                self.is_dragging = False
            
            # Tabs
            if imgui.begin_tab_bar("MainTabs"):
                # Visuals Tab
                if imgui.begin_tab_item("Visuals")[0]:
                    changed, self.visual_check_var = imgui.checkbox("Enable Visual", self.visual_check_var)
                    if changed:
                        Visual.VisualStatus = self.visual_check_var
                        if Visual.VisualStatus:
                            threading.Thread(target=Visual.Function, daemon=True).start()
                    
                    imgui.separator()
                    
                    changed, self.box_check_var = imgui.checkbox("Box ESP", self.box_check_var)
                    if changed:
                        Visual.BoxESPStatus = self.box_check_var
                    
                    changed, self.team_check_var = imgui.checkbox("Team Check", self.team_check_var)
                    if changed:
                        Visual.TeamCheck = self.team_check_var
                    
                    changed, self.health_check_var = imgui.checkbox("Health Bar", self.health_check_var)
                    if changed:
                        Visual.HealthStatus = self.health_check_var
                    
                    changed, self.weapon_check_var = imgui.checkbox("Weapon", self.weapon_check_var)
                    if changed:
                        Visual.WeaponStatus = self.weapon_check_var
                    
                    changed, self.line_check_var = imgui.checkbox("Line", self.line_check_var)
                    if changed:
                        Visual.LineStatus = self.line_check_var
                    
                    changed, self.crosshair_check_var = imgui.checkbox("Sniper Crosshair", self.crosshair_check_var)
                    if changed:
                        Visual.CrosshairStatus = self.crosshair_check_var
                    
                    changed, self.bomb_check_var = imgui.checkbox("Bomb Timer", self.bomb_check_var)
                    if changed:
                        Visual.BombESPStatus = self.bomb_check_var
                    
                    changed, self.crosshair_size = imgui.slider_float("Crosshair Size", self.crosshair_size, 2, 20)
                    if changed:
                        Visual.CrosshairSize = int(self.crosshair_size)
                    
                    changed, self.box_color = imgui.color_edit4("Box Color", *self.box_color)
                    if changed:
                        Visual.BoxESPColor = self.rgb_to_hex(self.box_color)
                    
                    changed, self.line_color = imgui.color_edit4("Line Color", *self.line_color)
                    if changed:
                        Visual.LineColor = self.rgb_to_hex(self.line_color)
                    
                    changed, self.crosshair_color = imgui.color_edit4("Crosshair Color", *self.crosshair_color)
                    if changed:
                        Visual.CrosshairColor = self.rgb_to_hex(self.crosshair_color)
                    
                    imgui.end_tab_item()
                
                # Aim Assist Tab
                if imgui.begin_tab_item("Aim Assist")[0]:
                    changed, self.aim_check_var = imgui.checkbox("Enable Aim Assist", self.aim_check_var)
                    if changed:
                        AimBot.AimBotStatus = self.aim_check_var
                        if AimBot.AimBotStatus:
                            threading.Thread(target=AimBot.Function, daemon=True).start()
                    
                    
                    if self.aim_check_var:
                        changed, self.aim_team_check_var = imgui.checkbox("Team Check", self.aim_team_check_var)
                        if changed:
                            AimBot.TeamCheck = self.aim_team_check_var
                        
                        changed, self.fov_check_var = imgui.checkbox("Show FOV", self.fov_check_var)
                        if changed:
                            AimBot.AimBotFOVStatus = self.fov_check_var
                        
                        changed, self.fov = imgui.slider_float("FOV", self.fov, 1, 360)
                        if changed:
                            AimBot.Fov = int(self.fov)
                        
                        changed, self.smooth = imgui.slider_float("Smooth", self.smooth, 1, 10)
                        if changed:
                            AimBot.Smooth = int(self.smooth)
                        
                        changed, self.aim_max_shot = imgui.slider_float("Max Shots", self.aim_max_shot, 0, 10)
                        if changed:
                            AimBot.MaxShot = int(self.aim_max_shot)
                        
                        changed, self.fov_color = imgui.color_edit4("FOV Color", *self.fov_color)
                        if changed:
                            AimBot.AimFOVColor = self.rgb_to_hex(self.fov_color)
                        
                        mouse_options = ["MOUSE1", "MOUSE2", "MOUSE4", "MOUSE5", "MOUSE6", "None"]
                        mouse_index = mouse_options.index(self.aim_mouse)
                        changed, new_index = imgui.combo("Mouse List", mouse_index, mouse_options)
                        if changed:
                            self.aim_mouse = mouse_options[new_index]
                            AimBot.VirtualKey = {"MOUSE1": 1, "MOUSE2": 2, "MOUSE4": 4, "MOUSE5": 5, "MOUSE6": 6, "None": 0}.get(self.aim_mouse, 0)
                        
                        bone_options = ["Head", "Heck", "Chest", "Stomach", "Nearest"]
                        bone_index = bone_options.index(self.bone)
                        changed, new_index = imgui.combo("Bone List", bone_index, bone_options)
                        if changed:
                            self.bone = bone_options[new_index]
                            AimBot.Bone = {"Head": 6, "Heck": 5, "Chest": 4, "Stomach": 0, "Nearest": -1}.get(self.bone, -1)
                    
                    imgui.separator()
                    
                    changed, self.trigger_check_var = imgui.checkbox("Enable Trigger Bot", self.trigger_check_var)
                    if changed:
                        TriggerBot.TriggerBotStatus = self.trigger_check_var
                        if TriggerBot.TriggerBotStatus:
                            threading.Thread(target=TriggerBot.Function, daemon=True).start()
                    
                    # TriggerBot Settings (shown only if Trigger Bot is enabled)
                    if self.trigger_check_var:
                        changed, self.trigger_team_check_var = imgui.checkbox("Team Check (Trigger)", self.trigger_team_check_var)
                        if changed:
                            TriggerBot.TeamCheck = self.trigger_team_check_var
                        
                        changed, self.delay = imgui.slider_float("Delay", self.delay, 10, 1000)
                        if changed:
                            TriggerBot.Delay = int(self.delay)
                        
                        changed, self.trigger_max_shot = imgui.slider_float("Max Shots (Trigger)", self.trigger_max_shot, 0, 10)
                        if changed:
                            TriggerBot.MaxShot = int(self.trigger_max_shot)
                        
                        mouse_options = ["MOUSE1", "MOUSE2", "MOUSE4", "MOUSE5", "MOUSE6", "None"]
                        mouse_index = mouse_options.index(self.trigger_mouse)
                        changed, new_index = imgui.combo("Mouse List (Trigger)", mouse_index, mouse_options)
                        if changed:
                            self.trigger_mouse = mouse_options[new_index]
                            TriggerBot.VirtualKey = {"MOUSE1": 1, "MOUSE2": 2, "MOUSE4": 4, "MOUSE5": 5, "MOUSE6": 6, "None": 0}.get(self.trigger_mouse, 0)
                    
                    imgui.separator()
                    
                    changed, self.recoil_check_var = imgui.checkbox("Enable Recoil Control", self.recoil_check_var)
                    if changed:
                        RecoilControl.RecoilControlStatus = self.recoil_check_var
                        if RecoilControl.RecoilControlStatus:
                            threading.Thread(target=RecoilControl.Function, daemon=True).start()
                    
                    # RecoilControl Settings (shown only if Recoil Control is enabled)
                    if self.recoil_check_var:
                        changed, self.sensitivity = imgui.slider_float("Sensitivity", self.sensitivity, 0.1, 2.0)
                        if changed:
                            RecoilControl.Sensitivity = self.sensitivity
                        
                        weapon_options = ["AK-47", "M4A4"]
                        weapon_index = weapon_options.index(self.weapon)
                        changed, new_index = imgui.combo("Weapon", weapon_index, weapon_options)
                        if changed:
                            self.weapon = weapon_options[new_index]
                            RecoilControl.Weapon = self.weapon
                    
                    imgui.end_tab_item()
                
                # Misc Tab
                if imgui.begin_tab_item("Misc")[0]:
                    changed, self.auto_pistol_check_var = imgui.checkbox("Enable Auto Pistol", self.auto_pistol_check_var)
                    if changed:
                        AutoPistol.AutoPistolStatus = self.auto_pistol_check_var
                        if AutoPistol.AutoPistolStatus:
                            threading.Thread(target=AutoPistol.Function, daemon=True).start()
                    
                    
                    if self.auto_pistol_check_var:
                        mouse_options = ["MOUSE2", "MOUSE4", "MOUSE5", "MOUSE6"]
                        mouse_index = mouse_options.index(self.auto_pistol_mouse) if self.auto_pistol_mouse in mouse_options else 0
                        changed, new_index = imgui.combo("Mouse List", mouse_index, mouse_options)
                        if changed:
                            self.auto_pistol_mouse = mouse_options[new_index]
                            AutoPistol.VirtualKey = {"MOUSE2": 2, "MOUSE4": 4, "MOUSE5": 5, "MOUSE6": 6}.get(self.auto_pistol_mouse, 0)
                    
                    imgui.separator()
                    
                    changed, self.bunny_hop_check_var = imgui.checkbox("Enable Bunny Hop", self.bunny_hop_check_var)
                    if changed:
                        BunnyHop.BunnyHopStatus = self.bunny_hop_check_var
                        if BunnyHop.BunnyHopStatus:
                            threading.Thread(target=BunnyHop.Function, daemon=True).start()
                    
                    imgui.end_tab_item()
                
                imgui.end_tab_bar()
            
            imgui.end()
            
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)
        
        self.impl.shutdown()
        glfw.terminate()
        cleanup_pycache()
        os.kill(os.getpid(), signal.SIGTERM)