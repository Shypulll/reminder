package com.example.javaserver.util;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.InputStream;

public class CredentialReader {
    public static String[] readCredentials() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        InputStream is = CredentialReader.class.getClassLoader().getResourceAsStream("credentials.json");
        JsonNode root = mapper.readTree(is);
        return new String[]{
                root.get("username").asText(),
                root.get("password").asText()
        };
    }
}