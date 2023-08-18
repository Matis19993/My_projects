package lab.auth.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.oauth2.provider.token.DefaultTokenServices;
import org.springframework.security.oauth2.provider.token.TokenStore;
import org.springframework.security.oauth2.provider.token.store.JwtAccessTokenConverter;
import org.springframework.security.oauth2.provider.token.store.JwtTokenStore;
import org.springframework.security.oauth2.provider.token.store.KeyStoreKeyFactory;

import java.security.KeyPair;

@Configuration
public class JWTConfig {

    @Autowired
    private OAuth2Params params;

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {

        KeyStoreKeyFactory keyFactory = new KeyStoreKeyFactory(
                params.getJwt().getKeyStore(),
                params.getJwt().getKeyStorePassword().toCharArray()
        );
        KeyPair keyPair = keyFactory.getKeyPair(params.getJwt().getKeyPairAlias());

        JwtAccessTokenConverter converter = new JwtAccessTokenConverter();
        converter.setKeyPair(keyPair);
        return converter;
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter());
    }

    @Bean
    public DefaultTokenServices defaultTokenServices() {
        DefaultTokenServices services = new DefaultTokenServices();
        services.setTokenStore(tokenStore());
        services.setSupportRefreshToken(true);
        return services;
    }


}
