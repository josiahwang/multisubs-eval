# -*- coding: utf-8 -*-
"""
Author: Josiah Wang (http://www.josiahwang.com)

Evaluate lexical translation task with the Ambiguous Lexical Index (ALI) metric
"""

from multisubs.translation import LexicalTranslationGroundTruthLoader, LexicalTranslationEvaluator

import json

def read_groundtruth(dataset_json_filepath, indices_list, split_label, dict_json_filepath):
	loader = LexicalTranslationGroundTruthLoader()
	(src_list, trg_list, positive_list, negative_list) = loader.load_from_json(dataset_json_filepath, split_json_filepath, split_label, dict_json_filepath)
	return (src_list, trg_list, positive_list, negative_list)


def read_predictions(prediction_filepath):
	return [line.strip() for line in open(prediction_filepath)]


def evaluate(evaluator, prediction_filepath, src_list, positive_list, negative_list):
	prediction_list = read_predictions(prediction_filepath)
	
	assert len(src_list) == len(prediction_list), \
		f"Number of ground truth words do not match predicted: {len(trg_list)} vs. {len(prediction_list)}"

	ali, ali_dict = evaluator.compute_ali(src_list, prediction_list, positive_list, negative_list)

	print(f"\nEvaluating {prediction_filepath}...")
	print(f"Mean ALI: {ali:.4f}")
	print(f"Sample per-word ALI:")
	count = 0
	for (src_word, instance) in ali_dict.items():
		print(f"{src_word}: {instance['mean']:.2f} ({len(instance['scores'])} instances)")
		count += 1
		if count > 10:
			break

	## dump the detailed results into a json file for inspection (something you should do regularly!)
	#with open(f"{prediction_filepath}.eval-ali.json", "w") as outfile:
	#	json.dump({"score": ali, "words": ali_dict}, outfile)

if __name__ == "__main__":
	dataset_json_filepath = f"en-fr.sents.json"
	split_json_filepath = f"en-fr.splits.json"
	split_label = "testSubset"
	dict_json_filepath = f"en-fr.dict.json"

	print("Setting up evaluator...")
	evaluator = LexicalTranslationEvaluator()

	print("Loading dataset...")
	src_list, trg_list, positive_list, negative_list = read_groundtruth(dataset_json_filepath, split_json_filepath, split_label, dict_json_filepath)

	print("Performing predictions...")
	prediction_filepath = "./sample_predictions/lexical_translation/en-fr.mfs.txt"
	evaluate(evaluator, prediction_filepath, src_list, positive_list, negative_list)

