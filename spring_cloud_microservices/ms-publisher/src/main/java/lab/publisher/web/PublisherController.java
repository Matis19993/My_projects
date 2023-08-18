package lab.publisher.web;

import lab.publisher.data.PublisherRepository;
import lab.publisher.model.Publisher;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
@Slf4j
public class PublisherController {

    private final PublisherRepository repository;

    @GetMapping("/publishers")
    List<Publisher> getPublishers(){
        log.info("about to retrieve publishers");
        return repository.findAll();
    }

    @GetMapping("/publishers/{id}")
    Publisher getPublisher(@PathVariable("id") int id){
        log.info("about to retrieve publisher {}", id);
        return repository.findById(id).orElse(null);
    }

}
