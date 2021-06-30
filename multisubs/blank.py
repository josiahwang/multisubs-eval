# -*- coding: utf-8 -*-

"""
Author: Josiah Wang (http://www.josiahwang.com/)

Module for evaluting the fill in the blank task. 

FillInTheBlankGroundTruthLoader: utility to load ground truth data from the fill in the blank json files.

FillInTheBlankEvaluator: utility to compute the accuracy and word similarity scores for the fill in the blank task
"""

import json
import numpy as np

from gensim.models import KeyedVectors


class FillInTheBlankGroundTruthLoader:
	""" Utility to load the ground truth for the fill in the blank task from the dataset
	"""
	def __init__(self):
		pass
	
	def load_from_json(self, dataset_json_filepath, split_json_filepath, split_label):
		""" Loads the ground truth words from a json file.
		
		Parameters
		----------
		dataset_json_filepath : str
			Path to json file of the dataset ("sents.json").
		split_json_filepath : str
			Path to json file containing test split info ("splits.json")
		split_label : str
			The label for the split to use (e.g. "testSubset", "test", "train", "val", "valSubset")

		Returns
		-------
		list
			List of ground truth words for the desired split
		"""
		
		dataset = json.load(open(dataset_json_filepath, encoding="utf-8"))
		split = json.load(open(split_json_filepath))
		indices_list = set(split[split_label])
		
		gt = []
		# load ground truth for selected instances
		for i, entry in enumerate(dataset):
			if i in indices_list:
				gt.append(entry["word"].lower())
		
		return gt



class FillInTheBlankEvaluator:
	""" Evaluator for the fill in the blank task
	"""
	def __init__(self, w2v_model_path=None):
		""" Constructor.
		
		Parameters
		----------
		w2v_model_path: str
			File path to word2vec binary file (GoogleNews-vectors-negative300.bin). If not provided, you will not be able to use compute_word_similarity(). You can omit this if you are only computing the accuracy score.
		"""
		if w2v_model_path is not None:
			self.model = KeyedVectors.load_word2vec_format(w2v_model_path, binary=True)
		else:
			self.model = None
	
	
	def compute_accuracy(self, groundtruth_list, prediction_list):
		""" Compute the accuracy given a list of ground truth words and a list of predicted words
		
		Parameters
		----------
		groundtruth_list : list
			List of ground truth words
		prediction_list : list
			List of predicted words
		
		Returns
		-------
		mean_accuracy: float
			the mean accuracy across all instances
		accuracies: list
			accuracies for each instance, ordered by groundtruth_list
		"""

		assert len(groundtruth_list) == len(prediction_list), \
			f"Number of ground truth words do not match predicted: {len(gt_list)} vs. {len(prediction_list)}"

		scores = []
		for (gt, pred) in zip(groundtruth_list, prediction_list):
			if gt == pred:
				scores.append(1.0)
			else:
				scores.append(0.0)

		return (np.mean(scores), scores)

	
	def compute_word_similarity(self, groundtruth_list, prediction_list):
		""" Compute the word similarity score given a list of ground truth words and a list of predicted words
		
		Parameters
		----------
		groundtruth_list : list
			List of ground truth words
		prediction_list : list
			List of predicted words
		w2v_model_path: str
			File path to word2vec binary file (GoogleNews-vectors-negative300.bin)
		
		Returns
		-------
		mean_similarity: float
			the mean word similarity score across all instances
		similarities: list
			word similarity scores for each instance, ordered by groundtruth_list
		"""
		
		if self.model is None:
			raise Exception("Cannot compute word similarity because the word2vec model has not been initialised. Please provide the path to the word2vec binary file using the w2v_model_path argument in the FillInTheBlankEvaluator constructor.")
		
		
		assert len(groundtruth_list) == len(prediction_list), \
			f"Number of ground truth words do not match predicted: {len(gt_list)} vs. {len(prediction_list)}"


		scores = []
		for (gt, pred) in zip(groundtruth_list, prediction_list):
			try:
				score = self.model.similarity(gt, pred)
				scores.append(score)
			except KeyError:
				scores.append(0.0)
			
		return (np.mean(scores), scores)


def test_fill_in_the_blank():
	# Example usage for FillInTheBlankEvaluator
	
	groundtruth_words = ["cat", "dog", "chair", "table"]
	predicted_words = ["cat", "puppy", "sofa", "cow"]
	
	w2v_model_path = "./GoogleNews-vectors-negative300.bin"
	
	print("Initialising FillInTheBlankEvaluator...")
	evaluator = FillInTheBlankEvaluator(w2v_model_path=w2v_model_path)

	print("Computing accuracy...")
	(mean_accuracy, accuracies) = evaluator.compute_accuracy(groundtruth_words, predicted_words)
	print(mean_accuracy)
	print(accuracies)

	print("Computing word similarity...")
	(mean_similarity, similarities) = evaluator.compute_word_similarity(groundtruth_words, predicted_words)
	print(mean_similarity)
	print(similarities)


if __name__ == "__main__":
	test_fill_in_the_blank()
