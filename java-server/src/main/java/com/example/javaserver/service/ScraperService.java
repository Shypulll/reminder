package com.example.javaserver.service;

import com.example.javaserver.util.CredentialReader;
import com.example.javaserver.model.Lesson;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class ScraperService {

    public void scrapeAndSaveSchedule() throws Exception {
        String[] credentials = CredentialReader.readCredentials();
        String username = credentials[0];
        String password = credentials[1];

        System.setProperty("webdriver.chrome.driver", "/opt/homebrew/bin/chromedriver");
        ChromeOptions options = new ChromeOptions();
        //options.addArguments("--headless");
        WebDriver driver = new ChromeDriver(options);

        try {
            driver.get("https://student.vizja.app");
            Thread.sleep(2000);

            // Нажимаем кнопку "Войти через Microsoft"
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
           // wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".fc-event-main")));

            WebElement loginButton = wait.until(ExpectedConditions.elementToBeClickable(
                    By.cssSelector("a[href*='microsoft']")  // ищет ссылку с microsoft в href
            ));

            loginButton.click();

            wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("loginfmt"))).sendKeys(username);
            driver.findElement(By.id("idSIButton9")).click();

            Thread.sleep(4000);
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("passwd"))).sendKeys(password);
            driver.findElement(By.id("idSIButton9")).click();


// Пропустить «остаться в системе»
            Thread.sleep(4000);
            List<WebElement> stayButtons = driver.findElements(By.id("idBtn_Back"));
            //if (!stayButtons.isEmpty()) {
                stayButtons.get(0).click();
            //}

            Thread.sleep(15000);
            String currentUrl = driver.getCurrentUrl();
            System.out.println(currentUrl);

//            if (currentUrl.contains("login")) {
//                System.out.println("❌ Вход не выполнен. Проверь логин и пароль.");
//                return;
//            }
//            // Вводим логин и пароль на странице Microsoft
//            driver.findElement(By.name("loginfmt")).sendKeys(username);
//            driver.findElement(By.id("idSIButton9")).click();
//            Thread.sleep(2000);
//
//            driver.findElement(By.name("passwd")).sendKeys(password);
//            driver.findElement(By.id("idSIButton9")).click();
//            Thread.sleep(3000);
//
//            // Пропустить сохранение входа
//            List<WebElement> yesButtons = driver.findElements(By.id("idBtn_Back"));
//            if (!yesButtons.isEmpty()) {
//                yesButtons.get(0).click();
//            }

            Thread.sleep(5000);

            // Открываем расписание
            driver.get("https://student.vizja.app/schedule");
            String currentUrl1 = driver.getCurrentUrl();
            System.out.println(currentUrl1);
            Thread.sleep(8000);
            try (PrintWriter out = new PrintWriter("full_schedule_page.html", StandardCharsets.UTF_8)) {
                out.println(driver.getPageSource());
                System.out.println("📄 HTML страницы сохранён в full_schedule_page.html");
            }
            // Пока что просто пример — позже спарсим расписание
            List<Lesson> lessons = new ArrayList<>();

            List<WebElement> lessonElements = driver.findElements(By.cssSelector(".fc-event-main"));
            System.out.println("🔍 Найдено элементов расписания: " + lessonElements.size());

            for (WebElement el : lessonElements) {
                try {
                    // Время
                    String time = el.findElement(By.cssSelector(".fc-event-time")).getText();
                    String[] parts = time.split("-");
                    String startTime = parts[0].trim();
                    String endTime = parts[1].trim();

                    // Название предмета + аудитория
                    WebElement titleDiv = el.findElement(By.cssSelector(".fc-event-title.fc-sticky > div"));
                    String fullTitle = titleDiv.getText(); // например: L4 Systemy wbudowane Babka Tower s.212 IT

                    // Можно позже разбить fullTitle на части: L4 (группа), название, место и т.д.
                    String subject = fullTitle;
                    String location = "–"; // временно
                    String teacher = "–";  // временно

                    lessons.add(new Lesson(subject, location, teacher, startTime, endTime));
                } catch (Exception ex) {
                    System.out.println("⚠️ Ошибка при парсинге одного из блоков: " + ex.getMessage());
                }
            }


            ObjectMapper mapper = new ObjectMapper();
            mapper.writeValue(new File("schedule.json"), lessons);

            System.out.println("✅ Расписание сохранено в schedule.json");
        } finally {
            driver.quit();
        }
    }
}