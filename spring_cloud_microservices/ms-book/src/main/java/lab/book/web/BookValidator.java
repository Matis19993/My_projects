package lab.book.web;

import lab.book.model.Book;
import lab.book.model.Publisher;
import lab.book.service.PublisherService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.validation.Errors;
import org.springframework.validation.Validator;

@Component
@RequiredArgsConstructor
@Slf4j
public class BookValidator implements Validator {

    public final PublisherService publisherService;

    @Override
    public boolean supports(Class<?> clazz) {
        return clazz.isAssignableFrom(Book.class);
    }

    @Override
    public void validate(Object target, Errors errors) {
        Book book = (Book) target;
        Publisher publisher = publisherService.getPublisherById(book.getPublisherId());
        if(publisher==null){
            errors.rejectValue("publisherId", "book.error.publisher.missing");
        }
    }
}
