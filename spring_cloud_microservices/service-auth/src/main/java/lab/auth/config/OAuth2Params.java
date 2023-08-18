package lab.auth.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

@Data
@ConfigurationProperties(prefix = "oauth2", ignoreUnknownFields = false)
@Component
public class OAuth2Params {

	private Client client;
	private Jwt jwt;

	@Data
	public static class Client {
		private String id;
		private String secret;
	}

	@Data
	public static class Jwt {
		private Resource keyStore;
		private String keyStorePassword;
		private String keyPairAlias;
		private String keyPairPassword;
	}


}
