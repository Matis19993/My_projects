package lab.book.service.impl;

import lab.book.data.BookRepository;
import lab.book.model.Book;
import lab.book.model.Rating;
import lab.book.service.BookService;
import lab.book.service.RatingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.OptionalDouble;

@Service
@RequiredArgsConstructor
@Slf4j
public class BookServiceBean implements BookService {

    private final BookRepository repository;
    private final RatingService ratingService;

    @Override
    public List<Book> getBooks() {
        List<Book> books = repository.findAll();
        books.forEach(this::calculateAverageRating);
        return books;
    }

    @Override
    public Book addBook(Book book) {
        return repository.save(book);
    }

    private void calculateAverageRating(Book book){
        List<Rating> ratings = ratingService.getRatingsByBookId(book.getId());
        OptionalDouble average = ratings.stream().mapToInt(rating->rating.getRate()).average();
        book.setAverageRating(average.orElse(0));
    }
}
