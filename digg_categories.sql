-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 16, 2012 at 04:00 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `digg_newdatabase`
--

-- --------------------------------------------------------

--
-- Table structure for table `digg_categories`
--

CREATE TABLE IF NOT EXISTS `digg_categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(50) NOT NULL,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `digg_categories`
--

INSERT INTO `digg_categories` (`category_id`, `category_name`, `description`) VALUES
(1, 'sports', 'Sports Digg Articles'),
(2, 'entertainment', 'Entertainment Digg Articles'),
(3, 'politics', 'Politics News'),
(4, 'technology', 'Technology News'),
(5, 'science', 'Science News'),
(6, 'world_news', 'World News'),
(7, 'Unknown', 'unknown');
