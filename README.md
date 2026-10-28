# Adversarial Arabic

Tests how well large language models read Arabic text that has been
deliberately distorted. Each obfuscation method changes the text in a
different way: swapping codepoints, stripping dots, adding diacritics,
rewriting roots and patterns, mixing in dialect and so on. Models are then
asked to (a) answer comprehension questions about the distorted text and
(b) restore the original text. The two tasks are sent as separate requests.

## Layout

| Path | Contents |
|---|---|
| `arabic_obfuscator/` | The transforms and the `obfuscate` pipeline that stacks them |
| `obfuscate.py` | CLI: obfuscates a text file and writes the question and restore prompts |
| `run_llm.py` | Sends the prompts to models on OpenRouter and has a judge model grade the replies |
| `score.py` | Scores replies by hand (e.g. answers pasted from a chat app) |
| `data/` | Source texts (`<text>.txt`) and their questions (`<text>.questions.txt` / `.json`) |
| `experiments/<text>/<method>/` | One folder per method: obfuscated text, prompts, replies and scores |
| `results.md` | One summary row per run |
| `output/`, `runs/` | Outputs from earlier runs, made before the `experiments/` layout |

## Setup

Most of the code uses only the Python standard library. The `root` and
`pattern` methods also need [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools)
and its MSA morphology database (Python 3.11+):

```sh
python3.12 -m venv .venv
.venv/bin/pip install --no-deps camel-tools
.venv/bin/pip install cachetools dill pyrsistent six future editdistance \
    emoji regex tqdm requests muddler docopt tabulate
.venv/bin/camel_data -i morphology-db-msa-r13
```

camel-tools is installed with `--no-deps` so that torch and transformers are
left out. Only the neural models need them.

`run_llm.py` needs an OpenRouter key:

```sh
export OPENROUTER_API_KEY="sk-or-..."
```

## Usage

### 1. Obfuscate a text

```sh
python3 obfuscate.py data/akkad.txt --mode dotless --seed 1 --html
python3 obfuscate.py data/akkad.txt --mode dotless,disconnect,tashkeel --seed 1
python3 obfuscate.py data/akkad.txt --mode 3,18 --seed 1          # methods by number
python3 obfuscate.py data/akkad.txt --mode root --target content  # only content words
```

This writes `experiments/<text>/<method>/` containing:

- `<text>.<method>.txt`: the obfuscated text
- `<text>.<method>.prompt.txt`: the text plus the questions from `data/<text>.questions.txt`
- `<text>.<method>.restore-prompt.txt`: a request to restore the original text
- `<text>.<method>.html`: a side-by-side preview (with `--html`)

Options:

- `--rate`: the fraction of words to change
- `--target all|content|function|random`: which words the word-level methods may change
- `--seed`: makes a run reproducible
- per-method settings such as `--kashida-rate 0.5` or `--tashkeel-style stacked`. See `python3 obfuscate.py -h` for all of them.

### 2. Run models and score them

```sh
python3 run_llm.py experiments/akkad/10-dotless/akkad.10-dotless.prompt.txt
python3 run_llm.py experiments/akkad/*/*.prompt.txt \
    --model anthropic/claude-sonnet-5.5,google/gemini-3.8-flash --judge openai/gpt-5.6-terra
```

Replies are saved next to the prompt and reused on later runs unless you
pass `--rerun`. The judge grades every answer as 1, 0.5 or 0. It also gives
the restored text a score out of 10, reported alongside an automatic
character and word similarity score. With `--judge keywords` the judge is
skipped and keyword matching is used instead. Each run adds a row to
`results.md`.

To score replies from a chat app by hand:

```sh
python3 score.py experiments/akkad/2-homoglyph/akkad.2-homoglyph.prompt.txt --model claude-app
```

## Obfuscation methods

Each method has a number, and you can pass the number to `--mode` in place of
the name. Output folders are named after the numbers. Methods marked *lossy*
can't be undone mechanically. The others round-trip through `normalize()`.

| # | Mode | What it does | Lossy |
|---|---|---|---|
| 1 | `zwc` | Inserts invisible zero-width characters | |
| 2 | `homoglyph` | Swaps letters for Persian/Urdu lookalike codepoints | |
| 3 | `root` | Replaces a word's root but keeps its pattern (CAMeL Tools). Styles: `replace`, `permute` | ✓ |
| 4 | `gender` | Breaks gender agreement | ✓ |
| 5 | `number` | Breaks number agreement | ✓ |
| 6 | `order` | Reverses, swaps or shuffles the word order within clauses | ✓ |
| 7 | `layout` | Adds hard line breaks every few words, or mirrors lines with a bidi override | ✓ |
| 8 | `tashkeel` | Floods the text with diacritics. Styles: `random`, `stacked` | |
| 9 | `kashida` | Stretches joins with tatweel | |
| 10 | `dotless` | Strips the dots so that letters share skeletons (rasm) | ✓ |
| 11 | `shuffle` | Shuffles the middle letters of words | ✓ |
| 12 | `arabizi` | Writes letters (or whole words) with Latin letters and digits | ✓ |
| 13 | `presentation` | Converts letters to fixed presentation-form codepoints | |
| 14 | `altglyph` | Uses regional letter variants | ✓ |
| 15 | `dialect` | Replaces MSA words with dialect words | ✓ |
| 16 | `conjunction` | Swaps conjunctions | ✓ |
| 17 | `case` | Gives nouns ambiguous case endings, invented by combining real ones | ✓ |
| 18 | `pattern` | Moves a root to another of its patterns (CAMeL Tools) | ✓ |
| 19 | `blank` | Replaces interior letters with a filler the reader has to fill in | ✓ |
| 20 | `space` | Splits words with a stray space | ✓ |
| 21 | `huruf` | Adds spurious attached particles (و ف ك ب ل) to the start of words | ✓ |
| 22 | `silent` | Adds a random silent letter (with sukun) to the start of words | ✓ |
| 23 | `overlap` | Overlays small letters on the real ones | |
| – | `disconnect` | Breaks letter joins with ZWNJ | |

The alias `both` means `homoglyph,presentation`. Methods are always applied
in a fixed order, whatever order you give them in (see
`arabic_obfuscator/pipeline.py`).

## Results

See [results.md](results.md). In summary, Claude Sonnet 5.5 reads most of the
surface-level distortions without trouble: homoglyphs, presentation forms,
diacritics, kashida, zero-width characters, dotless text and Arabizi. Root
replacement is the strongest attack, scoring 0/10 on `akkad` when it is
applied to content words. Pattern swaps and stacked combinations come next.
With `0-no-text`, the questions are asked without any text, which gives a
baseline for how much the models can guess.
