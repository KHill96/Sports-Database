DROP TABLE IF EXISTS NBA.Standings;
DROP TABLE IF EXISTS NBA.Total_Stats;
DROP TABLE IF EXISTS NBA.Per_100_Stats;
DROP TABLE IF EXISTS NBA.Team_Standings;
DROP TABLE IF EXISTS NBA.Teams;
DROP TABLE IF EXISTS NBA.Players;
DROP SCHEMA IF EXISTS NBA;

-- Create the schema
CREATE SCHEMA NBA;

-- Create the referenced tables first
-- Teams
CREATE TABLE NBA.Teams
(
    Team_ID SMALLINT NOT NULL PRIMARY KEY,
    Team_Name CHAR(33) NOT NULL,
    Team_Abbreviation CHAR(3) NOT NULL
);
-- Players
CREATE TABLE NBA.Players
(
    Player_ID SMALLINT NOT NULL PRIMARY KEY,
    First_Name char(25) NOT NULL,
    Last_Name char(25) NOT NULL,
    Suffix char(5) NULL,
    Year_Started SMALLINT NOT NULL,
    Year_Last_Active SMALLINT NOT NULL,
    Position char(3) NOT NULL,
    Height_Feet SMALLINT NOT NULL,
    Height_Inches SMALLINT NOT NULL,
    Weight SMALLINT NULL,
    Birthday DATE NULL,
    College char(100) NULL
);

-- Create the tables that are referencing the tables above
-- Team Standings
CREATE TABLE NBA.Team_Standings
(
    Season SMALLINT NOT NULL,
    Team_ID SMALLINT NOT NULL,
    Total_Wins SMALLINT NOT NULL,
    Total_Losses SMALLINT NOT NULL,
    Home_Wins SMALLINT NOT NULL,
    Home_Losses SMALLINT NOT NULL,
    Road_Wins SMALLINT NOT NULL,
    Road_Losses SMALLINT NOT NULL,
    Neutral_Wins SMALLINT NULL,
    Neutral_Losses SMALLINT NULL,
    Eastern_Conference_Wins SMALLINT NOT NULL,
    Eastern_Conference_Losses SMALLINT NOT NULL,
    Western_Conference_Wins SMALLINT NOT NULL,
    Western_Conference_Losses SMALLINT NOT NULL,
    CONSTRAINT "PK_Team_Standings_Composite" PRIMARY KEY (Season,Team_ID),
    -- This connects to the teams table which acts as a bridge table
    CONSTRAINT "FK_Standings_Team_Bridge" FOREIGN KEY (Team_ID) REFERENCES NBA.Teams(Team_ID) 
);
-- Indices/Indexes of the foreign keys
CREATE INDEX "FK_Index_Standings_Team_Bridge" ON NBA.Team_Standings
(
    Team_ID
);

-- Total Stats
CREATE TABLE NBA.Total_Stats
(
    Player_ID SMALLINT NOT NULL,
    Team_ID SMALLINT NOT NULL,
    Season SMALLINT NOT NULL,
    Age SMALLINT NOT NULL,
    Games_Played SMALLINT NOT NULL,
    Minutes SMALLINT NOT NULL,
    Points SMALLINT NOT NULL,
    Field_Goals_Made SMALLINT NOT NULL,
    Field_Goals_Attempted SMALLINT NOT NULL,
    FG_3P_Made SMALLINT NULL,
    FG_3P_Attempted SMALLINT NULL,
    FG_2P_Made SMALLINT NOT NULL,
    FG_2P_Attempted SMALLINT NOT NULL,
    FT_Made SMALLINT NOT NULL,
    FT_Attempted SMALLINT NOT NULL,
    Offensive_Rebounds SMALLINT NOT NULL,
    Defensive_Rebounds SMALLINT NOT NULL,
    Assists SMALLINT NOT NULL,
    Turnovers SMALLINT NULL,
    Steals SMALLINT NOT NULL,
    Blocks SMALLINT NOT NULL,
    Personal_Fouls SMALLINT NOT NULL,
    CONSTRAINT "PK_Totals_Composite" PRIMARY KEY(Player_ID,Team_ID,Season,Age),
    -- This connects to the teams table which acts as a bridge table
    CONSTRAINT "FK_Totals_Teams" FOREIGN KEY (Team_ID) REFERENCES NBA.Teams,
    CONSTRAINT "FK_Totals_Players" FOREIGN KEY(Player_ID) REFERENCES NBA.Players
);
-- Indices/Indexes of the foreign keys
-- Teams and Total Stats
CREATE INDEX "FK_Index_Teams_Total_Stats" ON NBA.Total_Stats
(
    Team_ID
);
-- Players and Total Stats
CREATE INDEX "FK_Index_Players_Total_Stats" ON NBA.Total_Stats
(
    Player_ID
);

-- Per 100 Stats
CREATE TABLE NBA.Per_100_Stats
(
    Player_ID SMALLINT NOT NULL,
    Team_ID SMALLINT NOT NULL,
    Season SMALLINT NOT NULL,
    Age SMALLINT NOT NULL,
    Games_Played SMALLINT NOT NULL,
    Minutes SMALLINT NOT NULL,
    Points REAL NOT NULL,
    Field_Goals_Made REAL NOT NULL,
    Field_Goals_Attempted REAL NOT NULL,
    FG_3P_Made REAL NULL,
    FG_3P_Attempted REAL NULL,
    FG_2P_Made REAL NOT NULL,
    FG_2P_Attempted REAL NOT NULL,
    FT_Made REAL NOT NULL,
    FT_Attempted REAL NOT NULL,
    Offensive_Rebounds REAL NOT NULL,
    Defensive_Rebounds REAL NOT NULL,
    Assists REAL NOT NULL,
    Turnovers REAL NULL,
    Steals REAL NOT NULL,
    Blocks REAL NOT NULL,
    Personal_Fouls REAL NOT NULL,
    Offensive_Rating REAL NULL,
    Defensive_Rating REAL NOT NULL,
    CONSTRAINT "PK_Per_100_Composite" PRIMARY KEY(Player_ID,Team_ID,Season),
    CONSTRAINT "FK_Per_100_Teams" FOREIGN KEY (Team_ID) REFERENCES NBA.Teams,
    CONSTRAINT "FK_Per_100_Players" FOREIGN KEY(Player_ID) REFERENCES NBA.Players
);
-- Indices/Indexes of the foreign keys
-- Teams and Per 100
CREATE INDEX "FK_Index_Teams_Per_100_Stats" ON NBA.Per_100_Stats
(
    Team_ID
);
-- Players and Per 100
CREATE INDEX "FK_Index_Players_Per_100_Stats" ON NBA.Per_100_Stats
(
    Player_ID
);
