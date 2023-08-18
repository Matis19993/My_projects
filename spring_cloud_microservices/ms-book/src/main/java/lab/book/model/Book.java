package lab.book.model;

import lombok.Data;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;

@Entity
@Data
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    @NotNull
    private String title;
    @ManyToOne
    private Author author; // _id
    private String cover;
    @Positive
    private float price;
    private int publisherId;
    @Transient
    private double averageRating;
}
