# 可以将保存的UI换成QT内置的文件系统的UI
from qtpy.QtWidgets import QLineEdit, QPushButton
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QMessageBox

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_SAVE


class SaveNodeContent(QDMNodeContentWidget):
    def initUI(self):
        # self.verticalBox = QVBoxLayout()
        # self.filename = QLineEdit("filename")
        self.save = QPushButton("保存模型", self)
        # self.verticalBox.addWidget(self.filename)
        # self.verticalBox.addWidget(self.save)
        # self.setLayout(self.verticalBox)


@register_node(OP_NODE_SAVE)
class SaveNode(CalcNode):
    icon = "icons/dot.png"
    op_code = OP_NODE_SAVE
    op_title = "保存"
    content_objname = "save_node"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = SaveNodeContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.save.clicked.connect(self.onSave)

    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return
        self.value = inp.eval()
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return self.value

    def onSave(self):

        if self.isDirty() or self.isInvalid():
            QMessageBox.information(
                None,
                "错误！",
                "该节点无有效输入模型"
            )
            return
        # 使用qt文件系统选择文件夹
        directory = QFileDialog.getExistingDirectory(
            None,
            "请选择要保存模型的文件夹",
            "./"
        )
        if directory == "":
            QMessageBox.information(
                None,
                "错误！",
                "该模型尚未命名"
            )
            return
        try:
            self.value[1].save(directory)
        except Exception as e:
            dumpException(e)
