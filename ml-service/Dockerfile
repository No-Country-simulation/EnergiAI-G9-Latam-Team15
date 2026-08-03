# EnergiAI — ml-service (servicio de inferencia)
# Construir DESDE LA RAIZ del repo:  docker build -f ml-service/Dockerfile -t energiai-ml .
FROM python:3.12-slim

WORKDIR /app

# 1) Dependencias (capa cacheable). Se respeta la estructura del repo para que
#    las rutas relativas de train.py / inference.py funcionen igual que en local.
COPY ml-service/requirements.txt ./ml-service/requirements.txt
RUN pip install --no-cache-dir -r ml-service/requirements.txt

# 2) Código + dataset
COPY ml-service/inference.py ml-service/train.py ./ml-service/
COPY data/processed/dataset_hibrido_v3.csv ./data/processed/dataset_hibrido_v3.csv

# 3) Entrenar el modelo EN el build -> imagen self-contained con ml-service/models/model.pkl
#    (Alternativa producción: cargar el .pkl desde OCI Object Storage en runtime.)
RUN python ml-service/train.py

# 4) Servir (desde ml-service para que uvicorn encuentre inference.py)
WORKDIR /app/ml-service
EXPOSE 8000
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]
