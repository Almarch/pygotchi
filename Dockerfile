FROM python:3.10

RUN pip install --upgrade pip
RUN pip install --no-cache-dir build

WORKDIR /app
COPY . /app/pygotchi

RUN python -m build /app/pygotchi
RUN pip install --no-cache-dir /app/pygotchi

EXPOSE 80
CMD ["python", "-m", "pygotchi", "0.0.0.0", "80"]
