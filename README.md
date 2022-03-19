# kafka-producer-demo
Containerized Kafka producer endlessly producing data for testing and demoing of consumer apps
The project consists on:
- A python script using Kafka's python package to endlessly produce data
- A modified Docker image already prepared with a producer and ready to produce data on launch

## Running the demo

1. Tweak `producer.py` to fit your data needs (it is programmed to produce data that serves my use case)
2. Build a Docker image using the project's `Dockerfile` (or [pull](https://hub.docker.com/r/ulitol97/kafka-producer))
3. Run your image in a new container: `docker run --name kafka-producer -d -p 2181:2181 -p 9092:9092 kafka-producer:tag`
4. Enjoy an endless Kafka stream in the configured host and port

### Tweaking the image
The following environment variables can be used to modify app containers:
- `TOPIC_NAME`: the name of the topic that will be constantly streaming messages from the container (default to `test-topic`)

Additionally, the following can be used to change Kafka's base behaviour (see them [here](https://github.com/ulitol97/kafka-producer-demo/blob/ec91b3a889d3ed2decf0e5fcabf6df21df56f31f/kafka-zookeeper/assets/scripts/start-kafka.sh#L3)):
- `ADVERTISED_HOST`: the external ip for the container (default is `localhost`)
- `ADVERTISED_PORT`: the external port for Kafka (default is `9092`)
- `ZK_CHROOT`: the zookeeper chroot that's used by Kafka (without / prefix), e.g. "kafka"
- `LOG_RETENTION_HOURS`: the minimum age of a log file in hours to be eligible for deletion
- `LOG_RETENTION_MINUTES`: the minimum age of a log file in minutes to be eligible for deletion (superseedes LOG_RETENTION_HOURS if defined) (default is `15`)
- `LOG_RETENTION_BYTES`: configure the size at which segments are pruned from the log (default is `20971520`, for 20MB)
- `NUM_PARTITIONS`: configure the default number of log partitions per topic (default is `1`)
- `AUTO_CREATE_TOPICS`: whether a new topic should be created when a non existent topic is written to (default is `true`)



### The base image
As explained in [_Behind the scenes_](#behind-the-scenes), the demo itself relies on a custom image running Kafka and Zookeeper altogether. You are free to build your own derived images from its [Dockerfile](https://github.com/ulitol97/kafka-producer-demo/blob/main/kafka-zookeeper/Dockerfile), although for most changes overriding one of this build arguments shall do the trick:
- `KAFKA_VERSION`: Kafka version to be downloaded and installed
- `ZOOKEEPER_VERSION`: Zookeeper version to be downloaded and installed. Download links are slighly different since 3.5, so downgrading below that won't work without adapting the Dockerfile
- `SCALA_VERSION`: Scala version, should remain 2.13 for a while for new Kafka versions

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
