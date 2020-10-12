from core.node import *

DEBUG = True


class Node_material(Node):
    def __init__(self, scene, title="Material", parent=None, method=None, *args, **kwargs):
        super().__init__(Node=self)
        self.MODULO = 'Material'
        self.MODULO_INITIALIZED = False
        self.parent = parent
        self.scene = scene
        self.title = title
        self.content = QDMNodeMaterial(self)  # mando o node tambem
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(240, 200)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = []
        outputs = [{'pos': 0.88, 'type': 'dict'}]

        self.configInputsOutputs(inputs, outputs)

        self.configureObjectTree()

        if 'INDEX' in kwargs.keys():
            self.content.comboBox.setCurrentIndex(kwargs['INDEX'])


class QDMNodeMaterial(QWidget):

    def __init__(self, node, parent=None):
        super().__init__()
        self.node = node
        db = utils.Database()
        with db.database:
            data = db.database.execute("SELECT * FROM MATERIAL")

        self.materials_db = [data for data in data]
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        vframe = QFrame()
        vlayout = QVBoxLayout(vframe)
        vframe.setFixedHeight(40)
        self.layout.addWidget(vframe)
        self.comboBox = QComboBox()

        self.comboBox.addItem('Selecione o material ')
        self.comboBox.model().item(0).setEnabled(False)
        for item in self.materials_db:
            self.comboBox.addItem(item[0])
        vlayout.addWidget(self.comboBox)



        vframe = QFrame()
        vlayout = QVBoxLayout(vframe)

        vlayout.addWidget(QLabel('Propriedades'))

        gridFrame = QFrame()
        vlayout.addWidget(gridFrame)
        gridLayout = QGridLayout(gridFrame)

        gridLayout.addWidget(SVGLabel().load('\\rho', size=(20, 20)),0, 0)
        gridLayout.addWidget(SVGLabel().load('E', size=(20, 20)), 0, 1)
        self.current_property_frame = QFrame()
        self.current_property_layout = QHBoxLayout(self.current_property_frame)
        self.layout.addWidget(vframe)
        self.layout.addWidget(self.current_property_frame)

        self.comboBox.currentIndexChanged.connect(self.node.updateNode)

    def comboBoxItemBehaviour(self):
        # TODO organizar melhor a tabela com
        self.node.kwargs.update({'INDEX': self.comboBox.currentIndex()})
        currentMaterial = self.materials_db[self.comboBox.currentIndex() - 1]
        while self.current_property_layout.takeAt(0):
            pass
        self.current_property_layout.addWidget(QLabel(f'{currentMaterial[1]:.3e}'))
        self.current_property_layout.addWidget(QLabel(f'{currentMaterial[2]:.3e}'))


        dict = {'Material': currentMaterial[0],
                'Massa Específica': currentMaterial[1],
                'E': currentMaterial[2]}

        self.node.sendSignal([dict], [self.node.outputs[0]], [self], ['dict'])


    def refresh(self):
        self.comboBoxItemBehaviour()





