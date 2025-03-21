

// javaserver.java
package com.example.javaserver;

import com.example.javaserver.model.Lesson;
import com.example.javaserver.service.ScraperService;
import com.example.javaserver.util.CredentialReader;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Service;

import java.io.File;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
public class JavaServer implements CommandLineRunner {

    private final ScraperService scraperService;

    public JavaServer(ScraperService scraperService) {
        this.scraperService = scraperService;
    }

    public static void main(String[] args) {
        SpringApplication.run(JavaServer.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        scraperService.scrapeAndSaveSchedule();
    }
}
