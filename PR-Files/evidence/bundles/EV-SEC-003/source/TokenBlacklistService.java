package com.example.demo.auth.security;

import java.time.Duration;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.dao.DataAccessException;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class TokenBlacklistService {

    private static final String BLACKLIST_KEY_PREFIX = "blacklist:";
    private final RedisTemplate<String, String> redisTemplate;

    /**
     * Access Token의 JTI를 blacklist에 등록한다.
     *
     * @param jti JWT ID
     * @param expirationMillis blacklist 유지 시간(ms)
     */
    public void blacklist(String jti, long expirationMillis) {
        if (jti == null || jti.isBlank() || expirationMillis <= 0) {
            return;
        }

        try {
            redisTemplate.opsForValue().set(
                    buildKey(jti),
                    "1",
                    Duration.ofMillis(expirationMillis)
            );
            log.debug("Blacklisted token registered. jti={}, ttlMs={}", jti, expirationMillis);
        } catch (DataAccessException e) {
            log.error("Failed to register token to Redis blacklist. jti={}", jti, e);
            throw new RedisUnavailableException("Redis is unavailable for blacklist registration", e);
        }
    }

    /**
     * 해당 JTI가 blacklist에 등록되어 있는지 확인한다.
     *
     * @param jti JWT ID
     * @return blacklist 등록 여부
     */
    public boolean isBlacklisted(String jti) {
        if (jti == null || jti.isBlank()) {
            return false;
        }

        try {
            return Boolean.TRUE.equals(
                    redisTemplate.hasKey(buildKey(jti))
            );
        } catch (DataAccessException e) {
            log.error("Failed to check Redis blacklist. jti={}", jti, e);
            throw new RedisUnavailableException("Redis is unavailable for blacklist verification", e);
        }
    }

    private String buildKey(String jti) {
        return BLACKLIST_KEY_PREFIX + jti;
    }
}
