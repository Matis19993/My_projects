package lab.publisher.data;

import lab.publisher.model.Publisher;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface PublisherRepository extends JpaRepository<Publisher, Integer> {
    /*List<Publisher> findAll();

    Optional<Publisher> findById(Integer id);

    Publisher save(Publisher p);*/
}
