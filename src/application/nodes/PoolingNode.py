from qtpy.QtWidgets import QComboBox, QSpinBox
from qtpy.QtWidgets import QVBoxLayout
from keras.layers.pooling import *

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LAYER_POOLING


class LayerPoolingContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.pooling = QComboBox(self)
        self.pooling.addItem("AveragePooling2D")
        self.pooling.addItem("MaxPooling2D")
        self.pooling.addItem("GlobalAveragePooling2D")
        self.pooling.addItem("GlobalMaxPooling2D")

        self.poolSize = QSpinBox()
        self.poolSize.setMinimum(1)
        self.poolSize.setToolTip("池化尺寸")

        self.padding = QComboBox()
        self.padding.addItem("same")
        self.padding.addItem("valid")
        self.padding.addItem("full")
        self.padding.addItem("causal")

        self.strides = QSpinBox()
        self.strides.setMinimum(1)
        self.strides.setToolTip("步长")

        self.verticalBox.addWidget(self.pooling)
        self.verticalBox.addWidget(self.poolSize)
        self.verticalBox.addWidget(self.padding)
        self.verticalBox.addWidget(self.strides)
        self.setLayout(self.verticalBox)

    def serialize(self):
        res = super().serialize()
        res['pooling'] = self.pooling.currentIndex()
        res['poolSize'] = self.poolSize.value()
        res['padding'] = self.padding.currentIndex()
        res['strides'] = self.strides.value()
        return res

    def deserialize(self, data, hashmap = {}):
        res = super().deserialize(data, hashmap)
        try:
            self.pooling.setCurrentIndex(data['pooling'])
            self.poolSize.setValue(data['poolSize'])
            self.padding.setCurrentIndex(data['padding'])
            self.strides.setValue(data['strides'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_LAYER_POOLING)
class LayerPoolingNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LAYER_POOLING
    op_title = "池化层"
    content_objname = "layer_pooling"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = LayerPoolingContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.height += 74
        self.grNode.height += 52 * 2
        self.content.pooling.currentIndexChanged.connect(self.onInputChanged)
        self.content.poolSize.textChanged.connect(self.onInputChanged)
        self.content.padding.currentIndexChanged.connect(self.onInputChanged)
        self.content.strides.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None
        inp = inp.eval()
        pooling = self.content.pooling.currentText()
        poolSize = self.content.poolSize.value()
        padding = self.content.padding.currentText()
        strides = self.content.strides.value()

        if self.content.pooling.currentIndex() == 0:
            value = AveragePooling2D(poolSize, strides, padding)(inp[1])
        elif self.content.pooling.currentIndex() == 1:
            value = MaxPooling2D(poolSize, strides, padding)(inp[1])
        elif self.content.pooling.currentIndex() == 2:
            value = GlobalAveragePooling2D()(inp[1])
        else:
            value = GlobalMaxPooling2D()(inp[1])
        value = [inp[0], value]
        self.value = value

        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return self.value

