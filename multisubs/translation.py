# -*- coding: utf-8 -*-

"""
Author: Josiah Wang (http://www.josiahwang.com)

Lexical TranslationGroundTruthLoader: utility to load ground truth data from the fill in the blank json files.

LexicalTranslationEvaluator: Utility to compute the ALI score for evaluating the lexical translation task
"""

import json
import statistics

from collections import defaultdict


class LexicalTranslationGroundTruthLoader:
	""" Utility to load the ground truth for the lexical translation task from the dataset
	"""
	def __init__(self):
		pass
	
	def load_from_json(self, dataset_json_filepath, split_json_filepath, split_label, dict_json_filepath):
		""" Load list of ground truth source words, target words, positive target words, and negative target words from the json files of the dataset.
		
		Parameters
		----------
		dataset_json_filepath : str
			Path to json file of the dataset ("en-es.sents.json").
		split_json_filepath : str
			Path to json file containing test split info ("en-es.splits.json")
		split_label : str
			The label for the split to use (e.g. "testSubset", "test", "train", "val", "valSubset")
		dict_json_filepath : str
			Path to json file containing the mapping from a word in the source language to all possible translations in the target language ("en-es.dict.json")
		
		Returns
		-------
		tuple: 4 elements
			src_list: List of ground truth source words for the desired split
			trg_list: List of ground truth target words for the desired split
			positive_trg_list: List of possible correct target words per instance for the desired split
			negative_trg_list: List of bad target words per instance for the desired split
		"""
		
		dataset = json.load(open(dataset_json_filepath, encoding="utf-8"))
		split = json.load(open(split_json_filepath))
		indices_list = set(split[split_label])
		translation_dict = json.load(open(dict_json_filepath, encoding="utf-8"))
		src_list = [] # source word list
		trg_list = [] # target word list
		positive_trg_list = [] # list of all set of positive target words
		negative_trg_list = [] # list of all set of negative target words
		
		# load ground truth for selected instances
		for i, entry in enumerate(dataset):
			if i in indices_list:
				src_word = entry["word"].lower()
				src_list.append(src_word)

				trg_word = entry["target"].lower()
				trg_list.append(trg_word)

				# get set of positive target words for this instance
				positive_trgs = set(entry["positiveTargets"])
				positive_trg_list.append(positive_trgs)
				
				# get set of negative target words for this instance
				negative_trgs = set(translation_dict.get(src_word, [])) - positive_trgs
				negative_trg_list.append(negative_trgs)
		
		return (src_list, trg_list, positive_trg_list, negative_trg_list)


class LexicalTranslationEvaluator:
	""" Evaluator for the lexical translation task
	"""
	def __init__(self):
		pass
	
	def compute_ali(self, goldSourceWordList, predictedTargetWordList, positiveTargetWordSetList, negativeTargetWordSetList):
		""" Evaluates lexical translation using the Ambiguous Lexical Index (ALI) for each test instance

		Parameters
		----------
		goldSourceWordList : list of str
			List of ground truth source words for each instance. Assumes words are case normalised.
		predictedTargetWordList : list of str
			List of predicted target words for each instance. Assumes words are case normalised.
		positiveTargetWordSetList : list of set of str
			List of all possible correct words for each instance
		negativeTargetWordSetList : list of set of str
			List of all possible negative words for each instance

		Returns
		-------
		score : float
			Average ALI score across all source words
		aliDict : dict
			For each source word, average ALI score across all instances
			dict[sourceWord] = {"mean": avg, "scores": {idxInGoldSourceWordList: score, idx: score, ...}}
		"""

		assert len(goldSourceWordList) == len(predictedTargetWordList) == len(positiveTargetWordSetList) == len(negativeTargetWordSetList)

		scoreDict = defaultdict(dict) # scoresDict[srcWord] = {idx: score, idx: score}

		# get ALI score per instance, aggregate over source words
		for i, (src, tgt, positiveSet, negativeSet) in enumerate(zip(goldSourceWordList, predictedTargetWordList, positiveTargetWordSetList, negativeTargetWordSetList)):
			if tgt in positiveSet:
				score = 1
			elif tgt in negativeSet:
				score = -1
			else:
				score = 0
			scoreDict[src][i] = score

		# compute mean ALI score per word
		aliDict = {} # aliDict[srcWord] = {"mean": avg, "scores": {idx: score, idx: score}
		aliScores = []
		for (key, val) in scoreDict.items():
			aliDict[key] = {}
			aliDict[key]["scores"] = val
			aliDict[key]["mean"] = statistics.mean([score for (k, score) in val.items()])
			aliScores.append(aliDict[key]["mean"])

		# compute overall average ALI score
		ali = statistics.mean(aliScores)
		return (ali, aliDict)


def test_lexical_translation():
	# Example usage
	
	# ground truth src words
	src = ["seal", "seal", "seal", "bank"]
	
	# predicted target words
	pred = ["selo", "selo", "rubbish", "banc"]
	
	# ground truth target words
	# there can be multiple correct answers per instance
	posSetList = [set(["selo","sello"]),
				set(["foca"]),
				set(["selo","sello"]),
				set(["banco","banc"])]
	
	# ground truth bad target words
	# ALI will penalise you for predicting bad target words
	negSetList = [set(["foca","stamp"]),
					set(["selo","sello","stamp"]),
					set(["foca","stamp"]),
					set(["riverb","seaside"])]
	
	# setup evaluator
	evaluator = LexicalTranslationEvaluator()
	
	# compute ALI
	(ali, aliDict) = evaluator.compute_ali(src, pred, posSetList, negSetList)
	
	# print results
	print(ali)
	print(aliDict)
	

if __name__ == "__main__":
	test_lexical_translation()

