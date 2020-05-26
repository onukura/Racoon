FROM python:3.7

RUN mkdir /app

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

ADD . /app/

RUN sed -i 's/\r//' /app/wait-for-it.sh