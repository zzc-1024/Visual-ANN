import sys
from threading import Thread

from qtpy.QtWidgets import QPushButton, QLabel, QSpinBox, QDoubleSpinBox
from qtpy.QtWidgets import QHBoxLayout, QVBoxLayout
from qtpy.QtWidgets import QDialog

from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException

from src.application.calc_node_base import CalcNode, CalcGraphicsNode
from src.application.calc_conf import register_node
from src.application.calc_conf import OP_NODE_FIT


class FitNodeContent(QDMNodeContentWidget):
    def initUI(self):
        # 注意，这里是水平布局
        self.horizonBox = QVBoxLayout()
        self.setLayout(self.horizonBox)

        self.fit = QPushButton("开始训练")
        self.horizonBox.addWidget(self.fit)

        self.batchSize = QSpinBox()
        self.batchSize.setToolTip("每批大小")
        self.batchSize.setMinimum(1)
        self.batchSize.setMaximum(2147483647)
        self.horizonBox.addWidget(self.batchSize)

        self.epochs = QSpinBox()
        self.epochs.setToolTip("训练次数")
        self.epochs.setMinimum(1)
        self.epochs.setMaximum(2147483647)
        self.horizonBox.addWidget(self.epochs)

        self.validation = QDoubleSpinBox()
        self.validation.setToolTip("验证集比例")
        self.validation.setMinimum(0.0)
        self.validation.setMaximum(1.0)
        self.validation.setSingleStep(0.1)
        self.horizonBox.addWidget(self.validation)

    def serialize(self):
        res = super().serialize()
        res['batchSize'] = self.batchSize.value()
        res['epochs'] = self.epochs.value()
        res['validation'] = self.validation.value()
        return res

    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True):
        res = super().deserialize(data, hashmap)
        try:
            self.batchSize.setValue(data['batchSize'])
            self.epochs.setValue(data['epochs'])
            self.validation.setValue(data['validation'])
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_FIT)
class FitNode(CalcNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_FIT
    op_title = "训练"
    content_objname = "fit_node"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2, 2], outputs=[])
        self.eval()

    def initInnerClasses(self):
        self.content = FitNodeContent(self)
        self.grNode = CalcGraphicsNode(self)

    def onTrain(self):
        if self.isDirty() or self.isInvalid():
            return
        dataset = self.getInput(1)
        if dataset is None:
            return
        dataset = dataset.eval()
        try:
            if len(dataset) != 2:
                return
        except Exception as e:
            dumpException(e)
        if self.value[1] is None:
            return

        class trainThread(Thread):
            def __init__(self, model, x_label, y_label, batchSize, epochs, validation):
                super().__init__()
                self.model = model
                self.x_label = x_label
                self.y_label = y_label
                self.batchSize = batchSize
                self.epochs = epochs
                self.validation = validation

            def run(self) -> None:
                self.model.fit(
                    self.x_label,
                    self.y_label,
                    batch_size=self.batchSize,
                    epochs=self.epochs,
                    validation=self.validation
                )

        class Dialog(QDialog):
            def __init__(self, model, x_label, y_label, batchSize, epochs, validation, parent=None):
                super(Dialog, self).__init__(parent)
                thread = trainThread(
                    model,
                    x_label,
                    y_label,
                    batchSize,
                    epochs,
                    validation
                )
                self.initUI()
                thread.start()

            def initUI(self):
                self.verticalBox = QVBoxLayout()
                self.setLayout(self.verticalBox)

                self.label = QLabel("训练中，请稍后")
                self.verticalBox.addWidget(self.label)

                self.button = QPushButton("关闭")
                self.verticalBox.addWidget(self.button)
                self.button.clicked.connect(self.close)

        dialog = Dialog(
            self.value[1],
            dataset[0],
            dataset[1],
            self.content.batchSize,
            self.content.epochs,
            self.content.validation
        )
        dialog.exec()


    def evalImplementation(self):
        inp = self.getInput()

        if inp is None:
            self.markDirty()
            self.markInvalid()
            return None

        inp = inp.eval()
        self.value = inp
        self.markDirty(False)
        self.markInvalid(False)
        self.markDescendantsDirty()
        self.evalChildren()
        return inp
