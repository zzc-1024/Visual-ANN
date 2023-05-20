LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT_INT = 0x1
OP_NODE_OUTPUT_LABEL = 0x2
OP_NODE_OP_ADD = 0x3
OP_NODE_OP_SUB = 0x4
OP_NODE_OP_MUL = 0x5
OP_NODE_OP_DIV = 0x6

OP_NODE_BASE = 0x40
OP_NODE_LAYER_INPUT = 0x40
OP_NODE_LAYER_DENSE = 0x41
OP_NODE_LAYER_ACTIVATION = 0x42
OP_NODE_LAYER_MODEL = 0x43
OP_NODE_COMPILE = 0x44
OP_NODE_SAVE = 0x45
OP_NODE_LOAD_MODEL = 0x46
OP_NODE_LAYER_CONVOLUTION = 0x47
OP_NODE_LAYER_POOLING = 0x48
OP_NODE_SHOW_MODEL = 0x49
OP_NODE_LAYER_ADD = 0x4a
OP_NODE_LAYER_BATCH_NORMALIZATION = 0x4b
OP_NODE_LAYER_DROPOUT = 0x4c
OP_NODE_LAYER_FLATTEN = 0x4d
OP_NODE_FIT = OP_NODE_BASE + 0xe


CALC_NODES = {
}


class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in CALC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" %(
            op_code, CALC_NODES[op_code]
        ))
    CALC_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in CALC_NODES: raise OpCodeNotRegistered("操作码 '%d' 未被注册" % op_code)
    return CALC_NODES[op_code]



# import all nodes and register them
from src.application.nodes import *