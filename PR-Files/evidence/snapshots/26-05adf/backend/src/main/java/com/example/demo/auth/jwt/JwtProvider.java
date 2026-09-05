package com.example.demo.auth.jwt;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;    // jwt 서명 용 보안 키 와 jjwt : HS256 방식 대칭키
import jakarta.annotation.PostConstruct; // 빈 생성 후 초기화 : 보안 키 검증용
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.security.Key;     // 보안 키 객체
import java.util.Date;        // 만료 날짜
import java.util.UUID;        // 만료 jti
import lombok.extern.slf4j.Slf4j;    // 기본 로거 호출용

@Slf4j
@Component
public class JwtProvider {    // 각 토큰 제공 파일
    
    // application.yaml 부분의 환경 변수 일치 확인 할 것
    
    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.expiration}")
    private long expiration;

    @Value("${jwt.access-expiration}")
    private long accessExpiration;

    @Value("${jwt.refresh-expiration}")
    private long refreshExpiration;
    
    //
    
    private Key key;
    private JwtParser jwtParser;

    // secretKey 길이 32바이트 미만이면 런타임 에러
    @PostConstruct
    public void init() {            //Secret Key 검증 부분
        if (secretKey == null || secretKey.length() < 32) {
            throw new IllegalStateException(
                "JWT Secret Key must be at least 32 characters."
            );
        }  

        this.key = Keys.hmacShaKeyFor(
            secretKey.getBytes(StandardCharsets.UTF_8)
        );
        this.jwtParser = Jwts.parserBuilder()
            .setSigningKey(this.key)
            .build();
    }

    // 1. 접근 토큰 생성
    public String createAccessToken(Long userId, String username) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + accessExpiration);

        String jti = UUID.randomUUID().toString();

        return Jwts.builder()
                .setSubject(String.valueOf(userId))
                .setId(jti)
                .claim("username", username) 
                .claim("type", "access")
                .setIssuedAt(now)
                .setExpiration(expiry)
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }

    // 1. 리프레시 토큰 생성    
    public String createRefreshToken(Long userId) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + refreshExpiration);

        String jti = UUID.randomUUID().toString();

        return Jwts.builder()
                .setSubject(String.valueOf(userId))
                .setId(jti)
                .claim("type", "refresh")
                .setIssuedAt(now)
                .setExpiration(expiry)
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }

    // 2. claims 공통 파서 (캐싱된 jwtParser 재사용)
    public Claims parseClaims(String token) {
        return jwtParser.parseClaimsJws(token).getBody();
    }

    // 2-5. Jti 추출
    public String getJti(String token) {
        return parseClaims(token).getId();
    }

    // 3. userId 추출
    public Long getUserId(String token) {
        return Long.parseLong(parseClaims(token).getSubject());
    }

    // 4. JWT 유효성 검증
    public boolean validateToken(String token) {
        if (token == null || token.isBlank()) {
            return false;
        }
        try {
            parseClaims(token);
            return true;
        } catch (SecurityException | MalformedJwtException e) {
            log.warn("Invalid JWT signature / malformed token: {}", e.getMessage());
        } catch (ExpiredJwtException e) {
            log.warn("Expired JWT token: {}", e.getMessage());
        } catch (UnsupportedJwtException e) {
            log.warn("Unsupported JWT token: {}", e.getMessage());
        } catch (IllegalArgumentException e) {
            log.warn("JWT token claims string is empty or invalid: {}", e.getMessage());
        } catch (JwtException e) {
            log.warn("JWT processing failed: {}", e.getMessage());
        }
        return false;
    }

    // 5. role 추출
    public String getRole(String token) {
        return parseClaims(token)
            .get("role", String.class);
    }

}
