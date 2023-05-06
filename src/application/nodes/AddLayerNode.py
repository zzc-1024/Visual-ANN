# 可以改为merge层
from qtpy.QtWidgets import QVBoxLayout, QLabel
from keras.layers import Add

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_ADD

class AddLayerNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.tip = QLabel("合并两个输入")
        self.verticalBox.addWidget(self.tip)
        self.setLayout(self.verticalBox)


@register_node(OP_NODE_LAYER_ADD)
class AddLayerNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_ADD
    op_title = "张量加法"
    content_objname = "add_layer_node"

    def __init__(self, scene):
        super().__init__(scene)
        self.eval()

    def initInnerClasses(self):
        self.content = AddLayerNodeContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.height += 74

    def evalOperation(self, input1, input2):
        return [
            Add()([
                input1[0],
                input2[0]
            ]),
            Add()([
                input1[1],
                input2[1]
            ])
        ]
