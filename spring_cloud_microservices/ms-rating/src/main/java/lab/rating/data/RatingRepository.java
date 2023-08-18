package lab.rating.data;

import lab.rating.model.Rating;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface RatingRepository extends JpaRepository<Rating, Integer> {

    @Query("select r from Rating r where r.bookId=:bookId")
    List<Rating> findAllByBookId(@Param("bookId") int bookId);
}
