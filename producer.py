import datetime
import os
import random
import signal
import sys
import time

from kafka import KafkaProducer

"""Seconds to sleep between messages"""
sleep_time = 5


def handler(signum, frame):
    """Handler for interruptions raised by the user halting the program"""
    print("Interrupted by user")
    exit(1)


# Define behaviour on Ctrl+C
signal.signal(signal.SIGINT, handler)
# Provide graceful shutdown when Docker sends SIGTERM to stop container
signal.signal(signal.SIGTERM, handler)


def get_api_version(env_var="KAFKA_VERSION"):
    """Get Kafka's version from environment and format it as expected by kafka-python"""
    api_version_str = os.environ[env_var].split('.')
    api_version_int = map(lambda x: int(x), api_version_str)
    return tuple(api_version_int)


def get_topic():
    """Get the first program argument as the destination topic"""
    if len(sys.argv) < 2:
        # arg[0] is script name
        # arg[1] is the target topic
        print("No topic defined for the producer")
        exit(5)
    else:
        return sys.argv[1].strip()


def generate_message(arg):
    """Produce data messages: i.e.: TURTLE data mimicking a sensor reading"""
    # https://rdfshape.weso.es/link/16478801915
    # Produce a random temperature in range
    temperature = random.uniform(16.0, 22.5)
    # Produce current time in ISO 8601
    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    new_message = f"""
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix ex:  <http://example.org/> .
    ex:reading a ex:sensorReading ;
          ex:readingDatetime "{current_time}"^^xsd:dateTime ;
          ex:readingTemperature "{temperature:.2f}"^^xsd:decimal ;
          ex:status "OK" .
    """.strip()
    return new_message


if __name__ == "__main__":
    # Get the topic
    topic = get_topic()
    # Create the producer: string-serialized values (most straightforward)
    producer = KafkaProducer(
        # https://stackoverflow.com/a/60096382/9744696
        api_version=get_api_version(),
        bootstrap_servers=['localhost:9092'],  # Running on local machine
        value_serializer=str.encode
    )

    print(f"Sending messages to topic '{topic}'...")
    # Infinite loop - runs until you kill the program
    while True:
        # Generate a message
        msg = generate_message(random.randint(1, 1000))
        # Send it to the target topic
        producer.send(topic, msg)
        # Sleep for a while
        time.sleep(sleep_time)
