package org.baseball.ood.scheduler;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.*;

@Component
public class RainScheduler {

    private static final String PYTHON_EXE = "C:/Users/hod76/AppData/Local/Programs/Python/Python310/python.exe";
    private static final String SCRIPT1_PATH = "src/main/python/rain_crawler.py";
    private static final String SCRIPT2_PATH = "src/main/python/rain-percent.py";
    private static boolean running = false;

    @Scheduled(cron = "0 3 * * * *")
    public synchronized void runRainScripts() {
        if (running) {
            System.out.println("[RAIN-SCHEDULER] 이미 실행 중입니다. 건너뜁니다.");
            return;
        }

        running = true;

        try {
            runPythonScript(SCRIPT1_PATH);
            runPythonScript(SCRIPT2_PATH);

        } catch (Exception e) {
            System.err.println("[RAIN-SCHEDULER] 실행 중 예외 발생");
            e.printStackTrace();
        } finally {
            running = false;
        }
    }

    private void runPythonScript(String scriptPath) throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder(PYTHON_EXE, scriptPath);
        pb.directory(new File("."));
        pb.redirectErrorStream(true);

        Process process = pb.start();

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {
        }

        int exitCode = process.waitFor();
    }
}
