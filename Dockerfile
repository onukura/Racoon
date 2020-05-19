FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
RUN python manage.py init_db
EXPOSE 5000