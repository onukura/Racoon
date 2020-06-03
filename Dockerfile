FROM python:3.7

# Requirements have to be pulled and installed here to use cache
RUN mkdir /requirements
COPY ./requirements/ /requirements/
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r /requirements/develop.txt

COPY ./wait-for-it.sh /wait-for-it.sh
RUN sed -i 's/\r//' /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN mkdir /app
ADD . /app/
WORKDIR /app