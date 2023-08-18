package lab.book.model;

import lombok.Data;

@Data
public class Rating {

    private int id;
    private int rate;
    private String description;
    private int bookId;
}
