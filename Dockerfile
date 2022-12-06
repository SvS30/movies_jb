# https://hub.docker.com/layers/python/library/python/3.6-alpine/images/sha256-ada5fee6b97267270f36b8744b5a16dd058206fdf5776bec3bf58e5a83d65049?context=explore
FROM python:3.6-alpine

ENV MoviesHome=/home/app/movies

# Show the Python shell
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR $MoviesHome
COPY . .

# Install the dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]