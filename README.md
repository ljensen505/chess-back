# Chess API

more details coming soon. Built with python3.11 and fastapi

## Installation

create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

install dependencies

```bash
pip install -r requirements.txt
```

### Usage

```bash
uvicorn main:app --reload
```

### Testing

```bash
pytest
```

or test a specific module

```bash
pytest app
```

```bash
pytest chess
```

### Known Issues

- [ ] En passant
- [ ] deploy to pi
- [ ] castling check not comprehensive
- [ ] add check
- [ ] add checkmate
