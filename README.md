## How to launch a spider
 - Create a virtualEnv Python3. 
 - Install NEUKOLLN.
 - Launch spider_urls.py.
 - Extract all URLS and put them into a csv file.
 - Add the previous csv file as an input in the second spider spider_parsing.py

<hr>

## Follow this steps

- Launch each spider in different Screen 
``` 
scrapy crawl spider_urls -o spider_urls.csv
scrapy crawl spider_parsing -o spider_parsing.csv

```

- Execute the post_process in Jupyter Notebook 
```
luxeresidence.ipynb

```

- Drop duplicate
```
sort -u -k3,3 -t";" merge_files.csv > merge_file_without_dup.csv

