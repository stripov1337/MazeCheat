import time

from Tool.Process import *
from Tool.Device.Mouse import *

from Classes.Entity import *
from Classes.Player import *
from Classes.Weapon import *

from SDK.GameVar import *
from SDK.GameSDK import *

from SDK.Render import *


AimBotStatus = False
AimBotFOVStatus = False
TeamCheck = True

Bone = -1   
Fov = 90
Smooth = 1
VirtualKey = 1
MaxShot = 5

AimFOVColor = "#ffffff"


def MoveMouseSmooth(x, y, smooth):
    """
    Smoothly moves the mouse by relative deltas using mouse events.
    x, y: Target delta in pixels relative to screen center.
    smooth: Smoothing factor (higher = slower/smoother movement).
    """
    try:
        import win32api
        import win32con
        import time

        # Scale deltas by smoothing factor
        scaled_x = x / smooth
        scaled_y = y / smooth

        # Single-step movement for simplicity and responsiveness
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(scaled_x), int(scaled_y), 0, 0)

        # Debug: Print applied movement
        print(f"Debug: Applied mouse movement: ({scaled_x}, {scaled_y})")

        # Small delay to prevent jitter
        time.sleep(0.01 / smooth)

    except Exception as e:
        print(f"Mouse movement error: {str(e)}")


def getBestTarget():
    BestEntity = csEntity(0)
    OldDistance = -9999

    Matrix = SDK.getViewMatrix()

    for Entity in GameVar.EntityList:
        if (Entity.Valid()):
            if ((TeamCheck and Entity.getTeam() == GameVar.LocalPlayer.Team) ):
                continue
            
            BoneWorldToScreen = SDK.WorldToScreen(Entity.getBonePosition(6), Matrix)
            
            if (BoneWorldToScreen.x > 0 and BoneWorldToScreen.y > 0):
                Distance = SDK.getDistanceFromCenter(BoneWorldToScreen, Fov)

                if (OldDistance < Distance and Distance > 0):
                    BestEntity = Entity
                    OldDistance = Distance

    return BestEntity


def getBestBone(Entity: csEntity):
    OldDistance = -9999
    BestBone = 6

    Matrix = SDK.getViewMatrix()

    for Bone in GameVar.BoneList:
        BoneWorldToScreen = SDK.WorldToScreen(Entity.getBonePosition(Bone), Matrix)

        if (BoneWorldToScreen.x > 0 and BoneWorldToScreen.y > 0):
            Distance = SDK.getDistanceFromCenter(BoneWorldToScreen, 360)

            if (OldDistance < Distance and Distance > 0):
                BestBone = Bone
                OldDistance = Distance

    return BestBone


def Function():
    """
    Optimized aimbot function for targeting in a game.
    Selects the target closest to the crosshair and smoothly aims at it.
    """
    try:
        Entity = csEntity(0)
        # MaxShot = 0  # Hardcoded; adjust as needed
        # VirtualKey = 0x01  # Left mouse button (VK_LBUTTON); adjust as needed
        # Smooth = 1.5  # Controls smoothness (higher = smoother/slower); adjust as needed
        # Bone = -1  # Hardcoded; adjust as needed

        while AimBotStatus:
            if not Game.WindowIsOpen():
                # print("Debug: Game window not open")
                continue

            if MaxShot > 0 and GameVar.LocalPlayer.getShotFired() >= MaxShot:
                # print("Debug: Max shots reached")
                continue

            # Check if aimbot should activate
            if (Game.KeyStatus(VirtualKey) and 
                GameVar.LocalPlayer.Alive and 
                GameVar.LocalPlayer.WeaponCattegory not in [WEAPON_KNIFE, WEAPON_BOMB]):
                
                # Debug: Confirm aimbot activation
                # print("Debug: Aimbot activated")

                # Refresh target if invalid or dead
                if not Entity.Valid() or Entity.getHealth() <= 0:
                    Entity = getBestTarget()
                    if not Entity.Valid():
                        # print("Debug: No valid target selected")
                        continue

                # Process valid target
                if Entity.Valid():
                    # Determine bone to target
                    EntityBonePosition = Entity.getBonePosition(getBestBone(Entity) if Bone == -1 else Bone)

                    # Convert world coordinates to screen
                    Matrix = SDK.getViewMatrix()
                    BonePositionWTS = SDK.WorldToScreen(EntityBonePosition, Matrix)

                    # Debug: Print target coordinates
                    print(f"Debug: Target screen pos: ({BonePositionWTS.x}, {BonePositionWTS.y})")

                    # Ensure target is on screen
                    if BonePositionWTS.x > 0 and BonePositionWTS.y > 0:
                        # Calculate mouse movement delta
                        MousePosition = Vector2()
                        MousePosition.x = BonePositionWTS.x - (GameVar.WindowScreen.x / 2)
                        MousePosition.y = BonePositionWTS.y - (GameVar.WindowScreen.y / 2)

                        # Debug: Print mouse delta
                        # print(f"Debug: Mouse delta: ({MousePosition.x}, {MousePosition.y})")

                        # Apply smoothed mouse movement
                        MoveMouseSmooth(MousePosition.x, MousePosition.y, Smooth)
                    
                       
            else:
                # Reset entity when aimbot is inactive
                Entity = csEntity(0)
                # print("Debug: Aimbot inactive (key not pressed, player dead, or invalid weapon)")

    except Exception as e:
        # print(f"Aimbot error: {str(e)}")
        Entity = csEntity(0)  # Reset entity on error