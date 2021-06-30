# `MultiSubs` Evaluation Toolkit

By [Josiah Wang](http://www.josiahwang.com)


## Introduction 

This repository contains the libraries and scripts used for evaluating the fill-in-the-blank task and the lexical translation task derived from the `MultiSubs` dataset. Details of the dataset, task and evaluation metrics/setup can be found in our paper [`MultiSubs`: A Large-scale Multimodal and Multilingual Dataset](https://arxiv.org/abs/2103.01910).


The `MultiSubs` dataset is [available for download on Zenodo](https://doi.org/10.5281/zenodo.5034604).



## Using the toolkit

The toolkit is a set of Python modules located in the ``multisubs/`` directory. Please refer to the doc comments in the code for explanations and usage.

Example evaluation scripts demonstrating the usage for the two tasks are available as ``eval_fill_in_the_blank.py`` and ``eval_lexical_translation.py`` respectively.

Some example predictions for the two tasks are available in the ``sample_predictions/`` directory.



## Dependencies

The toolkit requires ``python>=3.8`` and ``gensim``. You can install the required dependencies with ``pip install -r requirements.txt``.

You will also need the JSON files from the [`MultiSubs` dataset](https://doi.org/10.5281/zenodo.5034604).

You will also need the pre-trained word2vec binary file (`GoogleNews-vectors-negative300.bin`) for computing word similarity scores. You should be able to obtain this from [the word2vec webpage](https://code.google.com/archive/p/word2vec/).



## Toolkit API

### ``multisubs.blank``

Module for evaluating the fill-in-the-blank task.


#### ``FillInTheBlankGroundTruthLoader``

Utility class for loading the ground truth of the fill-in-the-blank task from the `MultiSubs` dataset for evaluation.

##### ``load_from_json()`` method

Load the list of ground truth words from the `sents.json` file of the `MultiSubs` dataset. Please check the docstrings in the code for the documentation.


#### ``FillInTheBlankEvaluator``

Utility class for evaluating the fill-in-the-blank task. Provide the path to the Word2Vec binary (``GoogleNews-vectors-negative300.bin``) as an argument to the constructor to be able to compute the word similarity scores.

##### ``compute_accuracy()`` method

Compute the accuracy score for the fill in the blank task. Please check the docstrings in the code for the documentation.


##### ``compute_word_similarity()`` method

Compute the semantic word similarity score for the fill in the blank task. You must provide the path to the Word2Vec binary in the constructor of FillInTheBlankEvaluator to use this method. Please check the docstrings in the code for the documentation.


### ``multisubs.translation``

Module for evaluating the lexical translation task.


#### ``LexicalTranslationGroundTruthLoader``

Utility class for loading the ground truth of the lexical translation task from the `MultiSubs` dataset for evaluation.


##### ``load_from_json()`` method

Load list of ground truth source words, target words, positive target words, and negative target words from the json files of the `MultiSubs` dataset. Please check the docstrings in the code for the documentation.


#### ``LexicalTranslationEvaluator``

Utility class for evaluating the lexical translation task. 

##### ``compute_ali()`` method

Compute the Ambiguous Lexical Index (ALI) score for the lexical translation task, as introduced in the paper. Please [refer to the paper](https://arxiv.org/abs/2103.01910) for a detailed description of the metric. Please check the docstrings in the code for the documentation for this method.



## Citation

Please cite the following paper if you use this evaluation toolkit:

Josiah Wang, Pranava Madhyastha, Josiel Figueiredo, Chiraag Lala, Lucia Specia (2021). **MultiSubs: A Large-scale Multimodal and Multilingual Dataset**. CoRR, abs/2103.01910. Available at: https://arxiv.org/abs/2103.01910

```bibtex
@article{DBLP:journals/corr/abs-2103-01910,
  author    = {Josiah Wang and
               Pranava Madhyastha and
               Josiel Figueiredo and
               Chiraag Lala and
               Lucia Specia},
  title     = {MultiSubs: {A} Large-scale Multimodal and Multilingual Dataset},
  journal   = {CoRR},
  volume    = {abs/2103.01910},
  year      = {2021},
  url       = {https://arxiv.org/abs/2103.01910},
  archivePrefix = {arXiv},
  eprint    = {2103.01910},
  timestamp = {Thu, 04 Mar 2021 17:00:40 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2103-01910.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```


## License for the toolkit

GNU General Public License v3.0

