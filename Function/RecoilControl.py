import win32api
import win32con
import win32gui
import time
import psutil

# RCS settings
RecoilControlStatus = False
Sensitivity = 1.0  # Mouse sensitivity multiplier
Weapon = "AK-47"  # Default weapon

# Recoil patterns (dx, dy) where positive dy represents upward recoil
# Scaled by 2.0 to mimic C++ aim punch effect (vPunch * 2.0)

RECOIL_PATTERNS = {
    "AK-47": [
        (0, 0),    # Bullet 1: No recoil
        (0, 4),    # Bullet 2: Strong upward
        (2, 6),    # Bullet 3: Upward with slight right
        (4, 8),    # Bullet 4: Stronger upward, more right
        (6, 10),   # Bullet 5: Peak upward, right
        (8, 10),   # Bullet 6: High upward, max right
        (4, 8),    # Bullet 7: Slight downward trend, less right
        (0, 6),    # Bullet 8: Upward, center
        (-2, 6),   # Bullet 9: Upward, slight left
        (-4, 4),   # Bullet 10: Reduced upward, more left
        (-6, 4),   # Bullet 11: Upward, stronger left
        (-4, 3),   # Bullet 12: Reduced upward, left
        (0, 3),    # Bullet 13: Upward, center
        (2, 2),    # Bullet 14: Slight upward, slight right
        (4, 2),    # Bullet 15: Slight upward, right
        (2, 1),    # Bullet 16: Minimal upward, right
        (0, 1),    # Bullet 17: Minimal upward, center
        (-2, 1),   # Bullet 18: Minimal upward, slight left
        (-4, 1),   # Bullet 19: Minimal upward, left
        (-2, 0),   # Bullet 20: No vertical, slight left
    ],
    "M4A4": [
        (0, 0),    # Bullet 1
        (0, 2),    # Bullet 2
        (0, 4),    # Bullet 3
        (2, 4),    # Bullet 4
        (2, 6),    # Bullet 5
        (0, 6),    # Bullet 6
        (-2, 4),   # Bullet 7
        (-2, 4),   # Bullet 8
        (0, 2),    # Bullet 9
        (0, 2),    # Bullet 10
        (0, 2),    # Bullet 11
        (0, 2),    # Bullet 12
        (0, 2),    # Bullet 13
        (0, 2),    # Bullet 14
        (0, 2),    # Bullet 15
        (0, 1),    # Bullet 16
        (0, 1),    # Bullet 17
        (0, 1),    # Bullet 18
        (0, 1),    # Bullet 19
        (0, 1),    # Bullet 20
    ],
}

def is_game_running():
    """
    Check if cs2.exe is running using psutil.
    """
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == 'cs2.exe':
                return True
        print("[DEBUG] CS2 process not found")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to check game process: {e}")
        return False

def is_game_window_active():
    """
    Check if the CS2 window is the active (foreground) window.
    """
    try:
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd).lower()
        if "counter-strike 2" in window_title:
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Failed to check active window: {e}")
        return False

def Function():
    """
    Main loop for Recoil Control System.
    Simulates mouse movements to counteract recoil, inspired by C++ aim punch logic.
    """
    global RecoilControlStatus, Weapon, Sensitivity
    print("[INFO] Recoil Control thread started")
    try:
        while True:
            if not RecoilControlStatus or not is_game_running() or not is_game_window_active():
                time.sleep(0.1)
                continue

            # Check if player is firing (left mouse button held)
            if win32api.GetKeyState(win32con.VK_LBUTTON) < 0:
                print("[DEBUG] Left mouse button held, applying recoil control")
                pattern = RECOIL_PATTERNS.get(Weapon, [])
                shot_count = 0

                while (win32api.GetKeyState(win32con.VK_LBUTTON) < 0 and
                       shot_count < len(pattern) and
                       is_game_running() and
                       is_game_window_active() and
                       RecoilControlStatus):
                    if shot_count < len(pattern):
                        dx, dy = pattern[shot_count]
                        print("getting from patterns: ","x: ", dx ,"///// y: ",dy)
                        # Positive dy in pattern = upward recoil
                        # Apply negative dy to move mouse downward
                        dx = int(dx / Sensitivity)
                        dy = int(-dy / Sensitivity)  # Negative dy for downward movement
                        print(f"[DEBUG] Moving mouse: dx={dx}, dy={dy}")
                        win32api.mouse_event(
                            win32con.MOUSEEVENTF_MOVE,
                            dx,
                            -dy
                        )
                    else:
                        print("[DEBUG] Reached end of recoil pattern")
                        break

                    shot_count += 1
                    time.sleep(0.01)  # Simulate weapon fire rate

            time.sleep(0.016)  # ~60 FPS loop

    except Exception as e:
        print(f"[ERROR] RecoilControl failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("[INFO] Recoil Control thread stopped")