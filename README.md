# FASoC Datasheet-Scrubber

The FASoC Datasheet Scrubber is a utility that scrubs through large sets of PDF datasheets/documents in order to extract key circuit information. The information gathered is used to build a database of commercial off-the-shelf (COTS) IP that can be used to build larger SoC in the FASoC design. More information [here](https://fasoc.engin.umich.edu/datasheet-scrubber).

### Setup instructions

1. Ensure your machine has the correct python version and all of the python modules required to run through the datasheet scrubber. 
    - Requirements: Anaconda 3 or Python 3.6/3.7 (packages pandas, scipy, matplot, matplotlib, pdfminer.six, pypdf2, request, lxml, tabula-py, sklearn, regex, keras, tensorflow, pdf2image, pillow, pytesseract, numpy, opencv-python, gensim, nltk). Python versions below 3.6 are not supported.
    
1. Ensure you have ssh keys setup for github. Instructions for generating and adding ssh keys can be found [here](https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

1. Clone the Datasheet Scrubber repository
    ```bash
    git clone git@github.com:idea-fasoc/datasheet-scrubber.git
    ``` 

# Database

The FASoC database contains more than 700,000 records of Integrated Circuits (ICs) components collected from [Digikey](https://www.digikey.com/products/ics/en). 
### Database Web Application

In order to access a sample of this collection, visit our [web application](https://fasoc.herokuapp.com/) or proceed [here](https://github.com/idea-fasoc/fasoc-webapp).
### Raw Database
To have access to the entire collection of components, please visit [here](https://github.com/idea-fasoc/datasheet-scrubber/tree/master/src/Database).

# Datasheet-Scrubber
Datasheet scrubber includes three steps of [category recognition](https://github.com/idea-fasoc/datasheet-scrubber/tree/master/src/Category-Recognition), [table extracton](https://github.com/idea-fasoc/datasheet-scrubber/tree/master/src/table_extraction) and text extraction.
### Test
an example of how to use the table extractor can be found [here](https://github.com/idea-fasoc/datasheet-scrubber/tree/master/tests/table_extraction).
