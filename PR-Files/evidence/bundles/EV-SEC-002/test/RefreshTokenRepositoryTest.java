package com.example.demo.auth.security;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import org.mockito.InjectMocks;
import org.mockito.Mock;

import org.mockito.junit.jupiter.MockitoExtension;

import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

import java.time.Duration;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;

import static org.mockito.BDDMockito.given;

import static org.mockito.Mockito.verify;


@ExtendWith(MockitoExtension.class)
class RefreshTokenRepositoryTest {


    @InjectMocks
    private RefreshTokenRepository repository;


    @Mock
    private RedisTemplate<String, String> redisTemplate;


    @Mock
    private ValueOperations<String, String> valueOperations;


    @Test
    @DisplayName(
            "Refresh Token 저장 시 user 기준 Redis Key 저장"
    )
    void saveRefreshToken()
    {

        given(
                redisTemplate.opsForValue()
        )
        .willReturn(
                valueOperations
        );


        repository.save(
                1L,
                "refresh-jti",
                Duration.ofDays(7)
        );


        verify(
                valueOperations
        )
        .set(
                "auth:refresh:user:1",
                "refresh-jti",
                Duration.ofDays(7)
        );
    }


    @Test
    @DisplayName(
            "Refresh Token 삭제 시 사용자 Key 제거"
    )
    void deleteRefreshToken()
    {

        repository.delete(
                1L
        );


        verify(
                redisTemplate
        )
        .delete(
                "auth:refresh:user:1"
        );
    }


    @Test
    @DisplayName(
            "Refresh Token Rotation 성공 시 true 반환"
    )
    void rotateSuccess()
    {

        given(
                redisTemplate.execute(
                        any(),
                        anyList(),
                        anyString(),
                        anyString(),
                        anyString()
                )
        )
        .willReturn(
                1L
        );


        boolean result =
                repository.rotate(
                        1L,
                        "old-jti",
                        "new-jti",
                        Duration.ofDays(7)
                );


        assertThat(result)
                .isTrue();
    	verify(redisTemplate)
            .execute(
                    any(),
                    eq(List.of("auth:refresh:user:1")),
                    eq("old-jti"),
                    eq("new-jti"),
                    eq(String.valueOf(
                            Duration.ofDays(7).toMillis()
                    ))
            );
    }


    @Test
    @DisplayName(
            "이미 사용된 Refresh Token이면 Rotation 실패"
    )
    void rotateFail()
    {

        given(
                redisTemplate.execute(
                        any(),
                        anyList(),
                        anyString(),
                        anyString(),
                        anyString()
                )
        )
        .willReturn(
                0L
        );


        boolean result =
                repository.rotate(
                        1L,
                        "old-jti",
                        "new-jti",
                        Duration.ofDays(7)
                );


        assertThat(result)
                .isFalse();
	verify(redisTemplate)
   	     .execute(
                any(),
                eq(List.of("auth:refresh:user:1")),
                eq("old-jti"),
                eq("new-jti"),
                eq(String.valueOf(
                        Duration.ofDays(7).toMillis()
                ))
            );
    }

@Test
@DisplayName(
        "Redis Script 결과가 null이면 Rotation 실패"
)
void rotateNull()
{
    given(
        redisTemplate.execute(
            any(),
            anyList(),
            anyString(),
            anyString(),
            anyString()
        )
    )
    .willReturn(null);


    boolean result =
            repository.rotate(
                    1L,
                    "old-jti",
                    "new-jti",
                    Duration.ofDays(7)
            );


    assertThat(result)
            .isFalse();
}

}
