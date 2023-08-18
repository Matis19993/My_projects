package lab.cart.web;

import com.fasterxml.jackson.core.JsonProcessingException;
import lab.cart.data.CartRepository;
import lab.cart.model.Cart;
import lab.cart.model.Item;
import lab.cart.service.BookService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cloud.stream.messaging.Source;
import org.springframework.messaging.support.MessageBuilder;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.LinkedList;

@Slf4j
@RestController
@RequiredArgsConstructor
public class CartRest {

    private final CartRepository repository;
    private final BookService bookService;
    private final Source source;

    @PostMapping("/carts")
    public Cart createCart() {
        log.info("creating new cart...");
        return createNewCart();
    }


    private Cart createNewCart() {
        long millis = LocalDateTime.now().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli();
        Cart cart = new Cart();
        cart.setId(millis);
        repository.update(cart);
        log.info("cart created, id {}", millis);
        return cart;
    }

    @GetMapping("/carts/{id}")
    public Cart getCart(@PathVariable long id) {
        log.info("retrieving cart {}", id);
        return repository.findById(id);
    }

    @PostMapping("/carts/{id}")
    public Cart confirmCart(@PathVariable long id) throws JsonProcessingException {
        log.info("confirming cart {}", id);
        Cart cart = repository.findById(id);
        // TODO send order
        source.output().send(MessageBuilder.withPayload(cart).build());

        return createNewCart();
    }

    @PutMapping("/carts/{cartId}/items/{itemId}")
    public void addToCart(@PathVariable long cartId, @PathVariable int itemId, @RequestBody int amount) {
        log.info("adding item {} to cart {}", itemId, cartId);
        Cart cart = repository.findById(cartId);
        Item item = bookService.getItem(itemId, amount);
        if (cart.getItems() == null) {
            cart.setItems(new LinkedList<>());
        }
        cart.getItems().add(item);
        repository.update(cart);
    }

    @DeleteMapping("/carts/{cartId}/items/{itemId}")
    public void deleteFromCart(@PathVariable long cartId, @PathVariable int itemId) {
        log.info("deleting item {} from cart {}", itemId, cartId);
        Cart cart = repository.findById(cartId);
        cart.getItems().removeIf(item -> item.getProductId() == itemId);
        repository.update(cart);
    }

}
