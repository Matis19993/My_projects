package lab.book.service.impl;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import lab.book.model.Rating;
import lab.book.service.RatingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

//@Service
@RequiredArgsConstructor
@Slf4j
public class RatingServiceBean implements RatingService {

    private final RestTemplate restTemplate;

    @CircuitBreaker(name = "ms-rating-cb", fallbackMethod = "getRatingByBookIdFallback")
    @Override
    public List<Rating> getRatingsByBookId(int bookId) {
        log.info("about to fetch ratings of a book {}", bookId);


        String ratingServiceUrl = "http://ms-rating";
        log.info("connecting to ms-rating instance: {}", ratingServiceUrl);


        log.info("fetching ratings for a book {}", bookId);
        return List.of(restTemplate.exchange(
                ratingServiceUrl + "/books/" + bookId + "/ratings",
                HttpMethod.GET,
                HttpEntity.EMPTY,
                Rating[].class
        ).getBody());


    }

    private List<Rating> getRatingByBookIdFallback(int bookId, Throwable t) {
        log.error("error while fetching rating for a book " + bookId, t);
        //throw new MsBookException("exception while fetching ratings", t);
        return List.of();
    }
}
