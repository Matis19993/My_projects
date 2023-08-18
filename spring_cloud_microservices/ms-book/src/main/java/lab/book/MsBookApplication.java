package lab.book;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.security.oauth2.config.annotation.web.configuration.EnableResourceServer;

@SpringBootApplication
@EnableFeignClients
@EnableResourceServer
public class MsBookApplication {

    public static void main(String[] args) {
        SpringApplication.run(MsBookApplication.class, args);
    }

}
