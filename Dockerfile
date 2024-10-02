FROM python:3.11.3

WORKDIR /workmate_test

COPY main.py .
COPY requirements.txt .
COPY routers ./routers
COPY tests ./tests
COPY db ./db

EXPOSE 8000
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pytest
RUN python main.py

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]