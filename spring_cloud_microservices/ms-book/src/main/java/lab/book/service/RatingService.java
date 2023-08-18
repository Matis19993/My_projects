package lab.book.service;

import lab.book.model.Rating;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;

@FeignClient(name="ms-rating", fallback = RatingServiceFallback.class)
public interface RatingService {

    @GetMapping("/books/{id}/ratings")
    List<Rating> getRatingsByBookId(@PathVariable("id") int bookId);

}
