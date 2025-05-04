-- 1. 선수 정보
CREATE TABLE IF NOT EXISTS players (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT NOT NULL,
                                       team TEXT NOT NULL,
                                       position TEXT NOT NULL,
                                       stats TEXT,
                                       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 팀 정보
CREATE TABLE IF NOT EXISTS teams (
                                     team_name TEXT PRIMARY KEY,
                                     wins INTEGER,
                                     losses INTEGER,
                                     draws INTEGER,
                                     win_rate REAL,
                                     rank INTEGER,
                                     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. 야구 용어
CREATE TABLE IF NOT EXISTS terms (
                                     term TEXT PRIMARY KEY,
                                     description TEXT,
                                     source TEXT
);

-- 샘플 데이터 삽입

-- players
INSERT INTO players (name, team, position, stats) VALUES
                                                      ('전준우', '롯데', '외야수', '{"타율": "0.312", "홈런": "15"}'),
                                                      ('이대호', '롯데', '지명타자', '{"타율": "0.331", "홈런": "27"}');

-- teams
INSERT INTO teams (team_name, wins, losses, draws, win_rate, rank) VALUES
    ('롯데', 68, 63, 13, 0.519, 5);

-- terms
INSERT INTO terms (term, description, source) VALUES
                                                  ('타율', '전체 타수 대비 안타 수의 비율. 보통 0.300 이상이면 우수.', 'https://ko.wikipedia.org/wiki/타율'),
                                                  ('홈런', '타자가 친 공이 외야 담장을 넘겨서 곧바로 득점이 되는 것.', 'https://ko.wikipedia.org/wiki/홈런');
