package lab.book.service;

import lab.book.model.Book;

import java.util.List;

public interface BookService {

    List<Book> getBooks();

    Book addBook(Book book);
}
