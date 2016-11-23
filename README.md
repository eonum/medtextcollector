# medtextcollector
Scripts for the collection of free online medical texts and definitions
## Wikipedia
### Get some data
First of all you need one or more db dumps of wikipedia. We recommend that you don't start start with the English dump of wikipedia, because those are the biggest. Because of this we use the German dumps, they are smaller but not too small.
1. go to [https://dumps.wikimedia.org/dewiki/] and download one are all dumps of the articles. They start with `dewiki-latest-pages-articles[numberOfDump].xml...` and end with `.bz2`. The download will take a couple of minutes depending on the internetconnecion you have.
2. create a folder `data` in your git repot and add this folder to your `.gitignore` (it doesn't make sense to share the wikipedia dumps)
3. extract the `bz2` dump in your data folder with the command `bzip2 -dk`
You have now data to work with!
