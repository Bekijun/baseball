package org.baseball.ood.scheduler;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.*;

@Component
public class RainScheduler {

    private static final String PYTHON_EXE = "C:/Users/hod76/AppData/Local/Programs/Python/Python310/python.exe";
    private static final String SCRIPT1_PATH = "src/main/python/rain_crawler.py";
    private static final String SCRIPT2_PATH = "src/main/python/rain_percent.py";

    @Scheduled(cron = "0 0 * * * *")  // 매 정각마다 실행
    public void runRainScripts() {
        System.out.println("[스케줄] 정각마다 파이썬 스크립트 실행 시작");

        runPythonScript(SCRIPT1_PATH);
        runPythonScript(SCRIPT2_PATH);

        System.out.println("[스케줄] 모든 스크립트 실행 완료");
    }

    private void runPythonScript(String scriptPath) {
        try {
            ProcessBuilder pb = new ProcessBuilder(PYTHON_EXE, scriptPath);
            pb.directory(new File("."));  // 현재 프로젝트 루트 기준
            pb.redirectErrorStream(true);

            Process process = pb.start();

            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println("[PYTHON] " + line);
                }
            }

            int exitCode = process.waitFor();
            System.out.println("[스케줄] " + scriptPath + " 종료 코드: " + exitCode);

        } catch (IOException | InterruptedException e) {
            System.err.println("[ERROR] " + scriptPath + " 실행 중 예외 발생");
            e.printStackTrace();
        }
    }
}
