#data-sharing-example

# Usage

To import a csv into sqlite:

```
sqlite> create table foo(a, b);
sqlite> .mode csv
sqlite> .import test.csv foo
```

# Acknowledgements

Thank you to [jpwhite3/northwind-SQLite3](https://github.com/jpwhite3/northwind-SQLite3) for `Northwind_large.sqlite`.  See included MIT license.
