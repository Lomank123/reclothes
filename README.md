# reclothes
Clothes shop

The goal is to use everything I've learned so far to create real e-commerce shop. So in this project most of best practices (from previous experiences) have been implied.


## Fixtures

### Content

There are 2 fixture files:
- `dev.json` - everything for testing except user groups.
- `groups.json` - main user groups which must be added **before** running the server.

### Useful commands:

- To **dump**:

```
python3 manage.py dumpdata auth --natural-foreign --natural-primary -e auth.Permission --indent 2 > fixtures/groups.json
python3 manage.py dumpdata accounts carts catalogue orders payment --natural-foreign --natural-primary --indent 2 > fixtures/dev.json
```

- To **load**:

```
python3 manage.py loaddata fixtures/groups.json
python3 manage.py loaddata fixtures/dev.json
```
