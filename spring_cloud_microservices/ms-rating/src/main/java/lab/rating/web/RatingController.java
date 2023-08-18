package lab.rating.web;

import lab.rating.data.RatingRepository;
import lab.rating.model.Rating;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
@Slf4j
public class RatingController {

    private final RatingRepository repository;
    @GetMapping("/ratings")
    List<Rating> getRatings(){
        log.info("retrieve ratings");
        return repository.findAll();
    }

    @GetMapping("/ratings/{id}")
    Rating getRatingById(@PathVariable("id") int id){
        log.info("retrieve rating by id {}",id);
        return repository.findById(id).orElse(null);
    }

    @GetMapping("/books/{id}/ratings")
    List<Rating> getRatingsByBookId(@PathVariable("id") int bookId){
        log.info("retrieving rating for a book {}", bookId);
        return repository.findAllByBookId(bookId);
    }
}
