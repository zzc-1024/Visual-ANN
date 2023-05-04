# 有待改进
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QVBoxLayout
from keras import Model

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_MODEL


class ModelLayerContent(QDMNodeContentWidget):
    def initUI(self):
        self.VerticalBox = QVBoxLayout()
        self.labelTop = QLabel("输入层")
        self.labelMiddle = QLabel("输入层")
        self.labelBottom = QLabel("只接入一个自动判断")
        self.VerticalBox.addWidget(self.labelTop)
        self.VerticalBox.addWidget(self.labelMiddle)
        self.VerticalBox.addWidget(self.labelBottom)
        self.setLayout(self.VerticalBox)

@register_node(OP_NODE_LAYER_MODEL)
class LayerModel(CalcNode):
    icon = "icons/out.png"
    op_code = OP_NODE_LAYER_MODEL
    op_title = "生成模型"
    content_objname = "layer_model"

    def __init__(self, scene):
        super().__init__(scene)
        self.eval()

    def initInnerClasses(self):
        self.content = ModelLayerContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 180
        self.grNode.height += 74 + 52

    def evalImplementation(self):
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        if i1 is None and i2 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            return None
        elif i1 is None or i2 is None:
            inp = i1
            if i1 is None:
                inp = i2
            inp = inp.eval()
            value = self.evalOperation(inp[0], inp[1])

        else:
            i1 = i1.eval()
            i2 = i2.eval()
            value = self.evalOperation(i1[0], i2[1])
        self.value = value
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return value

    def evalOperation(self, input1, input2):
        return [input1, Model(input1, input2)]
