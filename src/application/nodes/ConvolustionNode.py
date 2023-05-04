from qtpy.QtWidgets import QSpinBox, QComboBox
from qtpy.QtWidgets import QVBoxLayout
from keras.layers import Conv2D

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_CONVOLUTION


class LayerConvolutionContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.filters = QSpinBox()
        self.filters.setMinimum(1)
        self.kernelSize = QSpinBox()
        self.kernelSize.setMinimum(1)
        self.strides = QSpinBox()
        self.strides.setMinimum(1)
        self.padding = QComboBox()
        self.padding.addItem("same")
        self.padding.addItem("valid")
        self.padding.addItem("full")
        self.padding.addItem("causal")
        self.verticalBox.addWidget(self.filters)
        self.verticalBox.addWidget(self.kernelSize)
        self.verticalBox.addWidget(self.strides)
        self.verticalBox.addWidget(self.padding)
        self.setLayout(self.verticalBox)

    def serialize(self):
        res = super().serialize()
        res['filters'] = self.filters.value()
        res['kernelSize'] = self.kernelSize.value()
        res['strides'] = self.strides.value()
        res['padding'] = self.padding.currentIndex()
        return res

    def deserialize(self, data, hashmap = {}):
        res = super().deserialize(data, hashmap)
        try:
            self.filters.setValue(data['filters'])
            self.kernelSize.setValue(data['kernelSize'])
            self.strides.setValue(data['strides'])
            self.padding.setCurrentIndex(data['padding'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_LAYER_CONVOLUTION)
class LayerConvolutionNode(CalcNode):
    icon = "icons/dot"
    op_code = OP_NODE_LAYER_CONVOLUTION
    op_title = "卷积层"
    content_objname = "layer_convolution"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = LayerConvolutionContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.height += 74
        self.grNode.height += 52 * 2
        self.content.filters.textChanged.connect(self.onInputChanged)
        self.content.kernelSize.textChanged.connect(self.onInputChanged)
        self.content.strides.textChanged.connect(self.onInputChanged)
        self.content.padding.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None
        inp = inp.eval()
        filters = self.content.filters.value()
        kernelSize = self.content.kernelSize.value()
        strides = self.content.strides.value()
        padding = self.content.padding.currentText()
        value = Conv2D(
            filters,
            kernelSize,
            strides,
            padding
        )(inp[1])
        value = [inp[0], value]
        self.value = value
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return value
