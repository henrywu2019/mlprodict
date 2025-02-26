"""
@file
@brief Optimisation of :epkg:`ONNX` graphs.
"""
from onnx.helper import make_graph
from ._onnx_optimisation_common import (  # pylint: disable=E0611
    _rename_node_input,
    _rename_node_output,
    _apply_optimisation_on_graph,
    _apply_remove_node_fct_node
)


def onnx_remove_node_identity(onnx_model, recursive=True, debug_info=None, **options):
    """
    Removes as many *Identity* nodes as possible.
    The function looks into every node and subgraphs if
    *recursive* is True for identity node. Unless such a
    node directy connects one input to one output, it will
    be removed and every other node gets its inputs or
    outputs accordingly renamed.

    @param      onnx_model      onnx model
    @param      recursive       looks into subgraphs
    @param      debug_info      debug information (private)
    @param      options         additional options (unused)
    @return                     new onnx _model
    """
    if debug_info is None:
        debug_info = [str(type(onnx_model)).rsplit(
            '.', maxsplit=1)[-1].strip("'>")]
    else:
        debug_info = (debug_info +
                      [str(type(onnx_model)).rsplit('.', maxsplit=1)[-1].strip("'>")])

    if hasattr(onnx_model, 'graph'):
        return _apply_optimisation_on_graph(
            onnx_remove_node_identity, onnx_model,
            recursive=recursive, debug_info=debug_info, **options)

    graph = onnx_model

    inputs = set(i.name for i in graph.input)
    outputs = set(o.name for o in graph.output)

    def retrieve_idnodes(graph, existing_nodes):
        idnodes = []
        for i, exnode in enumerate(existing_nodes):
            if exnode is None:
                continue
            if exnode.op_type == 'Identity':
                input = exnode.input[0]
                output = exnode.output[0]
                idnodes.append((i, exnode, input, output))
        return idnodes

    nodes = list(graph.node)
    rem = 1
    while rem > 0:
        rem = 0
        idnodes = retrieve_idnodes(graph, nodes)
        restart = False
        for i, _, inp, out in idnodes:
            if restart:
                break  # pragma: no cover
            if nodes[i] is None:
                # Already removed.
                continue  # pragma: no cover
            if inp in inputs and out in outputs:
                # Cannot be removed.
                continue
            if not restart and out not in outputs:
                # We cannot change an output name.
                for j in range(len(nodes)):  # pylint: disable=C0200
                    if nodes[j] is None:
                        continue
                    if out in nodes[j].input:
                        nodes[j] = _rename_node_input(nodes[j], out, inp)
                        rem += 1
                        if nodes[j].op_type == 'Identity':
                            restart = True  # pragma: no cover
                nodes[i] = None
                rem += 1
                continue
            if not restart and inp not in inputs and inp not in outputs:
                # We cannot change an input name or an output name.
                for j in range(len(nodes)):  # pylint: disable=C0200
                    if nodes[j] is None:
                        continue
                    if inp in nodes[j].output:
                        nodes[j] = _rename_node_output(nodes[j], inp, out)
                        rem += 1
                        if nodes[j].op_type == 'Identity':
                            restart = True  # pragma: no cover
                    if inp in nodes[j].input:
                        nodes[j] = _rename_node_input(nodes[j], inp, out)
                        rem += 1
                        if nodes[j].op_type == 'Identity':
                            restart = True
                nodes[i] = None
                rem += 1

    if recursive:
        # Handles subgraphs.
        for i in range(len(nodes)):  # pylint: disable=C0200
            node = nodes[i]
            if node is None or not (node.attribute):  # pylint: disable=C0325
                continue
            nodes[i] = _apply_remove_node_fct_node(
                onnx_remove_node_identity,
                node, recursive=True, debug_info=debug_info + [node.name])

    # Finally create the new graph.
    nodes = list(filter(lambda n: n is not None, nodes))
    graph = make_graph(nodes, onnx_model.name,
                       onnx_model.input, onnx_model.output,
                       onnx_model.initializer)

    graph.value_info.extend(onnx_model.value_info)  # pylint: disable=E1101
    return graph
