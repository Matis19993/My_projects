package lab.publisher.data.jpa;

import lab.publisher.data.PublisherRepository;
import lab.publisher.model.Publisher;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;
import java.util.Optional;

//@Repository
public abstract class JpaPublisherRepository implements PublisherRepository {

    @PersistenceContext
    private EntityManager em;

    @Override
    public List<Publisher> findAll() {
        return em.createQuery("select p from Publisher p").getResultList();
    }

    @Override
    public Optional<Publisher> findById(Integer id) {
        return Optional.ofNullable(em.find(Publisher.class, id));
    }

    @Override
    public Publisher save(Publisher p) {
        em.persist(p);
        return p;
    }
}
