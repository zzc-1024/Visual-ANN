from qtpy.QtWidgets import QVBoxLayout, QLabel
from keras.layers import BatchNormalization

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_BATCH_NORMALIZATION


class BatchNormalizationLayerNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.tip = QLabel("批正则化")
        self.verticalBox.addWidget(self.tip)
        self.setLayout(self.verticalBox)


@register_node(OP_NODE_LAYER_BATCH_NORMALIZATION)
class BatchNormalizationLayerNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_BATCH_NORMALIZATION
    op_title = "正则化"
    content_objname = "batch_normalization_layer_node"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = BatchNormalizationLayerNodeContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.height += 22

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None
        else:
            inp = inp.eval()
            val = [
                inp[0],
                BatchNormalization()(inp[1])
            ]
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.markDescendantsDirty()
            self.evalChildren()
            return val
