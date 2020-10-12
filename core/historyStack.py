from core import serialization
import logging
DEBUG = 1


class SceneHistory:

    history_stack = []
    history_current_step = -1
    history_limit = 8

    def __init__(self, scene):
        self.scene = scene

    def undo(self):
        logging.info('Desfazer ação')
        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.sceneRestoreState(self.history_stack[self.history_current_step])

    def redo(self):
        logging.info('Refazer ação')
        if self.history_current_step + 1 < len(self.history_stack):
            self.history_current_step += 1
            self.sceneRestoreState(self.history_stack[self.history_current_step])

    def sceneRestoreState(self, state):
        node_id = state['id']
        node_obj = self.scene.getNodeFromId(node_id)

        node_obj.setPos(state['x_pos'], state['y_pos'])
        try:
            for entrydata in state['entrys']:
                node_obj.content.entrys[entrydata['index']].setText(entrydata['valor'])
        except AttributeError as error:
            logging.error('Nao encontrada entrys, pular')
        for checkboxdata in state['checkboxes']:
            node_obj.content.checkboxes[checkboxdata['index']].setChecked(checkboxdata['status'])

        node_obj.updateNode()
        node_obj.updateConnectedEdges()

    def sceneStateChange(self):
        for node in self.scene.nodes:
            self.history_stack.append(serialization.Serialization().nodeSerialization(node))
            self.history_current_step += 1
