FROM adoptopenjdk/openjdk11:alpine-jre

COPY target/ms-publisher-1.0.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]