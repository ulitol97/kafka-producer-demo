# Image running Kafka and Zookeeper altogether,
# with an endless producer for testing
FROM ulitol97/kafka-zookeeper:dev

# 2181 is zookeeper, 9092 is kafka
EXPOSE 2181 9092

# Set topic name
ENV TOPIC_NAME test-topic

# Set wait between messages (millis)
ENV TIME_BETWEEN_MESSAGES 5000

# Install python/pip and python's kafka package
RUN apk add --update py3-pip && pip install kafka-python

# Copy the producer script into the machine /scripts
WORKDIR /scripts
COPY producer.py .

# 1. Start kafka and zookeeper via supervisord (as in parent image)
# 2. Create the kafka destination topic via kafka-scripts
# 3. Run the producer script in workdir, passing in the target topic
CMD supervisord && \
    $KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic $TOPIC_NAME && \
    python3 producer.py $TOPIC_NAME