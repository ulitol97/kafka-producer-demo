# kafka-producer-demo
Containerized Kafka producer endlessly producing data for testing and demoing of consumer apps
The project consists on:
- A python script using Kafka's python package to endlessly produce data
- A modified Docker image already prepared with a producer and ready to produce data on launch

## Running the demo

1. Tweak `producer.py` to fit your data needs (it is programmed to produce data that serves my use case)
2. Build a Docker image using the project's `Dockerfile` and run it
3. Enjoy an endless Kafka stream in the configured host and port



## Why this project
I was involved in a project requiring validation of persistent data streams, but I needed some data producers to begin testing and deployment!

Instead of hardcoding my way through, I though of preparing a customizable Docker image that can serve anyone's needs.

## Behind the scenes
The resulting project is a compendium of different techniques from different sources,
especial thanks go to:
- [Dario Radečić](https://betterdatascience.com/author/dario/) and his awesome blog posts for installing Kafka and creating a simple producer
- [@hey-johnnypark](https://github.com/hey-johnnypark) for implementing a Docker image containing both Kafka and Zookeper altogether, removing the hassle of setting up a docker-compose setup. 
  * This image was modified with the provided environment variables to generate [my own kafka-zookeper image](https://hub.docker.com/r/ulitol97/kafka-zookeeper) with:
    - Apache Kafka `3.1.0` (latest release as of now)
    - Apache Zookeper `3.7.0` (latest release in the stable branch as of now)
  * The image itself can be found in [hey-johnnypark/docker-kafka-zookeeper](https://github.com/hey-johnnypark/docker-kafka-zookeeper), the main idea coming from Spotify's deprecated [spotify/docker-kafka](https://github.com/spotify/docker-kafka)
