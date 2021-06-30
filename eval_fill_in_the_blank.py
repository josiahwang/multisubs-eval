# -*- coding: utf-8 -*-
"""
Author: Josiah Wang (http://www.josiahwang.com)

Evaluate fill in the blank task with the accuracy metric (exact match) 
"""

from multisubs.blank import FillInTheBlankGroundTruthLoader, FillInTheBlankEvaluator


def read_groundtruth(dataset_json_filepath, indices_list, split_label="testSubset"):
	loader = FillInTheBlankGroundTruthLoader()
	gt_list = loader.load_from_json(dataset_json_filepath, split_json_filepath, split_label)
	return gt_list


def read_predictions(prediction_filepath):
	return [line.strip() for line in open(prediction_filepath)]


def evaluate(evaluator, prediction_filepath, groundtruth_list):
	prediction_list = read_predictions(prediction_filepath)
	
	assert len(groundtruth_list) == len(prediction_list), \
		f"Number of ground truth words do not match predicted: {len(gt_list)} vs. {len(prediction_list)}"

	mean_accuracy, accuracies = evaluator.compute_accuracy(groundtruth_list, prediction_list)

	mean_similarity, similarities = evaluator.compute_word_similarity(groundtruth_list, prediction_list)
	
	print(f"Mean accuracy: {mean_accuracy:.4f}")
	print(f"Mean word similarity: {mean_similarity:.4f}")


if __name__ == "__main__":
	dataset_json_filepath = "./sents.json"
	split_json_filepath = "./splits.json"
	split_label = "testSubset"
	w2v_model_path = "./GoogleNews-vectors-negative300.bin"

	print("Setting up evaluator...")
	evaluator = FillInTheBlankEvaluator(w2v_model_path)

	print("Loading dataset...")
	groundtruth_list = read_groundtruth(dataset_json_filepath, split_json_filepath, split_label)

	print("Performing predictions...")
	prediction_filepath = "./sample_predictions/fill_in_the_blank/predictions.9gram.txt"
	evaluate(evaluator, prediction_filepath, groundtruth_list)

