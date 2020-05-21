FROM python:3.7

RUN mkdir /app

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

ADD . /app/

EXPOSE 5000

CMD ["waitress-serve", "--listen=0.0.0.0:5000", "manage:app"]