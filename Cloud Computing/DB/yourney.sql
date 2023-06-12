-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 09, 2023 at 02:26 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `yourney`
--

-- --------------------------------------------------------

--
-- Table structure for table `dataset`
--

CREATE TABLE `dataset` (
  `create_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `author` varchar(255) DEFAULT NULL,
  `tweet` varchar(255) DEFAULT NULL,
  `kategori` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `destinasi`
--

CREATE TABLE `destinasi` (
  `id_destinasi` int(11) NOT NULL,
  `id_kategori_destinasi` int(11) DEFAULT NULL,
  `nama_destinasi` varchar(255) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `pic_destinasi` varchar(255) DEFAULT NULL,
  `url_destinasi` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `destinasi`
--

INSERT INTO `destinasi` (`id_destinasi`, `id_kategori_destinasi`, `nama_destinasi`, `deskripsi`, `pic_destinasi`, `url_destinasi`) VALUES
(1, 1, 'Pantai Kuta Mandalika', 'Pantai Kuta Mandalika merupakan salah satu destinasi wisata bahari yang cukup populer di Lombok Nusa Tenggara Barat. Kuta Beach Lombok menyimpan sejumlah daya tarik berupa pesona alam yang dapat anda saksikan secara lebih dekat dengan mengunjunginya. Wisata Pantai Kuta Lombok wajib banget untuk anda explore lebih dalam dan temukan berbagai keseruan yang menyenangkan. View yang ditawarkan Pantai Kuta Lombok terlihat begitu menakjubkan dan akan membuat banyak pasanng takjub dengan keindahannya.', 'https://jengsusan.com/wp-content/uploads/2019/02/Serunya-Berlibur-ke-Pantai-Kuta-Mandalika-di-Lombok-min.jpg', 'https://www.traveloka.com/en-id/activities/indonesia/product/kuta-mandalika-full-day-tour-by-private-car-8434318511476'),
(2, 1, 'Pantai Kuta Mandalika', 'Pantai Kuta Mandalika merupakan salah satu destinasi wisata bahari yang cukup populer di Lombok Nusa Tenggara Barat. Kuta Beach Lombok menyimpan sejumlah daya tarik berupa pesona alam yang dapat anda saksikan secara lebih dekat dengan mengunjunginya. Wisata Pantai Kuta Lombok wajib banget untuk anda explore lebih dalam dan temukan berbagai keseruan yang menyenangkan. View yang ditawarkan Pantai Kuta Lombok terlihat begitu menakjubkan dan akan membuat banyak pasanng takjub dengan keindahannya.', 'https://jengsusan.com/wp-content/uploads/2019/02/Serunya-Berlibur-ke-Pantai-Kuta-Mandalika-di-Lombok-min.jpg', 'https://www.traveloka.com/en-id/activities/indonesia/product/kuta-mandalika-full-day-tour-by-private-car-8434318511476');

-- --------------------------------------------------------

--
-- Table structure for table `kategori`
--

CREATE TABLE `kategori` (
  `id_kategori_user` int(11) NOT NULL,
  `id_kategori` int(11) DEFAULT NULL,
  `id_destinasi1` int(11) DEFAULT NULL,
  `nama_kategori` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `kategori`
--

INSERT INTO `kategori` (`id_kategori_user`, `id_kategori`, `id_destinasi1`, `nama_kategori`) VALUES
(1, NULL, NULL, ''),
(2, NULL, NULL, ''),
(3, NULL, NULL, ''),
(4, NULL, NULL, ''),
(5, NULL, NULL, ''),
(6, NULL, NULL, ''),
(7, NULL, NULL, ''),
(8, NULL, NULL, '');

-- --------------------------------------------------------

--
-- Table structure for table `pictures`
--

CREATE TABLE `pictures` (
  `id_pic` int(11) NOT NULL,
  `pic` mediumblob DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tokenblocklist`
--

CREATE TABLE `tokenblocklist` (
  `id` int(11) NOT NULL,
  `jti` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `tokenblocklist`
--

INSERT INTO `tokenblocklist` (`id`, `jti`, `type`, `created_at`) VALUES
(1, '8927ae66-0583-492b-bed6-c4d25667de17', 'access', '2023-06-07 15:47:00'),
(2, '1d06464e-fad1-4ebc-bc47-7686a0fed76b', 'access', '2023-06-09 12:21:46'),
(3, '89a12744-f693-49fc-960a-7d4fd507b8be', 'access', '2023-06-09 12:21:54');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `id_kategori1` int(11) DEFAULT NULL,
  `idToken` int(11) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT current_timestamp(),
  `full_name` varchar(255) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `jenis_kelamin` varchar(255) DEFAULT NULL,
  `tempat_lahir` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `user_pic` varchar(255) DEFAULT NULL,
  `username_twitter` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `id_kategori1`, `idToken`, `create_time`, `full_name`, `username`, `password`, `jenis_kelamin`, `tempat_lahir`, `status`, `email`, `user_pic`, `username_twitter`) VALUES
(3, 3, NULL, '2023-06-07 07:37:10', NULL, 'rafli1.0', '7433215182389748344', 'Laki', 'BDGz', 'admin', 'rafli1.0@yopmail.com', NULL, NULL),
(4, 4, NULL, '2023-06-07 07:41:34', 'rafli', 'rafli2.0', '$5$rounds=535000$FHFDp7XZ6EiBcUrc$nbjBMPeCznEalMmVe4mXXoJk0HU6fKZ3wihNsHrMBWB', 'Laki', 'BDGz', 'admin', 'rafli2.0@yopmail.com', NULL, '@no_need_sleep'),
(5, 5, NULL, '2023-06-07 07:44:12', NULL, 'rafli3.0', '$5$rounds=535000$WyK4rl2g5R7QPR4w$o1jZiqrFnAdsRVyPzIbLgc3YiyRFt5SwNnCMckQumXD', 'Laki', 'BDGz', NULL, 'rafli3.0@yopmail.com', NULL, NULL),
(6, 6, NULL, '2023-06-07 08:17:45', NULL, 'rafli4.0', '$5$rounds=535000$CJxFD78HvBLtEBz8$URSWmZ4Ou4lyUsiXywyaJ.KBPtG94s4f9EeXS7tDWQ4', 'Laki', 'BDGz', NULL, 'rafli4.0@yopmail.com', NULL, NULL),
(7, 7, NULL, '2023-06-07 08:29:32', NULL, 'rafli9.0', '$5$rounds=535000$Mag6owQPPXck4joR$CPkvUk4MjuLIvXDo4kd4.ejg9U/VTlWlALl0JM.WDQA', 'Laki', 'BDGz', NULL, 'rafli9.0@yopmail.com', NULL, NULL),
(8, 8, NULL, '2023-06-07 08:32:10', NULL, 'rafli11.0', '$5$rounds=535000$8criuAdTSeh7dRc8$KN8eL3V8/uC5yyferkrCf05kSrg9P9ztyRsygV1A9B3', 'Laki', 'BDGz', NULL, 'rafli11.0@yopmail.com', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_liked`
--

CREATE TABLE `user_liked` (
  `id_like` int(11) NOT NULL,
  `id_user_liked` int(11) DEFAULT NULL,
  `id_destination_like` int(11) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `destinasi`
--
ALTER TABLE `destinasi`
  ADD PRIMARY KEY (`id_destinasi`),
  ADD KEY `id_kategori_destinasi` (`id_kategori_destinasi`);

--
-- Indexes for table `kategori`
--
ALTER TABLE `kategori`
  ADD PRIMARY KEY (`id_kategori_user`),
  ADD KEY `id_dataset1` (`id_kategori`,`id_destinasi1`),
  ADD KEY `id_destinasi1` (`id_destinasi1`);

--
-- Indexes for table `pictures`
--
ALTER TABLE `pictures`
  ADD PRIMARY KEY (`id_pic`);

--
-- Indexes for table `tokenblocklist`
--
ALTER TABLE `tokenblocklist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD KEY `idToken` (`idToken`),
  ADD KEY `id_kategori1` (`id_kategori1`);

--
-- Indexes for table `user_liked`
--
ALTER TABLE `user_liked`
  ADD PRIMARY KEY (`id_like`),
  ADD KEY `id_user_liked` (`id_user_liked`,`id_destination_like`),
  ADD KEY `id_destination_like` (`id_destination_like`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `destinasi`
--
ALTER TABLE `destinasi`
  MODIFY `id_destinasi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pictures`
--
ALTER TABLE `pictures`
  MODIFY `id_pic` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tokenblocklist`
--
ALTER TABLE `tokenblocklist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user_liked`
--
ALTER TABLE `user_liked`
  MODIFY `id_like` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `kategori`
--
ALTER TABLE `kategori`
  ADD CONSTRAINT `kategori_ibfk_1` FOREIGN KEY (`id_destinasi1`) REFERENCES `destinasi` (`id_kategori_destinasi`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_2` FOREIGN KEY (`id_kategori1`) REFERENCES `kategori` (`id_kategori_user`);

--
-- Constraints for table `user_liked`
--
ALTER TABLE `user_liked`
  ADD CONSTRAINT `user_liked_ibfk_2` FOREIGN KEY (`id_destination_like`) REFERENCES `destinasi` (`id_destinasi`),
  ADD CONSTRAINT `user_liked_ibfk_3` FOREIGN KEY (`id_user_liked`) REFERENCES `user` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
