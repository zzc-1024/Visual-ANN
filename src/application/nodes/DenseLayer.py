from qtpy.QtWidgets import QSpinBox, QComboBox, QCheckBox
from qtpy.QtWidgets import QVBoxLayout
from keras.layers import Dense

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_DENSE
from src.application.calc_node_base import CalcNode, CalcGraphicsNode


class LayerDenseContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.units = QSpinBox()
        self.units.setMinimum(1)
        self.units.setMaximum(2147483647)
        self.units.setValue(1)
        self.activation = QComboBox()
        self.activation.addItem('None')
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
        self.useBias = QCheckBox("启用偏置")
        self.useBias.setChecked(True)
        # self.useBias.setCheckState(True)
        self.units.setObjectName(self.node.content_objname)
        self.verticalBox.addWidget(self.units)
        self.verticalBox.addWidget(self.activation)
        self.activation.setObjectName(self.node.content_objname)
        self.verticalBox.addWidget(self.useBias)
        self.useBias.setObjectName(self.node.content_objname)
        self.setLayout(self.verticalBox)

    def serialize(self):
        res = super().serialize()
        res['units'] = self.units.value()
        res['activation'] = self.activation.currentIndex()
        res['useBias'] = self.useBias.isChecked()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.units.setValue(data['units'])
            self.activation.setCurrentIndex(data['activation'])
            self.useBias.setChecked(data['useBias'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_LAYER_DENSE)
class LayerDense(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_DENSE
    op_title = "全连接层"
    content_objname = "layer_dense"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = LayerDenseContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 200
        self.grNode.height += 74
        self.grNode.height += 52
        self.content.units.textChanged.connect(self.onInputChanged)
        self.content.activation.currentIndexChanged.connect(self.onInputChanged)
        self.content.useBias.stateChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None
        else:
            inp = inp.eval()
            units = self.content.units.value()
            activation = None
            if self.content.activation.currentText() == 'None':
                activation = None
            else:
                activation = self.content.activation.currentText()
            useBias = self.content.useBias.isChecked()
            val = Dense(units=units, activation=activation, use_bias=useBias)(inp[1])
            val = [inp[0], val]
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.markDescendantsDirty()
            self.evalChildren()
            return val

