from qtpy.QtWidgets import QComboBox, QDoubleSpinBox
from qtpy.QtWidgets import QVBoxLayout
from keras.layers import Activation
# 没做完，后面可以试着提供参数
# 目前做的状态是只能提供无参的激活函数
from keras.layers.activation import *

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_ACTIVATION


class LayerActivationContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.activation = QComboBox()
        self.activation.addItem("ReLU")
        self.activation.addItem("sigmoid")
        self.activation.addItem("softmax")
        self.activation.addItem("elu")
        self.activation.addItem("selu")
        self.activation.addItem("softplus")
        self.activation.addItem("softsign")
        self.activation.addItem("switch")
        self.activation.addItem("gelu")
        self.activation.addItem("tanh")
        self.activation.addItem("exponential")
        self.activation.addItem("hard_sigmoid")
        self.activation.setObjectName(self.node.content_objname)
        self.floatData = QDoubleSpinBox()
        self.floatData.setObjectName(self.node.content_objname)
        self.verticalBox.addWidget(self.activation)
        self.verticalBox.addWidget(self.floatData)
        self.setLayout(self.verticalBox)

    def serialize(self):
        res = super().serialize()
        res['activation'] = self.activation.currentIndex()
        res['float'] = self.floatData.value()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.activation.setCurrentIndex(data['activation'])
            self.floatData.setValue(data['float'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_LAYER_ACTIVATION)
class LayerActivation(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_ACTIVATION
    op_title = "激活函数"
    content_objname = "layer_activation"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = LayerActivationContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 200
        self.grNode.height += 74
        self.content.activation.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None
        else:
            inp = inp.eval()
            val = self.content.activation.currentText()
            val = Activation(val)(inp[1])
            val = [inp[0], val]
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.markDescendantsDirty()
            self.evalChildren()
            return val
