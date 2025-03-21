package com.example.javaserver.model;

public class Lesson {
    private String subject;
    private String location;
    private String teacher;
    private String startTime;
    private String endTime;

    public Lesson() {}

    public Lesson(String subject, String location, String teacher, String startTime, String endTime) {
        this.subject = subject;
        this.location = location;
        this.teacher = teacher;
        this.startTime = startTime;
        this.endTime = endTime;
    }

    // Getters and setters
    public String getSubject() { return subject; }
    public void setSubject(String subject) { this.subject = subject; }

    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }

    public String getTeacher() { return teacher; }
    public void setTeacher(String teacher) { this.teacher = teacher; }

    public String getStartTime() { return startTime; }
    public void setStartTime(String startTime) { this.startTime = startTime; }

    public String getEndTime() { return endTime; }
    public void setEndTime(String endTime) { this.endTime = endTime; }
}