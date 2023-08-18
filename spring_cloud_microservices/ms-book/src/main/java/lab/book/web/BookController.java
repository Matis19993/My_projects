package lab.book.web;

import lab.book.data.BookRepository;
import lab.book.model.Book;
import lab.book.service.BookService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.Errors;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@Slf4j
@RefreshScope
public class BookController {

    private final BookService bookService;
    private final BookRepository repository;
    private final BookValidator validator;

    @Value("${log.prefix}")
    private String logPrefix;

    @InitBinder
    void initBinder(WebDataBinder binder){
        binder.setValidator(validator);
    }

    @GetMapping("/books")
    List<Book> getBooks() {
        log.info("[" + logPrefix + "] retrieving books");
        return bookService.getBooks();
    }

    @GetMapping("/books/{id}")
    Book getBook(@PathVariable("id") int id){
        log.info("[" + logPrefix + "] retrieving book {}", id);
        return repository.findById(id).orElse(null);
    }


    @PostMapping("/books")
    ResponseEntity<Book> addBook(@RequestBody @Validated Book book, Errors errors) {
        log.info("[" + logPrefix + "] about to add new book {}", book);
        boolean valid = !errors.hasErrors();

        if (valid) {
            book = bookService.addBook(book);
            return ResponseEntity.status(HttpStatus.CREATED).body(book);
        } else {
            return ResponseEntity.badRequest().build();
        }
    }


}
