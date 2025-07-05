# TTrader.com Flask App

Este projeto é um site Flask com backend Python e frontend integrado, pronto para deploy no Render.com.

## Como rodar localmente:

```bash
pip install -r requirements.txt
python app.py
```

## Para deploy no Render:

- Conecte ao GitHub
- Use o comando de inicialização:

```bash
gunicorn app:app
```
