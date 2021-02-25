FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]