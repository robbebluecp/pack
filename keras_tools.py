import tensorflow as tf
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io
from pathlib import Path
from absl import logging
import keras
from keras import backend as K
from tensorflow.python.platform import gfile


K.set_learning_phase(0)


def h5_to_pb(input_path, output_path, channels_first=False, output_nodes_prefix=None, output_meta_ckpt=False, save_graph_def=False, quantize=False):
    if str(Path(output_path).parent) == '.':
        output_path = str((Path.cwd() / output_path))

    output_fld = Path(output_path).parent
    output_model_name = Path(output_path).name
    output_model_stem = Path(output_path).stem
    output_model_pbtxt_name = output_model_stem + '.pbtxt'

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if channels_first:
        K.set_image_data_format('channels_first')
    else:
        K.set_image_data_format('channels_last')

    model = keras.models.load_model(input_path)

    # TODO(amirabdi): Support networks with multiple inputs
    orig_output_node_names = [node.op.name for node in model.outputs]
    if output_nodes_prefix:
        num_output = len(orig_output_node_names)
        pred = [None] * num_output
        converted_output_node_names = [None] * num_output

        # Create dummy tf nodes to rename output
        for i in range(num_output):
            converted_output_node_names[i] = '{}{}'.format(
                output_nodes_prefix, i)
            pred[i] = tf.identity(model.outputs[i],
                                  name=converted_output_node_names[i])
    else:
        converted_output_node_names = orig_output_node_names
    logging.info('Converted output node names are: %s',
                 str(converted_output_node_names))

    sess = K.get_session()
    if output_meta_ckpt:
        saver = tf.train.Saver()
        saver.save(sess, str(output_fld / output_model_stem))

    if save_graph_def:
        tf.train.write_graph(sess.graph.as_graph_def(), str(output_fld),
                             output_model_pbtxt_name, as_text=True)
        logging.info('Saved the graph definition in ascii format at %s',
                     str(Path(output_fld) / output_model_pbtxt_name))

    if quantize:
        from tensorflow.tools.graph_transforms import TransformGraph
        transforms = ["quantize_weights", "quantize_nodes"]
        transformed_graph_def = TransformGraph(sess.graph.as_graph_def(), [],
                                               converted_output_node_names,
                                               transforms)
        constant_graph = graph_util.convert_variables_to_constants(
            sess,
            transformed_graph_def,
            converted_output_node_names)
    else:
        constant_graph = graph_util.convert_variables_to_constants(
            sess,
            sess.graph.as_graph_def(),
            converted_output_node_names)

    graph_io.write_graph(constant_graph, str(output_fld), output_model_name,
                         as_text=False)
    logging.info('Saved the freezed graph at %s',
                 str(Path(output_fld) / output_model_name))


def get_log(file):
    model = file
    graph = tf.get_default_graph()
    graph_def = graph.as_graph_def()
    graph_def.ParseFromString(gfile.FastGFile(model, 'rb').read())
    tf.import_graph_def(graph_def, name='graph')
    summaryWriter = tf.summary.FileWriter('log/', graph)
    summaryWriter.close()