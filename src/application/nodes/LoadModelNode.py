from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QPushButton
from keras.models import load_model

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_LOAD_MODEL


class LoadModelNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.load = QPushButton("加载模型", self)
        self.load.setObjectName(self.node.content_objname)


@register_node(OP_NODE_LOAD_MODEL)
class LoadModelNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_LOAD_MODEL
    op_title = "加载模型"
    content_objname = "load_model_node"
    model = None

    def __init__(self, scene):
        super().__init__(scene, inputs=[])
        self.eval()

    def initInnerClasses(self):
        self.content = LoadModelNodeContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.load.clicked.connect(self.onLoad)

    def evalImplementation(self):
        if self.model is None:
            self.value = None
            self.markDirty()
            return
        self.value = [self.model, self.model]
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return self.value

    def onLoad(self):
        directory = QFileDialog.getExistingDirectory(
            None,
            "请选择模型文件夹",
            "./"
        )
        try:
            self.model = load_model(directory)
        except Exception as e:
            dumpException(e)
            return
        self.onInputChanged()
