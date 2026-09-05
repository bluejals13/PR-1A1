package com.example.demo.auth.security;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.QueryTimeoutException;
import org.springframework.data.redis.RedisConnectionFailureException;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

import java.time.Duration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TokenBlacklistServiceTest {

    @InjectMocks
    private TokenBlacklistService tokenBlacklistService;

    @Mock
    private RedisTemplate<String, String> redisTemplate;

    @Mock
    private ValueOperations<String, String> valueOperations;

    @Test
    @DisplayName("정상적인 JTI와 만료시간으로 블랙리스트 등록 시 Redis에 저장된다")
    void blacklistSuccess() {
        given(redisTemplate.opsForValue()).willReturn(valueOperations);

        tokenBlacklistService.blacklist("test-jti", 60000L);

        verify(valueOperations).set(
                eq("blacklist:test-jti"),
                eq("1"),
                eq(Duration.ofMillis(60000L))
        );
    }

    @Test
    @DisplayName("JTI가 null 또는 빈 문자열이거나 유효하지 않은 만료시간이면 Redis를 호출하지 않는다")
    void blacklistIgnoreInvalidInput() {
        tokenBlacklistService.blacklist(null, 60000L);
        tokenBlacklistService.blacklist("", 60000L);
        tokenBlacklistService.blacklist("   ", 60000L);
        tokenBlacklistService.blacklist("test-jti", 0L);
        tokenBlacklistService.blacklist("test-jti", -100L);

        verifyNoInteractions(redisTemplate);
    }

    @Test
    @DisplayName("블랙리스트 등록 중 Redis 연결 장애 발생 시 RedisUnavailableException 예외가 발생한다")
    void blacklistThrowsRedisUnavailableExceptionWhenRedisFails() {
        given(redisTemplate.opsForValue()).willReturn(valueOperations);
        doThrow(new RedisConnectionFailureException("Connection refused"))
                .when(valueOperations).set(any(), any(), any(Duration.class));

        assertThatThrownBy(() -> tokenBlacklistService.blacklist("test-jti", 60000L))
                .isInstanceOf(RedisUnavailableException.class)
                .hasMessageContaining("Redis is unavailable");
    }

    @Test
    @DisplayName("블랙리스트에 등록된 JTI 조회 시 true를 반환한다")
    void isBlacklistedReturnsTrue() {
        given(redisTemplate.hasKey("blacklist:test-jti")).willReturn(true);

        boolean result = tokenBlacklistService.isBlacklisted("test-jti");

        assertThat(result).isTrue();
    }

    @Test
    @DisplayName("블랙리스트에 없는 JTI 조회 시 false를 반환한다")
    void isBlacklistedReturnsFalse() {
        given(redisTemplate.hasKey("blacklist:not-found")).willReturn(false);

        boolean result = tokenBlacklistService.isBlacklisted("not-found");

        assertThat(result).isFalse();
    }

    @Test
    @DisplayName("JTI가 null 또는 빈 문자열이면 false를 반환하고 Redis를 조회하지 않는다")
    void isBlacklistedReturnsFalseForNullOrBlank() {
        assertThat(tokenBlacklistService.isBlacklisted(null)).isFalse();
        assertThat(tokenBlacklistService.isBlacklisted("")).isFalse();
        assertThat(tokenBlacklistService.isBlacklisted("   ")).isFalse();

        verifyNoInteractions(redisTemplate);
    }

    @Test
    @DisplayName("블랙리스트 조회 중 Redis 타임아웃 발생 시 RedisUnavailableException 예외가 발생한다")
    void isBlacklistedThrowsRedisUnavailableExceptionWhenRedisFails() {
        given(redisTemplate.hasKey("blacklist:timeout-jti"))
                .willThrow(new QueryTimeoutException("Redis query timeout"));

        assertThatThrownBy(() -> tokenBlacklistService.isBlacklisted("timeout-jti"))
                .isInstanceOf(RedisUnavailableException.class)
                .hasMessageContaining("Redis is unavailable");
    }
}
