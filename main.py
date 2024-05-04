import keyboard  # keyboarimport
from aimbot import Aimbot


def toggle_aimbot():
    Aimbot.status_aimbot()

keyboard.add_hotkey('F1', toggle_aimbot)  # F1キーが押されたときにtoggle_aimbot関数を呼び出す
#keyboard.add_hotkey('F2', quit_program)  # F2キーが押されたときにquit_program関数を呼び出す

# メインプログラムの続行中にキー入力を監視
keyboard.wait()