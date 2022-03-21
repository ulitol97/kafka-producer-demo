# Image running Kafka and Zookeeper altogether,
# with an endless producer for testing
FROM ulitol97/kafka-zookeeper:dev

# Set topic name
ENV TOPIC_NAME test-topic

# Create the topic via kafka-scripts
RUN $KAFKA_HOME/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic $TOPIC_NAME

# Install python/pip and python's kafka package
RUN apk add --update py3-pip && pip install kafka-python

# Copy the producer script into the machine /scripts
WORKDIR /scripts
COPY producer.py .

# Non-priviledged user to run the app "kafka-user"
RUN addgroup --system kafka-user && adduser --system --shell /bin/false --ingroup kafka-user kafka-user
RUN chown -R kafka-user:kafka-user /scripts
USER kafka-user

# 2181 is zookeeper, 9092 is kafka
EXPOSE 2181 9092

# Run the producer script in workdir, passing in the target topic
CMD python3 producer.py $TOPIC_NAME