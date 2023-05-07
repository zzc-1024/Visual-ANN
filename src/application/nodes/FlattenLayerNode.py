from qtpy.QtWidgets import QVBoxLayout, QLabel
from keras.layers import Flatten

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_FLATTEN


class FlattenLayerNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.label = QLabel("将输入层改为一维", self)
        self.label.setObjectName(self.node.content_objname)


@register_node(OP_NODE_LAYER_FLATTEN)
class FlattenLayerNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_FLATTEN
    op_title = "拉伸层"
    content_objname = "flatten_layer_node"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = FlattenLayerNodeContent(self)
        self.grNode = CalcGraphicsNode(self)

    def evalImplementation(self):
        inp = self.getInput()
        if inp is None:
            self.markDirty()
            self.markInvalid()
            return
        inp = inp.eval()
        value = [
            inp[0],
            Flatten()(inp[1])
        ]
        self.value = value
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return value

