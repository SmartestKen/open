import tensorflow as tf

class BertModel():
	def __init__(self, config, input_data):
		self.config = config
		self.config["is_training"] = False
		input_shape = input_data.shape.as_list()
		batch_size = input_shape[0]
		seq_length = input_shape[1]


# find embedding
# get output, [-1] gives the output








	



