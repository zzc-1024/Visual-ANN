from qtpy.QtWidgets import QPushButton
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QMessageBox
from keras.utils import plot_model

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_SHOW_MODEL


class ShowModelNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.verticalBox = QVBoxLayout()
        self.showSummary = QPushButton("模型摘要")
        self.showGraph = QPushButton("模型图结构")
        self.verticalBox.addWidget(self.showSummary)
        self.verticalBox.addWidget(self.showGraph)
        self.setLayout(self.verticalBox)


global summary


@register_node(OP_NODE_SHOW_MODEL)
class ShowModelNode(CalcNode):
    icon = "icons/out.png"
    op_code = OP_NODE_SHOW_MODEL
    op_title = "展示"
    content_objname = "show_model_node"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[])
        self.eval()

    def initInnerClasses(self):
        self.content = ShowModelNodeContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.grNode.width = 180
        self.grNode.height += 74
        self.content.showSummary.clicked.connect(self.onShowSummary)
        self.content.showGraph.clicked.connect(self.onShowGraph)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return

        inp = inp.eval()

        if inp is None:
            self.markInvalid()
            return

        self.value = inp
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return self.value

    def onShowSummary(self):
        global summary
        summary = ""
        def getSummary(s):
            global summary
            summary += s + '\n'

        self.value[1].summary(print_fn=getSummary)
        QMessageBox.about(None, "摘要", summary)

    def onShowGraph(self):
        try:
            plot_model(
                self.value[1],
                "tmp.png",
                show_shapes=True
            )
            QMessageBox.about(
                None,
                "图结构",
                "<img src=\"tmp.png\">"
            )
        except Exception as e:
            dumpException(e)

    def onDoubleClicked(self, event):
        try:
            QMessageBox.about(
                None,
                "详情",
                f"{self.value}"
            )
        except Exception as e:
            QMessageBox.about(
                None,
                "详情",
                f"{e.__str__()}"
            )