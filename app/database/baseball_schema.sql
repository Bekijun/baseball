-- 1. 선수 정보 (상세 정보 포함)
CREATE TABLE IF NOT EXISTS players (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT,
                                       birthday TEXT,
                                       height INTEGER,
                                       weight INTEGER,
                                       team TEXT,
                                       position TEXT,
                                       debut_year INTEGER,
                                       introduction TEXT,
                                       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. 선수 성적 정보 (연도별, 항목별)
CREATE TABLE IF NOT EXISTS player_stats (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            player_id INTEGER NOT NULL,
                                            season TEXT NOT NULL,
                                            stat_type TEXT NOT NULL,
                                            value TEXT NOT NULL,
                                            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                                            FOREIGN KEY (player_id) REFERENCES players(id)
);

-- 3. 팀 정보
CREATE TABLE IF NOT EXISTS teams (
                                     team_name TEXT PRIMARY KEY,
                                     wins INTEGER,
                                     losses INTEGER,
                                     draws INTEGER,
                                     win_rate REAL,
                                     rank INTEGER,
                                     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. 야구 용어
CREATE TABLE IF NOT EXISTS terms (
                                     term TEXT PRIMARY KEY,
                                     description TEXT,
                                     source TEXT
);
