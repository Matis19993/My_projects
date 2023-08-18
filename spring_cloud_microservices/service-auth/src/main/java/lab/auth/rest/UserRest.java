package lab.auth.rest;

import org.springframework.security.oauth2.provider.OAuth2Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class UserRest {

    @GetMapping("/user")
    Map<String, Object> getUser(OAuth2Authentication authentication){

        Map<String, Object> map = new HashMap<>();
        map.put("username", authentication.getUserAuthentication().getPrincipal());
        map.put("authorities", authentication.getUserAuthentication().getAuthorities());
        map.put("details", authentication.getDetails());

        return map;
    }

}
