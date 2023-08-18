package lab.cart.data;

import lab.cart.model.Cart;

public interface CartRepository {

    Cart findById(long id);

    void update(Cart cart);


}
