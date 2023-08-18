package lab.book.service;

import lab.book.model.Publisher;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name="ms-publisher", fallback = PublisherServiceFallback.class)
public interface PublisherService {

    @GetMapping("/publishers/{id}")
    Publisher getPublisherById(@PathVariable("id") int publisherId);
}
