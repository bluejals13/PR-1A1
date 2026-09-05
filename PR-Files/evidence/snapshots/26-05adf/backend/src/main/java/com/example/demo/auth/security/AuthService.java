package com.example.demo.auth.security;
import com.example.demo.auth.jwt.JwtProvider;

import com.example.demo.iam.user.domain.User;
import com.example.demo.iam.user.domain.UserStatus;

import com.example.demo.iam.user.dto.LoginRequest;
import com.example.demo.iam.user.dto.LoginResult;
import com.example.demo.iam.user.dto.LoginResponse;

import com.example.demo.iam.user.repository.UserRepository;

import io.jsonwebtoken.Claims;
import lombok.RequiredArgsConstructor;

import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import org.springframework.security.authentication.DisabledException;

import java.time.Duration;

@Service
@RequiredArgsConstructor
public class AuthService {

    private static final Duration REFRESH_TOKEN_TTL =
            Duration.ofDays(7);

    private final JwtProvider jwtProvider;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    private final RefreshTokenRepository refreshTokenRepository;
    private final TokenBlacklistService blacklistService;


    @Transactional
    public LoginResult login(LoginRequest request) {

        User user = findActiveUser(
                request.username(),
                request.password()
        );

        String accessToken = createAccessToken(user);
        String refreshToken = createRefreshToken(user);

        saveRefreshToken(user.getId(), refreshToken);

        return new LoginResult(
                accessToken,
                "Bearer",
                refreshToken
        );
    }

    

    public LoginResult refresh(String refreshToken) {

        Claims claims = parseTokenClaims(
                refreshToken,
                "refresh"
        );

        Long userId = Long.parseLong(
                claims.getSubject()
        );

        String oldJti = claims.getId();

        if (oldJti == null || oldJti.isBlank()) {    //Jti null,
            throw new BadCredentialsException(
                    "INVALID_REFRESH_TOKEN"
            );
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new BadCredentialsException(
                                "INVALID_CREDENTIALS"
                        )
                );

        checkAccountActive(user);

        String newRefreshToken =
                createRefreshToken(user);

        String newJti =
                extractJti(newRefreshToken);

        boolean rotated =
                refreshTokenRepository.rotate(
                        userId,
                        oldJti,
                        newJti,
                        REFRESH_TOKEN_TTL
                );

        if (!rotated) {    
            throw new BadCredentialsException(        //!rotated,
                    "INVALID_OR_REUSED_REFRESH_TOKEN"
            );
        }

        return new LoginResult(
                createAccessToken(user),
                "Bearer",
                newRefreshToken
        );
    }
    


    public void logout(String accessToken) {

        //if (accessToken == null || accessToken.isBlank()) { return; }

        Claims claims = parseTokenClaims(
                accessToken,
                "access"
        );

        Long userId =
                Long.parseLong(claims.getSubject());

        String jti = claims.getId();

        long remainingMillis =
                claims.getExpiration().getTime()
                        - System.currentTimeMillis();

        if (jti != null && remainingMillis > 0) {        //jti null,
            blacklistService.blacklist(
                    jti,
                    remainingMillis
            );
        }

        refreshTokenRepository.delete(userId);
    }
    


    private Claims parseTokenClaims(    // Claims
            String token,
            String expectedType
    ) {

        Claims claims =
                jwtProvider.parseClaims(token);

        String type =
                claims.get("type", String.class);

        if (!expectedType.equals(type)) {    // 동등 타입으로 확인

            throw new BadCredentialsException(
                    "INVALID_TOKEN"
            );
        }

        return claims;
    }


    private void checkAccountActive(User user) {

        if (user.getStatus() != UserStatus.ACTIVE) {    // 권한 ACTIVE 검증 DisabledException

            throw new DisabledException("ACCOUNT_DISABLED");
        }
    }


    private String extractJti(String token) {        // 유효한 리프레시 가능 Jti 검증,

        Claims claims =
                jwtProvider.parseClaims(token);

        String jti = claims.getId();

        if (jti == null || jti.isBlank()) {

            throw new BadCredentialsException(
                    "INVALID_REFRESH_TOKEN"
            );
        }

        return jti;
    }


    private void saveRefreshToken(    // 리프레시토큰 저장 / Jti 따로 저장
            Long userId,
            String refreshToken
    ) {

        refreshTokenRepository.save(
                userId,
                extractJti(refreshToken),
                REFRESH_TOKEN_TTL
        );
    }


    private String createAccessToken(User user) {    // 접근 토큰 생성

        return jwtProvider.createAccessToken(
                user.getId(),
                user.getUsername()
        );
    }


    private String createRefreshToken(User user) {    // 리프레시 토큰 생성

        return jwtProvider.createRefreshToken(
                user.getId()
        );
    }


    private User findActiveUser(        // 해당 계정 JPA 요청
            String username,
            String password
    ) {

        User user =
                userRepository.findByUsername(username)
                        .orElseThrow(() ->
                                new BadCredentialsException(
                                        "INVALID_CREDENTIALS"
                                )
                        );

        if (!passwordEncoder.matches(       // 비번 오류
                password,
                user.getPassword()
        )) {
            throw new BadCredentialsException(
                    "INVALID_CREDENTIALS"
            );
        }

        checkAccountActive(user);

        return user;
    }
}
