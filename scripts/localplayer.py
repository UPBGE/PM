import bge.logic as logic
import bge.logic as logic
import bge.events as events
import bge.constraints as constraints
import math
from mathutils import Vector
from scripts.parpaing import Parpaing

class LocalPlayer:
    def __init__(self):
        self.scene = logic.getCurrentScene()
        #Define alias to objects of the player
        self.hitbox = self.scene.objects["player.hitbox"]
        self.viseur1 = self.scene.objects["player.viseur1"]
        self.viseur2 = self.scene.objects["player.viseur2"]
        self.camera = self.scene.objects["player.camera"]
        self.manche = self.scene.objects["player.manche"]
        self.virtualParpaing = self.scene.objects["virtual_parpaing"]

        self.mouse = logic.mouse
        self.keyboard = logic.keyboard

        self.mode = 1 #The orientation of the parpaing

    #Detect if pressed or just activated at the last frame:
    def isPressedM(self, event):
        return logic.KX_INPUT_JUST_ACTIVATED in self.mouse.inputs[event].queue
    def isPressedK(self, event):
        return logic.KX_INPUT_JUST_ACTIVATED in self.keyboard.inputs[event].queue
    def isActivatedM(self, event):
        return logic.KX_INPUT_ACTIVE in self.mouse.inputs[event].status
    def isActivatedK(self, event):
        return logic.KX_INPUT_ACTIVE in self.keyboard.inputs[event].status

    def keyboardUpdate(self):
        if self.isActivatedK(events.ZKEY):
            self.hitbox.applyMovement((-.15, 0, 0), True)
        if self.isActivatedK(events.SKEY):
            self.hitbox.applyMovement((.15, 0, 0), True)
        if self.isActivatedK(events.QKEY):
            self.hitbox.applyMovement((0, -.15, 0), True)
        if self.isActivatedK(events.DKEY):
            self.hitbox.applyMovement((0, .15, 0), True)
        if self.isActivatedK(events.SPACEKEY):
            constraints.getCharacter(self.hitbox).jump()
        if self.isPressedK(events.EKEY):
            self.mode *= -1
        if self.isPressedK(events.RKEY):
            self.throwParpaing()
        if self.isPressedK(events.TKEY):
            self.orientationParpaing()

    def mouseUpdate(self):
        if self.isPressedM(events.RIGHTMOUSE):
            self.putParpaing()
        if self.isPressedM(events.LEFTMOUSE):
            self.supprParpaing()

    def putParpaing(self):
            self.viseur1["parpaings"] += 1 #count parpaing
            newPar = Parpaing(self.scene.addObject("Parpaing"))
            newPar.position = self.virtualParpaing.position
            newPar.orientation = self.virtualParpaing.orientation

    def supprParpaing(self):
        self.viseur1["parpaings"] -= 1
        cible = self.viseur1.rayCast(self.viseur2, None, 6)[0]

        if cible:
            if cible.name == "Parpaing":
                cible.endObject()

    def virtual_parpaing(self):
        rayCatch = self.viseur1.rayCast(self.viseur2, None, 30)

        if rayCatch[0]:
            self.virtualParpaing.position = (round(rayCatch[1][0], 0), round(rayCatch[1][1], 0), round(rayCatch[1][2],0)+.3)
            ori = self.virtualParpaing.orientation.to_euler()
            if self.mode == 1:
                ori[2] = math.pi/2
            else:
                ori[2] = 0
                self.virtualParpaing.applyMovement((-.5, -.5, 0), True)
            self.virtualParpaing.orientation = ori
            #Test y-axis
            if self.mode == 1:
                if round(rayCatch[0].position[1], 0) +1 == round(self.virtualParpaing.position[1], 0):
                    self.virtualParpaing.position[1]+=1
                elif round(rayCatch[0].position[1], 0) -1 == round(self.virtualParpaing.position[1], 0):
                    self.virtualParpaing.position[1]-=1
            """else:
                if round(rayCatch[0].position[0], 0) -1 == round(self.virtualParpaing.position[0], 0):
                    self.virtualParpaing.position[0]+=1
                elif round(rayCatch[0].position[0], 0) +1 == round(self.virtualParpaing.position[0], 0):
                    self.virtualParpaing.position[0]-=1"""
        else:
            self.virtualParpaing.position = (0, 0, -100)

    def throwParpaing(self):
        newParpaing = self.scene.addObject("Parpaing", None)
        newParpaing.worldPosition = self.viseur1.worldPosition
        newParpaing.worldOrientation = self.viseur1.worldOrientation
        newParpaing.localLinearVelocity = (-20, 0, 0)

        self.viseur1["parpaings"] += 1

    def orientationParpaing(self):
        cible = self.viseur1.rayCast(self.viseur2, None, 30)[0]
        if cible.name == "Parpaing":
            cible.applyMovement((.1, .1, 0), True)
            cible.position = (round(cible.position[0], 0), round(cible.position[1], 0), cible.position[2])
            if self.mode == 1:
                cible.orientation=(0, 0, math.pi/2)
            else:
                cible.orientation=(0, 0, 0)
                cible.applyMovement((-.5, -.5, 0), True)
