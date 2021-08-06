#Build stage.
FROM maven:3.8.1-openjdk-11-slim AS builder
WORKDIR /app
COPY pom.xml .
# Resolve Dependencies
RUN mvn -e -B dependency:resolve
COPY src ./src
# Build and compile application
RUN mvn clean -e -B package

# Run stage
FROM openjdk:11-jre-slim
WORKDIR /app

# Copy final Jar file from the builder stage
COPY --from=builder /app/target/dotenv_Java-1.0-jar-with-dependencies.jar .
# update PATH environment variable
ENV USERNAME=DOCKER_CONTAINER

ENTRYPOINT ["java", "-jar", "./dotenv_Java-1.0-jar-with-dependencies.jar"]
CMD ["-ric", "/EUR="]