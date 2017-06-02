import bge.logic as logic
import bge.types as types

class Parpaing(types.KX_GameObject):
    def __init__(self, parent):
        self.deactivate()
        self.maxImpulse = 50
        self.collisionCallbacks.append(self.callback)

    def deactivate(self):
        self.suspendDynamics()

    def activate(self):
        self.restoreDynamics()

    #Collision callback, compute
    def callback(self, object, point, normal, points):
        for p in points:
            if p.appliedImpulse > self.maxImpulse:
                self.activate()
                print(p.appliedImpulse)
