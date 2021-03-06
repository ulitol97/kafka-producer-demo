# Image running Kafka and Zookeeper altogether
# Inspired in https://github.com/hey-johnnypark/docker-kafka-zookeeper
# Adapted to Java 17, lastest Kafka/Zookeper, Alpine Linux 3.15 and the new naming scheme of Zookeper download links
FROM alpine:3.15

RUN apk add --update openjdk17-jre supervisor bash gcompat

ARG ZOOKEEPER_VERSION=3.7.0
ENV ZOOKEEPER_HOME /opt/apache-zookeeper-"$ZOOKEEPER_VERSION"-bin

# Download and extract Zookeeper. Cleanup downloaded files.
RUN wget -q https://archive.apache.org/dist/zookeeper/zookeeper-"$ZOOKEEPER_VERSION"/apache-zookeeper-"$ZOOKEEPER_VERSION"-bin.tar.gz -O /tmp/zookeeper-"$ZOOKEEPER_VERSION".tgz
RUN ls -l /tmp/zookeeper-"$ZOOKEEPER_VERSION".tgz
RUN tar xfz /tmp/zookeeper-"$ZOOKEEPER_VERSION".tgz -C /opt && rm /tmp/zookeeper-"$ZOOKEEPER_VERSION".tgz
ADD assets/conf/zoo.cfg $ZOOKEEPER_HOME/conf

ARG SCALA_VERSION=2.13
ARG KAFKA_VERSION=3.1.0

# Combine scala version and Kafka version to reference our Kafka
ENV KAFKA_FULL_VERSION_NAME kafka_${SCALA_VERSION}-${KAFKA_VERSION}

# Download and extract Kafka. Cleanup downloaded files.
ENV KAFKA_HOME /opt/"$KAFKA_FULL_VERSION_NAME"
ENV KAFKA_DOWNLOAD_URL https://archive.apache.org/dist/kafka/"$KAFKA_VERSION"/"$KAFKA_FULL_VERSION_NAME".tgz
RUN wget -q $KAFKA_DOWNLOAD_URL -O /tmp/"$KAFKA_FULL_VERSION_NAME".tgz
RUN tar xfz /tmp/"$KAFKA_FULL_VERSION_NAME".tgz -C /opt && rm /tmp/"$KAFKA_FULL_VERSION_NAME".tgz

# Scripts for stating Kafka/Zookeper. Use additional ENV variables to configure Kafka.
ADD assets/scripts/start-kafka.sh /usr/bin/start-kafka.sh
ADD assets/scripts/start-zookeeper.sh /usr/bin/start-zookeeper.sh

# Supervisor config
ADD assets/supervisor/kafka.ini assets/supervisor/zookeeper.ini /etc/supervisor.d/

# 2181 is zookeeper, 9092 is kafka
EXPOSE 2181 9092

# Set the default ENV variables for my use case (overridable by containers and derived images)
# Public IP of the Kafka cluster, defaults to localhost for internal usage (PORT is always 9092)
ENV ADVERTISED_HOST localhost
# 15 minutes before messagges are eligible for deletion
ENV LOG_RETENTION_MINUTES 15
# 20MB before pruning the log
ENV LOG_RETENTION_BYTES 20971520
# Single partition for new topics
ENV NUM_PARTITIONS 1
# Creates a topic when a message is produced to a topic that does not exist, makes testing more agile
ENV AUTO_CREATE_TOPICS true

# Set ENV vars with the build argument for future use in containers/derived images
ENV ZOOKEEPER_VERSION $ZOOKEEPER_VERSION
ENV SCALA_VERSION $SCALA_VERSION
ENV KAFKA_VERSION $KAFKA_VERSION

CMD ["supervisord", "-n"]
