from qtpy.QtWidgets import QLabel
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMessageBox
from src.application.calc_conf import register_node, OP_NODE_OUTPUT_LABEL
from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel("42", self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)


# @register_node(OP_NODE_OUTPUT_LABEL)
class CalcNode_Output(CalcNode):
    icon = "icons/out.png"
    op_code = OP_NODE_OUTPUT_LABEL
    op_title = "输出"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = CalcGraphicsNode(self)

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_node.eval()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return

        # self.content.lbl.setText("%d" % val)
        self.content.lbl.setText(val.__str__())
        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        return val
    def onDoubleClicked(self, event):
        try:
            QMessageBox.about(
                None,
                "详情",
                f"{self.content.lbl.text()}"
            )
        except Exception as e:
            QMessageBox.about(
                None,
                "详情",
                f"{e.__str__()}"
            )
