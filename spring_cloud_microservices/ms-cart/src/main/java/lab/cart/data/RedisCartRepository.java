package lab.cart.data;

import lab.cart.model.Cart;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.HashOperations;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Repository;

import javax.annotation.PostConstruct;

@Repository
@RequiredArgsConstructor
public class RedisCartRepository implements CartRepository {

    private static final String CART = "CART";

    private final RedisTemplate redisTemplate;
    private HashOperations<String, Long, Cart> hashOperations;

    @PostConstruct
    private void init() {
        hashOperations = redisTemplate.opsForHash();
    }

    @Override
    public Cart findById(long id) {
        return this.hashOperations.get(CART, id);
    }

    @Override
    public void update(Cart cart) {
        this.hashOperations.put(CART, cart.getId(), cart);
    }
}
