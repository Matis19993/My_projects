package lab.publisher.model;

import lombok.Data;

import javax.persistence.*;

@Data
@Entity
@Table(name="publisher")
public class Publisher {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column(name="name")
    private String name;
    private String logo;
}
