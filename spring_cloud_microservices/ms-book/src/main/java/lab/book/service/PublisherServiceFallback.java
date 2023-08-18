package lab.book.service;

import lab.book.model.Publisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
@Component
@Slf4j
public class PublisherServiceFallback implements PublisherService{
    @Override
    public Publisher getPublisherById(int publisherId) {
        log.error("Fallback action for getPublisherById({})", publisherId);
        return null;
    }
}