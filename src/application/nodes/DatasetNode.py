from qtpy.QtWidgets import QComboBox, QPushButton, QLabel
from qtpy.QtWidgets import QVBoxLayout
from keras.datasets import mnist, cifar10, cifar100

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_DATASET


class DatasetContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.setLayout(self.verticalBox)

        self.dataset = QComboBox()
        self.dataset.addItem("mnist")
        self.dataset.addItem("cifar10")
        self.dataset.addItem("cifar100")
        self.verticalBox.addWidget(self.dataset)

        self.button = QPushButton("加载数据集")
        self.verticalBox.addWidget(self.button)

        self.status = QLabel("未加载")
        self.verticalBox.addWidget(self.status)

        self.selection = QLabel("未选数据集")
        self.verticalBox.addWidget(self.selection)

    def serialize(self):
        res = super().serialize()
        res['dataset'] = self.dataset.currentIndex()
        return res

    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        res = super().deserialize(data, hashmap)
        try:
            self.dataset.setCurrentIndex(data['dataset'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_DATASET)
class DatasetNode(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_DATASET
    op_title = "加载数据集"
    content_objname = "dataset_node"

    train = None
    test = None

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = DatasetContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 200
        self.grNode.height += 74
        self.grNode.height += 52 * 2

        self.content.button.clicked.connect(self.onLoadDataset)

    def onLoadDataset(self):
        (x_train, y_train), (x_test, y_test) = tuple(), tuple()
        string = self.content.dataset.currentText()
        if string == "mnist":
            (x_train, y_train), (x_test, y_test) = mnist.load_data()
        elif string == "cifar10":
            (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        elif string == "cifar100":
            (x_train, y_train), (x_test, y_test) = cifar100.load_data()
        self.train = (x_train, y_train)
        self.test  = (x_test,  y_test )

        self.content.status.setText("已加载")
        self.content.selection.setText(string)
        self.value = self.train

        self.onInputChanged()

    def evalImplementation(self):
        if self.train is None:
            return None

        self.value = self.train
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.evalChildren()

        return self.value
