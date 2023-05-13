from src.application.calc_conf import register_node, OP_NODE_OP_ADD, OP_NODE_OP_SUB, OP_NODE_OP_MUL, OP_NODE_OP_DIV
from src.application.calc_node_base import CalcNode


# @register_node(OP_NODE_OP_ADD)
class CalcNode_Add(CalcNode):
    icon = "icons/add.png"
    op_code = OP_NODE_OP_ADD
    op_title = "加法"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def evalOperation(self, input1, input2):
        return input1 + input2


# @register_node(OP_NODE_OP_SUB)
class CalcNode_Sub(CalcNode):
    icon = "icons/sub.png"
    op_code = OP_NODE_OP_SUB
    op_title = "减法"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def evalOperation(self, input1, input2):
        return input1 - input2

# @register_node(OP_NODE_OP_MUL)
class CalcNode_Mul(CalcNode):
    icon = "icons/mul.png"
    op_code = OP_NODE_OP_MUL
    op_title = "乘法"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def evalOperation(self, input1, input2):
        return input1 * input2

# @register_node(OP_NODE_OP_DIV)
class CalcNode_Div(CalcNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_OP_DIV
    op_title = "除法"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def evalOperation(self, input1, input2):
        return input1 / input2

# way how to register by function call
# register_node_now(OP_NODE_ADD, CalcNode_Add)