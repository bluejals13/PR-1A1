// backend/src/main/java/com/example/demo/common/exception/GlobalExceptionHandler.java
package com.example.demo.common.exception;

import com.example.demo.common.dto.ApiResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

        // 1. @Valid 유효성 검사 실패 (400)
        @ExceptionHandler(MethodArgumentNotValidException.class)
        public ResponseEntity<ApiResponse<Void>> handleValidationExceptions(MethodArgumentNotValidException ex) {
            String errorMessage = ex.getBindingResult().getFieldErrors().stream()
                    .findFirst()
                    .map(err -> err.getDefaultMessage())
                    .orElse("잘못된 요청 파라미터입니다.");
            log.warn("Validation Error: {}", errorMessage);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(ApiResponse.error(errorMessage));
        }

        // 2. 비즈니스 파라미터 검증 실패 / 잘못된 인자 (400)
        @ExceptionHandler(IllegalArgumentException.class)
        public ResponseEntity<ApiResponse<Void>> handleIllegalArgumentException(IllegalArgumentException ex) {
            log.warn("Illegal Argument: {}", ex.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(ApiResponse.error(ex.getMessage()));
        }


        // 3. 인증 실패 (401)
        @ExceptionHandler(BadCredentialsException.class)
        public ResponseEntity<ApiResponse<Void>> handleBadCredentials(BadCredentialsException ex) {
            log.warn("Unauthorized: {}", ex.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(ApiResponse.error("인증에 실패했습니다."));
        }


        // 4. 권한 부족 (403)
        @ExceptionHandler(AccessDeniedException.class)
        public ResponseEntity<ApiResponse<Void>> handleAccessDenied(AccessDeniedException ex) {
            log.warn("Access Denied: {}", ex.getMessage());
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(ApiResponse.error("접근 권한이 없습니다."));
        }

        // 5. 서버 내부 예외 (500)
        @ExceptionHandler(Exception.class)
        public ResponseEntity<ApiResponse<Void>> handleAllExceptions(Exception ex) {
            log.error("Internal Server Error: ", ex);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(ApiResponse.error("서버 내부 오류가 발생했습니다. 관리자에게 문의하세요."));
        }

}