# Tiny Chess Engine

A minimal UCI-compatible chess engine in ~3200 bytes of Python.

## Features
- 0x88 board representation
- Alpha-beta search with quiescence
- MVV-LVA move ordering
- Piece-square tables (pawns, knights, bishops)
- Promotion handling

## Usage
```bash
python3 main.py
```
Set `MAKEFUN_ENV_URL=1` for auto-play demo.

## License
MIT (see LICENSE)