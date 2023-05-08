from qtpy.QtWidgets import QVBoxLayout, QDoubleSpinBox
from keras.layers import Dropout

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_DROPOUT


class DropoutLayerContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.rate = QDoubleSpinBox()
        self.rate.setMinimum(0.0)
        self.rate.setMaximum(1.0)
        self.rate.setObjectName(self.node.content_objname)
        self.verticalBox.addWidget(self.rate)
        self.setLayout(self.verticalBox)

    def serialize(self):
        res = super().serialize()
        res['rate'] = self.rate.value()
        return res

    def deserialize(self, data, hashmap = {}):
        res = super().deserialize(data, hashmap)
        try:
            self.rate.setValue(data['rate'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_LAYER_DROPOUT)
class DropoutLayerNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_DROPOUT
    op_title = "随机丢弃"
    content_objname = "dropout_layer_node"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = DropoutLayerContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 200
        self.grNode.height += 22
        self.content.rate.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None
        inp = inp.eval()
        rate = self.content.rate.value()
        value = Dropout(rate)(inp[1])
        self.value = [inp[0], value]
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return value
