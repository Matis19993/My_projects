package lab.delivery;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.function.Consumer;

@SpringBootApplication
@Slf4j
public class MsDeliveryApplication {

    public static void main(String[] args) {
        SpringApplication.run(MsDeliveryApplication.class, args);
    }

    @Bean
    Consumer<String> consumeCart(){
        return cartString -> log.info("starting delivery process for a cart {}", cartString);
    }

}
