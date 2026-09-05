package com.example.demo.auth.security;

import java.time.Duration;
import java.util.List;

import lombok.RequiredArgsConstructor;

import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.stereotype.Repository;

@Repository
@RequiredArgsConstructor
public class RefreshTokenRepository {

    private final RedisTemplate<String, String> redisTemplate;

    private static final String REFRESH_KEY =
            "auth:refresh:user:";

    private static final DefaultRedisScript<Long> ROTATE_SCRIPT =
            new DefaultRedisScript<>(
                    """
                    local current = redis.call(
                        'GET',
                        KEYS[1]
                    )

                    if current == ARGV[1] then
                        redis.call(
                            'SET',
                            KEYS[1],
                            ARGV[2],
                            'PX',
                            ARGV[3]
                        )

                        return 1
                    end

                    return 0
                    """,
                    Long.class
            );

    public void save(
            Long userId,
            String jti,
            Duration ttl
    ) {

        redisTemplate.opsForValue().set(
                key(userId),
                jti,
                ttl
        );
    }

    public boolean rotate(
            Long userId,
            String oldJti,
            String newJti,
            Duration ttl
    ) {

        Long result =
                redisTemplate.execute(
                        ROTATE_SCRIPT,
                        List.of(key(userId)),
                        oldJti,
                        newJti,
                        String.valueOf(ttl.toMillis())
                );

        return result != null && result == 1L;
    }

    public void delete(Long userId) {

        redisTemplate.delete(
                key(userId)
        );
    }

    private String key(Long userId) {

        return REFRESH_KEY + userId;
    }
}
