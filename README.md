# evo

This repository contains a minimal evolutionary optimization engine with an example domain plug-in for SQL queries. It includes unit tests and a small demo script.

## Local setup

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pytest -q  # run tests
```

## Docker usage

A `Dockerfile` is provided to run the project inside a container. Build the image and run the example:

```bash
docker build -t evo:latest .
docker run --rm evo:latest
```

The default command executes `main.py`, which performs a short evolution cycle and prints the best SQL query.

## Deploying to RunPod

1. Build and push the Docker image to a registry (e.g. Docker Hub):

   ```bash
   docker build -t <username>/evo:latest .
   docker push <username>/evo:latest
   ```

2. In the RunPod dashboard, create a new pod using the **Custom Image** option.
3. Enter the image tag you pushed (`<username>/evo:latest`) and set the container command to `python main.py` (or your own script).
4. Launch the pod. Logs will show the output from the evolution demo.

This setup works for CPU pods. For GPU pods you can select a GPU-enabled base image and adjust the Dockerfile accordingly.
