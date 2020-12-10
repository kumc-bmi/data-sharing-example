#data-sharing-example

# Usage

To import a csv into sqlite:

```
sqlite> create table foo(a, b);
sqlite> .mode csv
sqlite> .import test.csv foo
```

# Acknowledgements

Thank you to people.sc.fsu.edu for the example data, and [this stackoverflow post on sqlite basics](https://stackoverflow.com/questions/14947916/import-csv-to-sqlite#24582022).
