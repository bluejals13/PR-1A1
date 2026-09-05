package com.example.demo.auth.security;

import com.example.demo.auth.jwt.JwtProvider;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;

import java.io.IOException;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class JwtAuthenticationFilterTest {

    @InjectMocks
    private JwtAuthenticationFilter jwtAuthenticationFilter;

    @Mock
    private JwtProvider jwtProvider;

    @Mock
    private TokenBlacklistService tokenBlacklistService;

    @Mock
    private UserAuthorityService userAuthorityService;

    @Mock
    private HttpServletRequest request;

    @Mock
    private HttpServletResponse response;

    @Mock
    private FilterChain filterChain;

    @Mock
    private Claims claims;

    @BeforeEach
    void setUp() {
        SecurityContextHolder.clearContext();
    }

    @Test
    @DisplayName("인증 API 경로는 토큰 검증 없이 바로 다음 필터로 진행한다")
    void bypassAuthPath() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/auth/login");

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        verify(filterChain).doFilter(request, response);
        verifyNoInteractions(jwtProvider);
    }

    @Test
    @DisplayName("OPTIONS 사전 요청은 토큰 검증 없이 바로 다음 필터로 진행한다")
    void bypassOptionsMethod() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/users/me");
        given(request.getMethod()).willReturn("OPTIONS");

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        verify(filterChain).doFilter(request, response);
        verifyNoInteractions(jwtProvider);
    }

    @Test
    @DisplayName("Authorization 헤더가 없으면 토큰 검증 없이 필터 체인을 계속 진행한다")
    void bypassWhenNoAuthorizationHeader() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/users/me");
        given(request.getMethod()).willReturn("GET");
        given(request.getHeader("Authorization")).willReturn(null);

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        verify(filterChain).doFilter(request, response);
        verifyNoInteractions(jwtProvider);
    }

    @Test
    @DisplayName("유효한 Access Token인 경우 SecurityContext에 인증 정보가 설정된다")
    void validAccessTokenSetsSecurityContext() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/users/me");
        given(request.getMethod()).willReturn("GET");
        given(request.getHeader("Authorization")).willReturn("Bearer valid.access.token");

        given(jwtProvider.parseClaims("valid.access.token")).willReturn(claims);
        given(claims.get("type", String.class)).willReturn("access");
        given(claims.getId()).willReturn("test-jti");
        given(claims.getSubject()).willReturn("1");

        given(tokenBlacklistService.isBlacklisted("test-jti")).willReturn(false);
        given(userAuthorityService.getAuthorities(1L)).willReturn(
                List.of(new SimpleGrantedAuthority("ROLE_USER"))
        );

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNotNull();
        assertThat(SecurityContextHolder.getContext().getAuthentication().getAuthorities())
                .extracting(GrantedAuthority::getAuthority)
                .containsExactly("ROLE_USER");
        verify(filterChain).doFilter(request, response);
    }

    @Test
    @DisplayName("토큰 타입이 access가 아니면 401 Unauthorized를 반환한다")
    void nonAccessTokenReturnsUnauthorized() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/users/me");
        given(request.getMethod()).willReturn("GET");
        given(request.getHeader("Authorization")).willReturn("Bearer refresh.token");

        given(jwtProvider.parseClaims("refresh.token")).willReturn(claims);
        given(claims.get("type", String.class)).willReturn("refresh");

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        verify(response).setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        verify(filterChain, never()).doFilter(any(), any());
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
    }

    @Test
    @DisplayName("블랙리스트에 등록된 토큰인 경우 401 Unauthorized를 반환한다")
    void blacklistedTokenReturnsUnauthorized() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/users/me");
        given(request.getMethod()).willReturn("GET");
        given(request.getHeader("Authorization")).willReturn("Bearer blacklisted.token");

        given(jwtProvider.parseClaims("blacklisted.token")).willReturn(claims);
        given(claims.get("type", String.class)).willReturn("access");
        given(claims.getId()).willReturn("blacklisted-jti");
        given(tokenBlacklistService.isBlacklisted("blacklisted-jti")).willReturn(true);

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        verify(response).setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        verify(filterChain, never()).doFilter(any(), any());
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
    }

    @Test
    @DisplayName("Redis 장애 발생 시 503 Service Unavailable을 반환한다")
    void redisUnavailableReturns503() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/users/me");
        given(request.getMethod()).willReturn("GET");
        given(request.getHeader("Authorization")).willReturn("Bearer valid.token");

        given(jwtProvider.parseClaims("valid.token")).willReturn(claims);
        given(claims.get("type", String.class)).willReturn("access");
        given(claims.getId()).willReturn("test-jti");
        given(tokenBlacklistService.isBlacklisted("test-jti"))
                .willThrow(new RedisUnavailableException("Redis down", new RuntimeException()));

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        verify(response).setStatus(HttpServletResponse.SC_SERVICE_UNAVAILABLE);
        verify(filterChain, never()).doFilter(any(), any());
    }

    @Test
    @DisplayName("만료되었거나 손상된 JWT인 경우 401 Unauthorized를 반환한다")
    void invalidJwtReturnsUnauthorized() throws ServletException, IOException {
        given(request.getServletPath()).willReturn("/api/users/me");
        given(request.getMethod()).willReturn("GET");
        given(request.getHeader("Authorization")).willReturn("Bearer expired.token");

        given(jwtProvider.parseClaims("expired.token"))
                .willThrow(new ExpiredJwtException(null, claims, "Token expired"));

        jwtAuthenticationFilter.doFilter(request, response, filterChain);

        verify(response).setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        verify(filterChain, never()).doFilter(any(), any());
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
    }
}
