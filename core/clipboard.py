from PyQt5.QtGui import QCursor
from core import serialization
from core import node
from core import node_edge
class Clipboard:
    objects = []

    def __init__(self, scene):
        self.scene = scene

    def content(self, obj_list, cursorState):
        self.cursorState = cursorState
        print(self.cursorState)
        self.objects = obj_list

    def paste(self, event):
        # Comando executado quando o usuario pressionar Ctrl V na scene.
        #print(f'Evento {QCursor().pos()}')
        for paste_object in self.objects:
            if isinstance(paste_object, node.Node):
                serial_string = serialization.Serialization().nodeSerialization(paste_object)
                node_pasted = serialization.Serialization().nodeDeserialize(serial_string, self.scene, same_id=False)
                node_pasted.grNode.setPos(node_pasted.grNode.pos()+(QCursor().pos() - self.cursorState))
            # TODO como colar os sinais: referencia à ID nao funciona
            #if isinstance(paste_object, node_edge.Edge):
            #    serial_string = serialization.Serialization().edgeSerialization(paste_object)
            #    print(serial_string)



