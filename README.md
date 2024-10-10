# Don’t Stop Believin’ - A Unified Evaluation Approach for LLM Honeypots

This repository contains the annotation framework, dataset and code used for the research paper [*"Don’t Stop Believin’ - A Unified Evaluation Approach for LLM Honeypots"*](https://ieeexplore.ieee.org/document/10703029)

**Table of Contents:**

- [Repository Layout](#repository-layout)
- [Findings](#findings)
- [Licensing](#licensing)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Repository Layout

1. [annotations](./annotations): Expert-annotated data on request-response pairs. 
2. [code](./code): The main codebase for generating LLM-based responses, and performing evaluations. 
	1. [notebooks](./code/notebooks): Jupyter notebooks for interactive exploration and analysis of the datasets and results. 
	2. [scripts](./code/scripts): The script for response generation.
3. [data](./data): Holds the dataset samples used for the evaluation. 

## Findings

#### Dataset and Sample Distributions

				Dataset    Source    Commands    Unique Base-Commands
				Prague    Original      226               67
				Prague     Sample       129               49
				NL2Bash   Original   12,607              226
				NL2Bash    Sample       334              183
				Halle     Original    2,483               85
				Halle      Sample       943               59
				Total     Original   15,316              251
				Total      Sample     1,406              230

#### Dataset Convincing Responses (%)

				Dataset    Convincing(%)
				Prague        64.34
				Halle         54.93
				NL2Bash       40.12
				Overall       52.28

#### Inter-Annotator Agreement
				Dataset           Krippendorff’s Alpha (%)
				Halle                    63.46
				NL2Bash                  43.90
				Prague                   40.71
				Overall                  57.38

#### Transition Probabilities of session state 

				p(s + 1|s)       Non-Convincing     Convincing
				Non-Convincing       49.04%           50.96%
				Convincing           40.41%           59.59%


The findings underscore the current limitations of LLM-based honeypots and propose potential solutions such as paraphrase-mining to enhance evaluation metrics. 
The macro F1 values  for each model are as follows:

- all-MiniLM-L6-v2: 77.85%
- bert-base-uncased: 75.36%
- distilbert-base-uncased: 75.15%
- roberta-base: 67.96%

## Licensing

This work is licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 License](https://creativecommons.org/licenses/by-nc-nd/4.0/). 

## Contact
Please contact:
 [Simon.Weber@hhu.de](mailto:Simon.Weber@hhu.de) or [marc.feger@uni-duesseldorf.de](mailto:marc.feger@uni-duesseldorf.de)

## Acknowledgements

We would like to thank Benedikt Michaelis, Henning Ullrich, Eric Schüler and Stefan Stein for their contributions to the
annotation process in this paper.
