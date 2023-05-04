from qtpy.QtWidgets import QLineEdit, QPushButton, QSpacerItem
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtWidgets import QVBoxLayout, QHBoxLayout
from keras.layers import Input

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_socket import RIGHT_TOP
from nodeeditor.utils import dumpException

from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_INPUT
from src.application.calc_node_base import CalcNode, CalcGraphicsNode


class LayerInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        horizonBox = QHBoxLayout()
        self.sub = QPushButton("-")
        self.sub.setStyleSheet("width:40px")
        self.sub.setObjectName(self.node.content_objname)

        self.add = QPushButton("+")
        self.add.setStyleSheet("width:40px")
        self.add.setObjectName(self.node.content_objname)

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        horizonBox.addWidget(self.sub)
        horizonBox.addWidget(self.add)
        self.verticalBox.addLayout(horizonBox)
        line = QLineEdit("1")
        line.setObjectName(self.node.content_objname)
        self.verticalBox.addWidget(line)
        self.verticalBox.addSpacerItem(self.spacer)
        self.setLayout(self.verticalBox)

    def serialize(self):
        res = super().serialize()
        res['value'] = []
        for i in range(1, self.verticalBox.count() - 1):
            res['value'].append(self.verticalBox.itemAt(i).widget().text())
        return res

    def deserialize(self, data, hashmap = {}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.verticalBox.removeItem(self.spacer)
            it = self.verticalBox.itemAt(1)
            self.verticalBox.removeItem(it)
            self.node.grNode.height -= 52
            it = it.widget()
            it.deleteLater()
            for it in value:
                line = QLineEdit(it)
                line.textChanged.connect(self.node.onInputChanged)
                line.setObjectName(self.node.content_objname)
                self.verticalBox.addWidget(line)
                self.node.grNode.height += 52
            self.verticalBox.addSpacerItem(self.spacer)
            self.node.markDirty()
            self.node.eval()
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_LAYER_INPUT)
class LayerInput(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_INPUT
    op_title = "输入层"
    content_objname = "layer_input"

    def __init__(self, scene):
        super().__init__(scene,inputs=[], outputs=[3])
        self.eval()

    def initSettings(self):
        super().initSettings()
        self.output_socket_position = RIGHT_TOP

    def initInnerClasses(self):
        self.content = LayerInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 180
        self.grNode.height += 74
        self.content.sub.clicked.connect(self.onSubPressed)
        self.content.sub.clicked.connect(self.onInputChanged)
        self.content.add.clicked.connect(self.onAddPressed)
        self.content.add.clicked.connect(self.onInputChanged)
        widget = self.content.verticalBox.itemAt(1).widget()
        widget.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        res = []
        for i in range(1, self.content.verticalBox.count() - 1):
            param = self.content.verticalBox.itemAt(i).widget().text()
            param = int(param)
            res.append(param)
        res = tuple(res)
        res = Input(shape=res)
        res = [res, res]
        self.value = res
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.markDescendantsInvalid(False)
        self.evalChildren()
        return res

    def onSubPressed(self):
        if self.content.verticalBox.count() <= 3:
            return
        index = self.content.verticalBox.count() - 2
        it = self.content.verticalBox.itemAt(index)
        self.content.verticalBox.removeItem(self.content.spacer)
        self.content.verticalBox.removeItem(it)
        it = it.widget()
        it.deleteLater()
        self.grNode.height -= 52
        self.content.verticalBox.addSpacerItem(self.content.spacer)

    def onAddPressed(self):
        line = QLineEdit("1")
        line.setObjectName(self.content_objname)
        line.textChanged.connect(self.onInputChanged)
        self.content.verticalBox.removeItem(self.content.spacer)
        self.content.verticalBox.addWidget(line)
        self.content.verticalBox.addSpacerItem(self.content.spacer)
        self.grNode.height += 52
