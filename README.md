## How to get started with dummy data

> Simplified steps (untested and prone to errors)

1. Clone the repository
2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Be sure to have the following environment variables set in your `.env` file. They correspond to the database connection details.

```bash
# .env
DB_NAME=""
DB_USER=""
DB_HOST=""
DB_PWD=""
```

4. Set the `global dummy` variable to `True` in the `main.py` file. Like so:

```python
# main.py
global dummy; dummy = True
```

5. Run the `main.py` file

```bash
python main.py
```
