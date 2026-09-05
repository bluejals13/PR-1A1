package com.example.demo.auth.security;

import com.example.demo.auth.jwt.JwtProvider;

import com.example.demo.iam.user.domain.User;

import com.example.demo.iam.user.dto.LoginRequest;
import com.example.demo.iam.user.dto.LoginResult;

import com.example.demo.iam.user.repository.UserRepository;

import io.jsonwebtoken.Claims;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import org.junit.jupiter.api.extension.ExtendWith;

import org.mockito.InjectMocks;
import org.mockito.Mock;

import org.mockito.junit.jupiter.MockitoExtension;

import org.springframework.security.authentication.BadCredentialsException;

import org.springframework.security.crypto.password.PasswordEncoder;

import org.springframework.test.util.ReflectionTestUtils;

import java.time.Duration;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import static org.mockito.ArgumentMatchers.eq;

import static org.mockito.BDDMockito.given;

import static org.mockito.Mockito.mock;

import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;


@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @InjectMocks
    private AuthService authService;


    @Mock
    private JwtProvider jwtProvider;


    @Mock
    private RefreshTokenRepository refreshTokenRepository;


    @Mock
    private UserRepository userRepository;


    @Mock
    private PasswordEncoder passwordEncoder;


    @Mock
    private TokenBlacklistService blacklistService;




    @Test
    @DisplayName(
            "정상적인 사용자 정보면 Access Token과 Refresh Token을 발급한다"
    )
    void loginSuccess() {

        User user =
                createUser(
                        1L,
                        "testuser",
                        "encoded-password"
                );

        LoginRequest request =
                new LoginRequest(
                        "testuser",
                        "password123!"
                );

        Claims refreshClaims =
                mock(
                        Claims.class
                );

        given(
                userRepository.findByUsername(
                        "testuser"
                )
        ).willReturn(
                Optional.of(user)
        );

        given(
                passwordEncoder.matches(
                        "password123!",
                        "encoded-password"
                )
        ).willReturn(
                true
        );

        given(
                jwtProvider.createAccessToken(
                        1L,
                        "testuser"
                )
        ).willReturn(
                "access-token"
        );

        given(
                jwtProvider.createRefreshToken(
                        1L
                )
        ).willReturn(
                "refresh-token"
        );

        given(
                jwtProvider.parseClaims(
                        "refresh-token"
                )
        ).willReturn(
                refreshClaims
        );

        given(
                refreshClaims.getId()
        ).willReturn(
                "refresh-jti"
        );



        LoginResult result =
                authService.login(
                        request
                );


        assertThat(
                result.accessToken()
        ).isEqualTo(
                "access-token"
        );

        assertThat(
                result.grantType()
        ).isEqualTo(
                "Bearer"
        );

        assertThat(
                result.refreshToken()
        ).isEqualTo(
                "refresh-token"
        );


        verify(
                refreshTokenRepository
        ).save(
                1L,
                "refresh-jti",
                Duration.ofDays(7)
                );
    }


    @Test
    @DisplayName(
            "존재하지 않는 사용자면 로그인에 실패하고 토큰을 발급하지 않는다"
    )
    void loginFailWhenUserNotFound() {

        given(
                userRepository.findByUsername(
                        "unknown"
                )
        ).willReturn(
                Optional.empty()
        );


        assertThatThrownBy(
                () ->
                        authService.login(
                                new LoginRequest(
                                        "unknown",
                                        "password123!"
                                )
                        )
        )
                .isInstanceOf(
                        BadCredentialsException.class
                )
                .hasMessage(
                        "INVALID_CREDENTIALS"
                );


        verifyNoInteractions(
                jwtProvider
        );

        verifyNoInteractions(
                refreshTokenRepository
        );
    }


    @Test
    @DisplayName(
            "비밀번호가 일치하지 않으면 로그인에 실패하고 토큰을 발급하지 않는다"
    )
    void loginFailWhenPasswordDoesNotMatch() {

        User user =
                createUser(
                        1L,
                        "testuser",
                        "encoded-password"
                );

        given(
                userRepository.findByUsername(
                        "testuser"
                )
        ).willReturn(
                Optional.of(user)
        );

        given(
                passwordEncoder.matches(
                        "wrong-password",
                        "encoded-password"
                )
        ).willReturn(
                false
        );


        assertThatThrownBy(
                () ->
                        authService.login(
                                new LoginRequest(
                                        "testuser",
                                        "wrong-password"
                                )
                        )
        )
                .isInstanceOf(
                        BadCredentialsException.class
                )
                .hasMessage(
                        "INVALID_CREDENTIALS"
                );


        verifyNoInteractions(
                jwtProvider
        );

        verifyNoInteractions(
                refreshTokenRepository
        );
    }


    private User createUser(
            Long id,
            String username,
            String encodedPassword
    ) {

        User user =
                User.create(
                        username,
                        encodedPassword,
                        "test@example.com"
                );

        ReflectionTestUtils.setField(
                user,
                "id",
                id
        );

        return user;
    }
}
