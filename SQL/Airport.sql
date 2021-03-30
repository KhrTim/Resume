
CREATE TABLE Модельный_ряд (
                Модель VARCHAR(30) NOT NULL,
                Тип VARCHAR(30) NOT NULL,
                Места_для_багажа INTEGER NOT NULL,
                PRIMARY KEY (Модель)
);


CREATE TABLE Самолет (
                Номер_самолета VARCHAR(10) NOT NULL,
                Модель VARCHAR(30) NOT NULL,
                PRIMARY KEY (Номер_самолета)
);


CREATE TABLE Осуществляемые_рейсы (
                Номер_рейса VARCHAR(6) NOT NULL,
                Авиаперевозчик VARCHAR(30) NOT NULL,
                PRIMARY KEY (Номер_рейса)
);


CREATE TABLE Расписание_полетов (
                Номер_рейса VARCHAR(6) NOT NULL,
                Время_отправления TIMESTAMP NOT NULL,
                Время_прибытия TIMESTAMP NOT NULL,
                Номер_самолета VARCHAR(10) NOT NULL,
                CONSTRAINT Pk_flight_schedule PRIMARY KEY (Время_отправления, Номер_рейса)
);


CREATE TABLE Текущий_статус (
                Номер_рейса VARCHAR NOT NULL,
                Время_отправления TIMESTAMP NOT NULL,
                Фактическое_время_отправления TIMESTAMP,
                Фактическое_время_прибытия TIMESTAMP,
                Статус VARCHAR(50) NOT NULL,
                CONSTRAINT Pk_current_status PRIMARY KEY (Номер_рейса, Время_отправления)
);


CREATE TABLE Пассажиры (
                Номер_рейса VARCHAR NOT NULL,
                Время_отправления TIMESTAMP NOT NULL,
                Всего INTEGER NOT NULL,
                Детей INTEGER,
                CONSTRAINT Pk_passengers PRIMARY KEY (Номер_рейса, Время_отправления)
);

CREATE TABLE Меню_услуг (
                Наименование VARCHAR(50) NOT NULL,
                Цена INTEGER NOT NULL,
                PRIMARY KEY (Наименование)
);


CREATE TABLE Список_услуг (
                Номер_рейса VARCHAR NOT NULL,
                Время_отправления TIMESTAMP NOT NULL,
                Наименование VARCHAR(50) NOT NULL,
                CONSTRAINT Pk_services_list PRIMARY KEY (Номер_рейса, Время_отправления, Наименование)
);


ALTER TABLE Самолет ADD FOREIGN KEY (Модель)
REFERENCES Модельный_ряд (Модель)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Расписание_полетов ADD FOREIGN KEY (Номер_самолета)
REFERENCES Самолет (Номер_самолета)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Расписание_полетов ADD FOREIGN KEY (Номер_рейса)
REFERENCES Осуществляемые_рейсы (Номер_рейса)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Пассажиры ADD CONSTRAINT Fk_passengers
FOREIGN KEY (Время_отправления, Номер_рейса)
REFERENCES Расписание_полетов (Время_отправления, Номер_рейса)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Текущий_статус ADD CONSTRAINT Fk_current_status
FOREIGN KEY (Время_отправления, Номер_рейса)
REFERENCES Расписание_полетов (Время_отправления, Номер_рейса)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Список_услуг ADD CONSTRAINT Fk_services_list
FOREIGN KEY (Время_отправления, Номер_рейса)
REFERENCES Расписание_полетов (Время_отправления, Номер_рейса)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;


ALTER TABLE Список_услуг ADD FOREIGN KEY (Наименование)
REFERENCES Меню_услуг (Наименование)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

INSERT INTO Модельный_ряд(Модель, Тип, Места_для_багажа) 
VALUES ('Boeing 787', 'Широкофюзеляжный', 2000),
('Boeing 747', 'Широкофюзеляжный', 4000),
('Airbus A320', 'Узкофюзеляжный', 2000),
('Gulfstream G500', 'бизнес-джет', 50);

INSERT INTO Самолет(Номер_самолета, Модель) VALUES
('RA-12567', 'Boeing 787'),
('RA-53812', 'Boeing 747'),
('RA-87354', 'Boeing 747'),
('RA-18643', 'Airbus A320'),
('RA-87232', 'Gulfstream G500');

