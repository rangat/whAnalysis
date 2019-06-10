# WH Question Analysis

whAnalysis is a project for tagging clauseType and questType to analyze for frequencies.

The linguistic work which brought this project to life was presented at [XPRAG](https://www.xprag.de/?page_id=6207) on June 13th, 2019.

See more about our motivations behind this project [here](INTRO.md)

## Usage

### Installation

To use our tagger, we recommend you install simply using git clone

```bash
git clone https://github.com/rangat/whAnalysis.git
```

### Run

To run our tagger, run the command below. It will create a new file in your current directory with the tagged json.

```bash
python tagger.py relative/dir/to/data.json
```

### Data format

We've included a few really easy functions to convert corpora to our data format in the **corpus_handlers/** directory. The best example is our [bnc](corpus_handlers/bnc.py) handler.

The data must be in a .json file. The file must be a list of JSON objects which must include a new object for each sentence and a key ```"sentence"``` with the value of the sentence included. The JSON objects must be in a list for the tagger to work.

```javascript
[
    {
        "sentence": "Why did I need to include this json as a part of my readme?"
    },
    {
        "sentence": "It's helpful to have examples to follow!"
    }
]
```

### Dependencies

This project is designed and developed entirely in python with the use of

* [Python](https://www.python.org/) - Python Version **3.5** or greater
* [NLTK](https://www.nltk.org/) - The Natural Language Toolkit
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python scraping and parse tree processing library
* [JSON](https://docs.python.org/3/library/json.html) - Python json library
* [Multiprocessing](https://docs.python.org/3.7/library/multiprocessing.html) - Python multiprocessing library

## Authors and acknowledgment

* [**Rangaraj Tirumala**](http://www.rangarajt.com/) - *Current Work*
* [**Morgan Moyer**](http://www.rci.rutgers.edu/~mcm315/) - *Linguistic Guidance*
* [**Divya Appasamy**](https://github.com/divsquid) - *Current Work*
* [**Knyckolas Sutherland**](https://github.com/sutherland17) - *Initial work*

## License

GNU General Public License v3.0

See [COPYING](COPYING) for the full text
