# medtextcollector
Scripts for the collection of free online medical texts and definitions

## Dependencies
The list of dependencies can be found under requirements.txt. You can use pip to automatically install all of these requirements:

```
pip install -r requirements.txt
```

## Getting started
Make sure that the data directory is present and contains the input folder with positive and unlabeled (i.e. "negative") samples as configured in configuration.json.

Run the medtextcollector_pipeline in order to train the models:
```
python medtextcollector_pipeline.py
```

You can also specify a configuration file which isn't located in the default location (i.e. ./configuration.json) using:

```
python medtextcollector_pipeline.py -c path/to/alternative/configuration.json
```

After making sure that a classifier has been trained and configuring the crawler using configuration.json, you can start it using:
```
python crawler.py
```

You can always interrupt the crawler using CTRL+C. This will cause it to save its current state to the filesystem and to exit afterwards. The extracted documents and the state of the crawler will be stored in the output folder specified in configuration.json.

The crawler can also be started with a non default configuration file using the "-c" parameter.

```
python crawler.py -c path/to/alternative/configuration.json 
```

## Crawler results
Medical documents: /media/data/medtextcollector/data/output/crawler/pages (and /media/data/medtextcollector/data/output/crawler/pages/raw for the original html pages)

## Wikipedia
### Download a wiki dump
In order to train an initial classifier you need one or more db dumps of wikipedia in the language you'd like to crawl. 
**Make sure that you have around 20GB of free disk space bevore you download the complete German article dump!**

1. go to [https://dumps.wikimedia.org/dewiki/] and download one are all dumps of the articles. They start with `dewiki-latest-pages-articles[numberOfDump].xml...` and end with `.bz2`. 
2. create a folder `data` in your git repo and add this folder to your `.gitignore`
3. extract the `bz2` dump in your data folder with the command `bzip2 -dk`
