package lab.book.service;

import lab.book.model.Rating;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Slf4j
public class RatingServiceFallback implements RatingService{
    @Override
    public List<Rating> getRatingsByBookId(int bookId) {
        log.error("fallback action for getRatingByBookId( {} )", bookId);
        return List.of();
    }
}
