package lab.cart.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;

@Data
@EqualsAndHashCode
public class Item implements Serializable {

    private int productId;
    private String productName;
    private float price;
    private int amount;
}
