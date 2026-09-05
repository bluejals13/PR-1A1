package com.example.demo.auth.security;

import com.example.demo.iam.user.domain.User;
import com.example.demo.iam.user.domain.UserStatus;
import com.example.demo.iam.user.repository.UserRepository;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Slf4j
@Service
@RequiredArgsConstructor
public class UserAuthorityService {

    private final UserRepository userRepository;

    public List<GrantedAuthority> getAuthorities(Long userId) {
        log.debug("Fetching authorities for userId={}", userId);

        User user = userRepository.findWithRolesAndPermissionsById(userId)
                .orElseThrow(() -> {
                    log.warn("User not found during authority resolution: userId={}", userId);
                    return new BadCredentialsException("INVALID_CREDENTIALS");
                });

        // 사용자 상태 검증
        if (user.getStatus() != UserStatus.ACTIVE) {
            log.warn("User is not active: userId={}, status={}", userId, user.getStatus());
            throw new BadCredentialsException("USER_NOT_ACTIVE");
        }

        Set<GrantedAuthority> authorities = new HashSet<>();

        // ROLE + Permission 추가
        user.getRoles().forEach(role -> {
            authorities.add(
                    new SimpleGrantedAuthority(
                            "ROLE_" + role.getName()
                    )
            );

            role.getPermissions().forEach(permission -> {
                authorities.add(
                        new SimpleGrantedAuthority(
                                permission.getName()
                        )
                );
            });
        });

        log.debug("Resolved authorities for userId={}: {}", userId, authorities);
        return List.copyOf(authorities);
    }
}
