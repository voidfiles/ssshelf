FROM python:3.6

WORKDIR /code

RUN pip install Cython

ADD ./test_requirements.txt /code

RUN pip install -r test_requirements.txt

ADD ./requirements.txt /code

RUN pip install -r requirements.txt

COPY . /code
