package com.example.demo.menu;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class MenuSecurityIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void MENU_READ_권한이_있으면_메뉴를_조회할_수_있다()
            throws Exception {

        mockMvc.perform(
                get("/api/admin/menus")
                        .with(jwt().authorities(
                                () -> "MENU_READ"
                        ))
        )
        .andExpect(status().isOk());
    }

    @Test
    void MENU_READ_권한이_없으면_메뉴_조회가_거부된다()
            throws Exception {

        mockMvc.perform(
                get("/api/admin/menus")
                        .with(jwt().authorities(
                                () -> "USER_READ"
                        ))
        )
        .andExpect(status().isForbidden());
    }

    @Test
    void 인증된_사용자라도_MENU_READ가_없으면_403이다()
            throws Exception {

        mockMvc.perform(
                get("/api/admin/menus")
                        .with(jwt().authorities(
                                () -> "ROLE_READ"
                        ))
        )
        .andExpect(status().isForbidden());
    }

    @Test
    void 인증되지_않은_요청은_401이다()
            throws Exception {

        mockMvc.perform(
                get("/api/admin/menus"))
                .andExpect(status().isUnauthorized());
    }
}
