FROM python:3.7-alpine
WORKDIR /vc

COPY ./vc /vc

COPY ./requirements-dev.txt requirements.txt
COPY ./main.py main.py

RUN pip install -r requirements.txt

COPY ./vc /vc
COPY ./main.py /main.py
ENV PYTHONPATH=/vc
CMD ["python", "main.py"]
