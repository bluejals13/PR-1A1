// backend/src/main/java/com/example/demo/common/dto/ApiResponse.java
package com.example.demo.common.dto;

public record ApiResponse<T>(
        String status,
        String message,
        T data
) {

    // 성공 + 데이터
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(
                "SUCCESS",
                "요청이 성공적으로 처리되었습니다.",
                data
        );
    }

    // 성공 + 데이터 + 메시지
    public static <T> ApiResponse<T> success(T data, String message) {
        return new ApiResponse<>(
                "SUCCESS",
                message,
                data
        );
    }

    // 성공 + 메시지만
    public static ApiResponse<Void> success(String message) {
        return new ApiResponse<>(
                "SUCCESS",
                message,
                null
        );
    }

    // 에러
    public static ApiResponse<Void> error(String message) {
        return new ApiResponse<>(
                "ERROR",
                message,
                null
        );
    }
}
