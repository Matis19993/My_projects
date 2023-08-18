package lab.publisher;

import lab.publisher.data.PublisherRepository;
import lab.publisher.model.Publisher;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class PublisherCLI implements CommandLineRunner {

    private final PublisherRepository repository;
    @Override
    public void run(String... args) throws Exception {
        List<Publisher> publishers = repository.findAll();
        log.info("publishers: {}", publishers);
    }
}
