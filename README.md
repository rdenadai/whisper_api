# Whisper AI

Sorry this repo is a mess ...

Please take a look at `whisper_api` dir.

## Running

### Backend API (port 8000)

In the root of the project:
```bash
$ uvicorn whisper_api.app:app
```

### Frontend (port 5000)

Inside the `whisper_api` dir:
```bash
$> bunx --bun vite --port 5000
```
