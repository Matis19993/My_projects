package lab.cart.service;

import lab.cart.model.Item;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Slf4j
@Service
public class BookService {

    @Autowired
    RestTemplate restTemplate;

    public Item getItem(int id, int amount) {
        Book book = restTemplate
                .exchange("http://ms-book/books/" + id, HttpMethod.GET, HttpEntity.EMPTY, Book.class)
                .getBody();

        Item item = new Item();
        item.setProductId(book.id);
        item.setProductName(book.title);
        item.setPrice(book.price);
        item.setAmount(amount);
        return item;
    }


    @Data
    static class Book {
        private int id;
        private long price;
        private String title;
    }


}
