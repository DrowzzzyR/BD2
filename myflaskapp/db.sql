-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Янв 14 2024 г., 13:31
-- Версия сервера: 8.2.0
-- Версия PHP: 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `db`
--
CREATE DATABASE IF NOT EXISTS `db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `db`;

-- --------------------------------------------------------

--
-- Структура таблицы `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('3025af974662');

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `price` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`) VALUES
(1, 'product', '123', 123),
(2, 'product123', '456', 789),
(3, 'product12', '12', 12);

-- --------------------------------------------------------

--
-- Структура таблицы `supplies`
--

CREATE TABLE `supplies` (
  `id` int NOT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `price` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `supplies`
--

INSERT INTO `supplies` (`id`, `product_id`, `quantity`, `price`) VALUES
(1, 1, 123, '2024-01-03'),
(2, 2, 6000, '2024-01-13'),
(3, 2, 5000, '2024-01-04'),
(4, 3, 1000000, '2024-01-05');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `role` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `role`) VALUES
(7, '123', 'pbkdf2:sha256:260000$3kGKvpjNEyz0di0F$7ea990b660d03caddc82c05534af4b391e1d73ae56d27b17da387eea80c3b054', 'admin'),
(9, '1234', 'pbkdf2:sha256:260000$uwbEK496AgvCX1ur$24eeaae42da7b354bf6bdae8f20d36d6e73f78d50f512964eff9fec861356e05', 'admin'),
(10, 'admin1', 'pbkdf2:sha256:260000$uzGYeURCoTrFWoTk$49a52baedec5a0d81e58f656f93b4141c2df550b61a7a7e541862ccb5d6f38f9', 'admin'),
(11, 'admin1w2', 'pbkdf2:sha256:260000$svDCj1advJJK4lpz$fba0859a55a14c832a62682b07720ca007f990c6f2073ef4f3b83205ebc033a0', 'admin'),
(12, '1233453521152', 'pbkdf2:sha256:260000$tXm9hexAdoW22hlY$a8d7408022c55362290305f3e871e57f456bb46bb5d06ef7dea3c5c079c0d942', 'admin'),
(13, '12', 'pbkdf2:sha256:260000$iZFznX4z3NQ1GlDv$f730610793590b0adae338d4ecda2b796d22a50ddba612a0f28da8be4a3692e1', 'admin');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `supplies`
--
ALTER TABLE `supplies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_supplies_product_id_products` (`product_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_users_username` (`username`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `supplies`
--
ALTER TABLE `supplies`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `supplies`
--
ALTER TABLE `supplies`
  ADD CONSTRAINT `fk_supplies_product_id_products` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
