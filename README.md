# WH Question Analysis

whAnalysis is a project for analyzing sentences to tag for clauseType and questType
Works with data of any type in our perscribed json dataformat

## Built With

This project is designed and developed entirely in python with the use of
* [NLTK](https://www.nltk.org/) - The Natural Language Toolkit

## Usage

To use our tagger we recomend you install simply using git clone

```bash
git clone https://github.com/rangat/whAnalysis.git
```

We've included a few really easy functions to convert corpora to our data format in the **corpus_handlers** directory. The best example is our [bnc](corpus_handlers/bnc.py) handler.

### Dataformat

Our tagger accepts json files which are placed in a folder named ```unread/``` at the root of this project.

Our JSON data format includes a new object for each sentence and a key ```"sentence"``` with the value of the sentence incldued. For our convinenece we also incldued ```"corpus"``` and ```"medium"``` which are ignored by the tagger. The JSON objects must be in a list for the tagger to work

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

## Authors and acknowledgment

* [**Rangaraj Tirumala**](http://www.rangarajt.com/) - *Current Work*
* **Morgan Moyer** - *Linguistic Guidence*
* **Divya Appasamy** - *Current Work*
* **Knyckolas Sutherland** - *Initial work*

## License

GNU General Public License v3.0

See [COPYING](COPYING) for the full text
