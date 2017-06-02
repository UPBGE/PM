import bge.logic as logic
import scripts.localplayer as player


def startup():
    logic.getCurrentController().owner["class"] = player.LocalPlayer()

def update():
    playerInstance = logic.getCurrentController().owner["class"]
    playerInstance.keyboardUpdate()
    playerInstance.mouseUpdate()
    playerInstance.virtual_parpaing()
