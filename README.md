# WH Question Analysis

whAnalysis is a project for analyzing sentences to tag for clauseType and questType.

Works with data of any type in our prescribed json data format.

The linguistic work which brought this project to life was presented at [XPRAG](https://www.xprag.de/?page_id=6207) on June, 13th 2019.

## Usage

### Installation

To use our tagger we recommend you install simply using git clone

```bash
git clone https://github.com/rangat/whAnalysis.git
```

### Run

To run our tagger run the command below. It will create a new file in your current directory with the tagged json.

```bash
python tagger.py relative/dir/to/data.json
```

### Data format

We've included a few really easy functions to convert corpora to our data format in the **corpus_handlers/** directory. The best example is our [bnc](corpus_handlers/bnc.py) handler.

Our tagger accepts json files which are placed in a folder named ```unread/``` at the root of this project.

Our JSON data format includes a new object for each sentence and a key ```"sentence"``` with the value of the sentence included. For our continence we also included ```"corpus"``` and ```"medium"``` which are ignored by the tagger. The JSON objects must be in a list for the tagger to work

```javascript
[
    {
        "sentence": "Why did I need to include this json as a part of my readme?"
    },
    {
        "sentence": "It's helpful to have examples to follow!"
        "corpus": "github",
        "medium": "print"
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