INSERT INTO Осуществляемые_рейсы(Номер_рейса, Авиаперевозчик) VALUES
('SU35', 'Аэрофлот'),
('S71024', 'S7'),
('U6887', 'Уральские авиалинии');


INSERT INTO Меню_услуг(Наименование, Цена) VALUES
('Заправка', 100000),
('Уборка салона', 20000),
('Замена покрышек', 100000),
('Диагностика двигателей', 50000),
('Анализ информационных систем', 30000),
('Быстрая диагностика самолета', 50000);

INSERT INTO Расписание_полетов(Номер_рейса, Время_отправления, Время_прибытия, Номер_самолета) VALUES 
('SU35', '2020-12-1 22:30:00', '2020-12-2 6:30:00', 'RA-12567'),
('S71024', '2020-12-1 23:30:00', '2020-12-2 3:00:00', 'RA-53812'),
('U6887', '2020-12-2 3:00:00', '2020-12-2 8:00:00', 'RA-87354'),
('SU35', '2020-12-2 7:30:00', '2020-12-2 15:30:00', 'RA-18643');

INSERT INTO Пассажиры(Номер_рейса, Время_отправления, Всего, Детей) 
VALUES ('SU35', '2020-12-1 22:30:00', 220, 50),
('S71024', '2020-12-1 23:30:00', 150, 10),
('U6887', '2020-12-2 3:00:00', 200, 30),
('SU35', '2020-12-2 7:30:00', 170, 43);


INSERT INTO Список_услуг (Номер_рейса, Время_отправления, Наименование) 
VALUES ('SU35', '2020-12-1 22:30:00', 'Заправка'),
('SU35', '2020-12-1 22:30:00', 'Уборка салона'),
('SU35', '2020-12-1 22:30:00', 'Быстрая диагностика самолета'),
('S71024', '2020-12-1 23:30:00', 'Заправка'),
('S71024', '2020-12-1 23:30:00', 'Замена покрышек'),
('U6887', '2020-12-2 3:00:00', 'Диагностика двигателей'),
('SU35', '2020-12-2 7:30:00', 'Анализ информационных систем');

INSERT INTO Текущий_статус(Номер_рейса, Время_отправления, Фактическое_время_отправления, Фактическое_время_прибытия, Статус) 
VALUES ('SU35', '2020-12-1 22:30:00', '2020-12-1 22:45:00', '2020-12-2 6:20:00', 'Прибыл'),
('S71024', '2020-12-1 23:30:00', '2020-12-1 22:31:00', '2020-12-2 3:10:00', 'Прибыл'),
('U6887', '2020-12-2 3:00:00', '2020-12-2 3:01:00','2020-12-2 7:56:00', 'Прибыл'),
('SU35', '2020-12-2 7:30:00', '2020-12-2 7:34:00', '2020-12-2 15:38:00', 'Прибыл');


CREATE VIEW Динамическая_информация AS
SELECT p.Номер_рейса, tk.Фактическое_время_отправления, tk.Фактическое_время_прибытия, tk.Статус, sm.Номер_самолета, md.Тип AS Тип_самолета, md.Места_для_багажа, p.Всего AS Всего_пассажиров, p.Детей, su.Наименование FROM Пассажиры p LEFT JOIN Расписание_полетов rs ON (p.Номер_рейса= rs.Номер_рейса AND p.Время_отправления=rs.Время_отправления) LEFT JOIN Текущий_статус tk ON (p.Номер_рейса= tk.Номер_рейса AND p.Время_отправления=tk.Время_отправления) LEFT JOIN Самолет sm ON sm.Номер_самолета=rs.Номер_самолета LEFT JOIN Модельный_ряд md ON md.Модель=sm.Модель LEFT JOIN Список_услуг su ON (su.Номер_рейса= rs.Номер_рейса AND su.Время_отправления=rs.Время_отправления);

CREATE VIEW Статическая_информация AS
SELECT rs.Номер_рейса, rs.Время_отправления, rs.Время_прибытия, os.Авиаперевозчик, md.Тип AS Тип_самолета FROM Расписание_полетов rs LEFT JOIN Осуществляемые_рейсы os ON os.Номер_рейса=rs.Номер_рейса LEFT JOIN Самолет sm ON sm.Номер_самолета=rs.Номер_самолета LEFT JOIN Модельный_ряд md ON md.Модель=sm.Модель;

