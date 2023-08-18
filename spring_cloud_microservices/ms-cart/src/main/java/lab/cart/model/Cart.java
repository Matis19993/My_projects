package lab.cart.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;
import java.util.List;

@Data
@EqualsAndHashCode
public class Cart implements Serializable {

    private long id;
    private List<Item> items;
    private float totalPrice;

}
