package lab.book.service.impl;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import lab.book.model.Publisher;
import lab.book.service.PublisherService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

//@Service
@RequiredArgsConstructor
@Slf4j
public class PublisherServiceBean implements PublisherService {

    private final RestTemplate restTemplate;

    @CircuitBreaker(name = "ms-publisher-cb", fallbackMethod = "getPublisherByIdFallback")
    @Override
    public Publisher getPublisherById(int publisherId) {
        log.info("Fetching publisher {}", publisherId);

        String publisherServiceUrl = "http://ms-publisher";
        log.info("connecting to ms-publisher service: {}", publisherServiceUrl);

        ResponseEntity<Publisher> responseEntity = restTemplate.exchange(
                publisherServiceUrl + "/publishers/" + publisherId,
                HttpMethod.GET,
                HttpEntity.EMPTY,
                Publisher.class
        );
        return responseEntity.getBody();
    }

    private Publisher getPublisherByIdFallback(int publisherId, Throwable t){
        log.error("error while fetching publisher " + publisherId, t);
        //throw new MsBookException("exception while fetching publisher", t);
        return null;
    }
}