# Text Style Paraphraser: Code Implementation Description

## Problem Definition

The task is to transfer the style of a text while preserving its meaning. Existing models often alter the meaning of the original sentence.

## Proposed Solution

Reformulate the problem as a paraphrase generation task.

## Method: STRAP (Style Transfer via Paraphrasing)

STRAP is an unsupervised style transfer method that models the task as a controlled paraphrase generation problem. It requires no parallel data between different styles and proceeds in three simple stages:

1.  Create pseudo-parallel data by feeding sentences from different styles through a diverse paraphrase model.
2.  Train style-specific inverse paraphrase models that convert these paraphrased sentences back into the original stylized sentences.
3.  Use the inverse paraphraser for a desired style to perform style transfer.

## Step-by-Step Details

1.  **Creating Pseudo-Parallel Data:**
    *   The goal is to normalize input sentences by stripping away information that is predictive of its original style.
    *   For every sentence x from style i (x ∈ X_i), generate a paraphrase z using a pre-trained paraphrase model f_para:
        *   `z = f_para(x)` where `x ∈ X_i`
    *   This results in a dataset Z_i of normalized sentences and allows us to form a pseudo-parallel corpus (X_i, Z_i) between each original sentence and its paraphrased version.
    *   **Implementation:**
        *   The diverse paraphraser `f_para` is implemented using a fine-tuned GPT-2 model. See `style_paraphrase/inference_utils.py` (GPT2Generator class).
            *   The `GPT2Generator` class initializes with a `model_path`, loads training arguments from `model_path/training_args.bin`, and sets up the GPT-2 model and tokenizer using `init_gpt2_model` from `style_paraphrase/utils.py`.
        *   The data filtering process to promote diversity is implemented in `datasets/prepare_paraphrase_data.py`.
            *   This script takes a TSV file of sentence pairs as input and applies several filtering steps based on content similarity, lexical diversity, and syntactic diversity.
            *   The filtering thresholds (e.g., minimum similarity score, maximum unigram overlap) are defined as command-line arguments.
    *   **Data Source:** Filtered ParaNMT-50M corpus.
        *   The ParaNMT-50M corpus is a large corpus of back-translated text.
        *   The filtering process reduces the corpus size significantly (from 50M to ~75k sentence pairs) but improves the quality and diversity of the paraphrases.

2.  **Training the "Inverse Paraphrase" Model:**
    *   The goal is to train a style-specific model that attempts to reconstruct the original sentence x given its paraphrase z.
    *   The inverse paraphrase model f_inv_i for style i learns to reconstruct the original corpus X_i using the standard language modeling objective with cross-entropy loss L_CE:
        *   `x_hat = f_inv_i(z)` where `z ∈ Z_i`
        *   `loss = Σ x∈X_i L_CE(x, x_hat)`
    *   **Implementation:**
        *   The inverse paraphrase models are implemented using fine-tuned GPT-2 models. See `style_paraphrase/run_lm_finetuning.py`.
            *   The `load_and_cache_examples` function loads the training data and tokenizes it using the GPT-2 tokenizer.
            *   The `train` function performs the fine-tuning process.
        *   The `GPT2ParentModule` class in `style_paraphrase/utils.py` defines the forward pass and loss calculation.
            *   The `forward` method takes a batch of data as input and calculates the cross-entropy loss between the predicted tokens and the target tokens.
    *   **Fine-tuning:**
        *   The GPT-2 models are fine-tuned using a small learning rate (e.g., 5e-5) and the Adam optimizer.
            *   The `AdamW` optimizer is used with a weight decay fix.
        *   Early stopping is used based on validation set perplexity.
            *   The `evaluate` function calculates the perplexity on the validation set.
        *   The training process is defined in the `train` function in `style_paraphrase/run_lm_finetuning.py`.
            *   The training loop iterates over the training data in batches.
            *   For each batch, the model calculates the loss and updates the model parameters using backpropagation.
            *   Gradient clipping is used to prevent exploding gradients.

3.  **Style Transfer:**
    *   Given an arbitrary sentence s (in any particular style), convert it to a sentence s_j in target style j using a two-step process of style normalization with f_para followed by stylization with the inverse paraphraser f_inv_j:
        *   `s_j = f_inv_j(f_para(s))`
    *   **Implementation:**
        *   The `GPT2Generator` class in `style_paraphrase/inference_utils.py` implements the style transfer process.
        *   The `generate` method calls the diverse paraphraser and the appropriate inverse paraphrase model.
            *   The `generate` method first tokenizes the input sentence using the GPT-2 tokenizer.
            *   It then calls the `generate` method of the `GPT2ParentModule` class to generate the paraphrased sentence.
            *   The generated tokens are then detokenized to produce the final output sentence.
        *   The `sample_sequence` function in `style_paraphrase/utils.py` implements the sampling process.
        *   The `beam_search` function in `style_paraphrase/utils.py` implements the beam search process.

## Evaluation

*   Use metrics to evaluate the quality of the style transfer, including:
    *   Accuracy: Measures the success rate of style transfer.
    *   Similarity: Measures the semantic similarity between the original and transferred sentences.
    *   Fluency: Measures the fluency and naturalness of the transferred sentence.
*   Propose a new evaluation method that combines the above metrics at the sentence level (sentence-level aggregation) for a more comprehensive evaluation.
*   Use a new dataset (CDS) with 15 million sentences and 11 different styles to evaluate the model.

## Code Implementation Details

Here's how the key formulas are implemented in code:

*   **Top-k and Top-p filtering:** Implemented in the `top_k_top_p_filtering` function in `style_paraphrase/utils.py`.
    *   Input: `logits` (logits distribution), `top_k`, `top_p`.
    *   If `top_p > 0`:
        *   Sort logits and calculate cumulative probability:
            ```python
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
            ```
        *   Identify tokens to remove:
            ```python
            sorted_indices_to_remove = cumulative_probs > top_p
            ```
        *   Remove tokens:
            ```python
            indices_to_remove = sorted_indices_to_remove.scatter(dim=1, index=sorted_indices, src=sorted_indices_to_remove)
            logits[indices_to_remove] = filter_value
            ```
    *   If `top_k > 0`:
        *   Identify tokens to remove:
            ```python
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            ```
        *   Remove tokens:
            ```python
            logits[indices_to_remove] = filter_value
            ```
*   **Sampling sequence:** Implemented in the `sample_sequence` function in `style_paraphrase/utils.py`.
    *   Uses the `get_logits` function to get logits for the next token.
    *   Applies `top_k_top_p_filtering` to the logits.
    *   Samples the next token using `torch.multinomial`.
*   **Beam search:** Implemented in the `beam_search` function in `style_paraphrase/utils.py`.
    *   Uses the `get_logits` function to get logits for the next token.
    *   Selects the `beam_size` best tokens.
    *   Continues expanding the beam until the maximum length is reached or the end-of-sequence token is encountered.

## Summary

This method improves the ability to preserve meaning during text style transfer and achieves good results on various datasets.
