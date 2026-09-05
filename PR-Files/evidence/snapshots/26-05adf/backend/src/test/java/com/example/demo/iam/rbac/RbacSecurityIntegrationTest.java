package com.example.demo.iam.rbac;

import com.example.demo.auth.security.TokenBlacklistService;
import com.example.demo.auth.jwt.JwtProvider;
import com.example.demo.iam.role.service.RolePermissionService;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@ActiveProfiles("test")
@AutoConfigureMockMvc
@Sql("/sql/security-test-data.sql")
class RbacSecurityIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JwtProvider jwtProvider;

    @MockBean
    private TokenBlacklistService tokenBlacklistService;

    @MockBean
    private RolePermissionService rolePermissionService;

    @BeforeEach
    void setUp() {
        given(tokenBlacklistService.isBlacklisted(anyString()))
                .willReturn(false);
    }

    @Test
    @DisplayName("ROLE_ASSIGN 권한이 있으면 Role Permission 설정 API에 접근할 수 있다")
    void adminCanAssignPermissions() throws Exception {

        String token =
                jwtProvider.createAccessToken(
                        2L,
                        "admin"
                );

        mockMvc.perform(
                post("/api/admin/roles/1/permissions")
                        .header(
                                "Authorization",
                                "Bearer " + token
                        )
                        .contentType("application/json")
                        .content("""
                                {
                                    "permissionIds": []
                                }
                                """)
        )
                .andExpect(status().isOk());

        verify(rolePermissionService)
                .assignPermissions(
                        eq(2L),
                        eq(1L),
                        anyList()
                );
    }

    @Test
    @DisplayName("ROLE_ASSIGN 권한이 없으면 Role Permission 설정 API는 403을 반환한다")
    void normalUserCannotAssignPermissions() throws Exception {

        String token =
                jwtProvider.createAccessToken(
                        1L,
                        "testuser"
                );

        mockMvc.perform(
                post("/api/admin/roles/1/permissions")
                        .header(
                                "Authorization",
                                "Bearer " + token
                        )
                        .contentType("application/json")
                        .content("""
                                {
                                    "permissionIds": []
                                }
                                """)
        )
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("인증되지 않은 사용자는 Role Permission API에 접근할 수 없다")
    void unauthenticatedUserCannotAssignPermissions()
            throws Exception {

        mockMvc.perform(
                post("/api/admin/roles/1/permissions")
                        .contentType("application/json")
                        .content("""
                                {
                                    "permissionIds": []
                                }
                                """)
        )
                .andExpect(status().isUnauthorized());
    }
}
