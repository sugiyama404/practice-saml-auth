FROM python:3.13

WORKDIR /app

# xmlsec1の依存関係をインストール
RUN apt-get update && \
    apt-get install -y \
    libxml2-dev libxmlsec1-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --force-reinstall --no-binary lxml lxml

COPY . .

CMD ["python", "main.py"]
