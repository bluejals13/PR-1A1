package com.example.demo.auth.security;

import com.example.demo.auth.jwt.JwtProvider;

import org.springframework.test.context.jdbc.Sql;

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

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;


@SpringBootTest
@ActiveProfiles("test")
@AutoConfigureMockMvc
@Sql("/sql/security-test-data.sql")
class SecurityIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JwtProvider jwtProvider;

    @MockBean
    private TokenBlacklistService tokenBlacklistService;
    
    @BeforeEach
    void setUp() {
        given(tokenBlacklistService.isBlacklisted(anyString()))
                .willReturn(false);
    }
    
    @Test
    @DisplayName("인증되지 않은 사용자는 보호 API 접근 불가")
    void unauthenticatedUserCannotAccessProtectedApi()
            throws Exception {

        mockMvc.perform(
                get("/api/users/me")
        )
        .andDo(print())
        .andExpect(status().isUnauthorized()
        );
    }


    @Test
    @DisplayName("JWT 인증 사용자는 보호 API 접근 가능")
    void authenticatedUserCanAccessProtectedApi() throws Exception {

    String token =
            jwtProvider.createAccessToken(
                    1L,
                    "testuser"
            );

    mockMvc.perform(
            get("/api/users/me")
                    .header("Authorization", "Bearer " + token)
    )
        .andDo(result -> {
            System.out.println("========== /api/users/me ==========");
            System.out.println("STATUS = " + result.getResponse().getStatus());
            System.out.println("BODY = " + result.getResponse().getContentAsString());
            System.out.println("===================================");
        })
        .andExpect(
                status().isOk()
        );
    }


    @Test
    @DisplayName("JWT 인증 사용자는 관리자 API 접근 가능")
    void authenticatedUserCanAccessAdminPath() throws Exception {

    String token =
            jwtProvider.createAccessToken(
                    2L,
                    "admin"
            );

    mockMvc.perform(
            get("/api/admin/users")
                    .header("Authorization", "Bearer " + token)
    )
        .andDo(result -> {
            System.out.println("========== /api/admin/users ==========");
            System.out.println("STATUS = " + result.getResponse().getStatus());
            System.out.println("BODY = " + result.getResponse().getContentAsString());
            System.out.println("======================================");
        })
        .andExpect(
                status().isOk()
        );
    }
}
