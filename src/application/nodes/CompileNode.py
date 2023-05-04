# 有待改进
# 提供个性化参数
# 提供可变数量的指标选择
from qtpy.QtWidgets import QComboBox
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QCheckBox
from keras.models.cloning import clone_model
from keras import losses
from keras import optimizers
from keras import metrics

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_COMPILE


class CompileNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.loss = QComboBox()
        self.loss.addItem("MeanSquaredError")
        self.loss.addItem("MeanAbsoluteError")
        self.loss.addItem("MeanAbsolutePercentageError")
        self.loss.addItem("MeanSquaredLogarithmicError")
        self.loss.addItem("BinaryFocalCrossentropy")
        self.loss.addItem("CategoricalCrossentropy")
        self.loss.addItem("SparseCategoricalCrossentropy")
        self.loss.addItem("Hinge")
        self.loss.addItem("SquaredHinge")
        self.loss.addItem("CategoricalHinge")
        self.loss.addItem("Poisson")
        self.loss.addItem("LogCosh")
        self.loss.addItem("KLDivergence")
        self.loss.addItem("Huber")
        self.loss.addItem("CosineSimilarity")

        self.optimizer = QComboBox()
        self.optimizer.addItem("adadelta")
        self.optimizer.addItem("adagrad")
        self.optimizer.addItem("adam")
        self.optimizer.addItem("adamax")
        self.optimizer.addItem("experimentaladadelta")
        self.optimizer.addItem("experimentaladagrad")
        self.optimizer.addItem("experimentaladam")
        self.optimizer.addItem("experimentalsgd")
        self.optimizer.addItem("nadam")
        self.optimizer.addItem("rmsprop")
        self.optimizer.addItem("sgd")
        self.optimizer.addItem("ftrl")
        # 报错，可能是还需要提供一些参数吧
        # self.optimizer.addItem("lossscaleoptimizer")
        # self.optimizer.addItem("lossscaleoptimizerv3")
        # self.optimizer.addItem("lossscaleoptimizerv1")

        self.verticalBox.addWidget(self.loss)
        self.verticalBox.addWidget(self.optimizer)
        self.setLayout(self.verticalBox)

    def serialize(self):
        res = super().serialize()
        res['loss'] = self.loss.currentIndex()
        res['optimizer'] = self.optimizer.currentIndex()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.loss.setCurrentIndex(data['loss'])
            self.optimizer.setCurrentIndex(data['optimizer'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_COMPILE)
class CompileNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_COMPILE
    op_title = "编译"
    content_objname = "compile_node"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = CompileNodeContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 200
        self.grNode.height += 74
        self.content.loss.currentIndexChanged.connect(self.onInputChanged)
        self.content.optimizer.currentIndexChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None
        else:
            inp = inp.eval()
            loss = self.content.loss.currentText()
            optimizer = self.content.optimizer.currentText()
            value = clone_model(inp[1])
            value.compile(
                loss=losses.get(loss),
                optimizer=optimizers.get(optimizer),
                metrics=[
                    # 先用着get吧，后面得改
                    # 这个地方需要更多的可选指标
                    metrics.get('acc')
                ]
            )
            value = [inp[0], value]
            self.value = value
            self.markDirty(False)
            self.markInvalid(False)
            self.markDescendantsDirty()
            self.evalChildren()
            return value
