import tensorflow as tf

class BertConfig():
	def __init__(self):
		self.vocab_size = 
		self.hidden_size = 768
		self.num_hidden_layers = 12
		self.num_attention_heads = 12
		self.intermediate_size = 3072
		self.hidden_act = "gelu"
		self.hidden_dropout_prob = 0.1
		self.attention_probs_dropout_prob = 0.1
		self.max_position_embeddings = 512
		self.type_vocab_size = 16
		self.initializer_range = 0.02


class BertModel():
	def __init__(self, config, input_data):
		self.config = config
		self.config["is_training"] = False
		input_shape = input_data.shape.as_list()
		batch_size = input_shape[0]
		seq_length = input_shape[1]


# find embedding
# get output, [-1] gives the output








	



