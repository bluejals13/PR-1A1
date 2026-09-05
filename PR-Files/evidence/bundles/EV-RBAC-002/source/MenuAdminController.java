package com.example.demo.iam.menu;

import com.example.demo.iam.menu.dto.MenuRequest;
import com.example.demo.iam.menu.dto.MenuResponse;
import com.example.demo.iam.menu.service.MenuAdminService;

import com.example.demo.common.dto.ApiResponse;

import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin/menus")
@RequiredArgsConstructor
public class MenuAdminController {

    private final MenuAdminService menuAdminService;

    @PreAuthorize("hasAuthority('MENU_READ')")
    @GetMapping
    public ApiResponse<List<MenuResponse>> getMenus() {
        return ApiResponse.success(menuAdminService.getMenus());
    }
    @PreAuthorize("hasAuthority('MENU_READ')")
    @GetMapping("/{id}")
    public ApiResponse<MenuResponse> getMenu(
            @PathVariable Long id
    ) {
        return ApiResponse.success(menuAdminService.getMenu(id));
    }

    @PreAuthorize("hasAuthority('MENU_CREATE')")
    @PostMapping
    public ApiResponse<Void> createMenu(@RequestBody MenuRequest request) {
        menuAdminService.createMenu(request);
        return ApiResponse.<Void>success(null, "메뉴 생성에 성공했습니다.");
    }

    @PreAuthorize("hasAuthority('MENU_UPDATE')")
    @PatchMapping("/{id}")
    public ApiResponse<Void> updateMenu(
        @PathVariable Long id,
        @RequestBody MenuRequest request
    ) {
        menuAdminService.updateMenu(id, request);
        return ApiResponse.<Void>success(null, "메뉴 수정에 성공했습니다.");
    }

    @PreAuthorize("hasAuthority('MENU_DELETE')")
    @DeleteMapping("/{id}")
    public ApiResponse<Void> deleteMenu(@PathVariable Long id) {
        menuAdminService.deleteMenu(id);
        return ApiResponse.<Void>success(null, "메뉴 삭제에 성공했습니다.");
    }
}
