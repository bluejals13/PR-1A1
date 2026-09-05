package com.example.demo.auth.security;

public class RedisUnavailableException extends RuntimeException {

    public RedisUnavailableException(String message, Throwable cause) {
        super(message, cause);
    }

}
