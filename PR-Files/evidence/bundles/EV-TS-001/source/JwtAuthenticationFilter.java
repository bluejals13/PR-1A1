package com.example.demo.auth.security;

import com.example.demo.auth.jwt.JwtProvider;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtProvider jwtProvider;
    private final TokenBlacklistService tokenBlacklistService;
    private final UserAuthorityService userAuthorityService;

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {

        String path = request.getServletPath();

        // 1. 인증 관련 API는 JWT 필터 제외
        if (path.startsWith("/api/auth/")) {
            filterChain.doFilter(request, response);
            return;
        }

        // 2. CORS preflight 요청 제외
        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            filterChain.doFilter(request, response);
            return;
        }

        // 3. Authorization 헤더 확인
        String header = request.getHeader("Authorization");

        if (header == null || !header.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        String token = header.substring(7);

        if (token.isBlank()) {
            filterChain.doFilter(request, response);
            return;
        }

        try {
            // 4. JWT 파싱 및 서명 검증 (단일 파싱으로 최적화)
            Claims claims = jwtProvider.parseClaims(token);

            // 5. Token Type 검증 (Access Token 여부 확인)
            String tokenType = claims.get("type", String.class);
            if (!"access".equals(tokenType)) {
                log.warn("Invalid token type for authentication: {}", tokenType);
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                return;
            }

            // 6. Access Token blacklist 확인
            String jti = claims.getId();
            if (jti != null && tokenBlacklistService.isBlacklisted(jti)) {
                log.debug("Blacklisted JWT detected. jti={}", jti);
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                return;
            }

            // 7. 사용자 정보 및 권한 조회
            Long userId = Long.parseLong(claims.getSubject());
            List<GrantedAuthority> authorities =
                    userAuthorityService.getAuthorities(userId);

            // 8. SecurityContext 인증 정보 생성
            CustomUserPrincipal principal =
                    new CustomUserPrincipal(userId);

            UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(
                            principal,
                            null,
                            authorities
                    );

            SecurityContextHolder.getContext()
                    .setAuthentication(authentication);

            // 9. 다음 필터로 진행
            filterChain.doFilter(request, response);

        } catch (RedisUnavailableException e) {     // Redis 장애 → 503
            log.error(
                    "Redis is unavailable. Authentication cannot be verified.",
                    e
            );

            SecurityContextHolder.clearContext();
            response.setStatus(HttpServletResponse.SC_SERVICE_UNAVAILABLE);
            return;

        } catch (JwtException | IllegalArgumentException e) {     // JWT 인증 실패 → 401
            log.warn("Invalid or expired JWT: {}", e.getMessage());

            SecurityContextHolder.clearContext();
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }
    }
}
